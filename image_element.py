import os
import numpy as np
from OpenGL.GL import *
from PIL import Image
from video_base import VideoBase


class ImageElement(VideoBase):
    """Image element for rendering image files"""
    def __init__(self, image_path: str, scale: float = 1.0):
        super().__init__()
        self.image_path = image_path
        self.scale = scale
        self.texture_id = None
        self.texture_width = 0
        self.texture_height = 0
        self.original_width = 0
        self.original_height = 0
        self._create_image_texture()
        # 初期化時にサイズを計算
        self.calculate_size()
    
    def _create_image_texture(self):
        """Initialize image texture creation"""
        # Texture creation is deferred until render time (requires OpenGL context)
        self.texture_created = False
    
    def _create_texture_now(self):
        """Create texture within OpenGL context"""
        if not os.path.exists(self.image_path):
            print(f"Warning: Image file not found: {self.image_path}")
            return
        
        try:
            # Load image
            img = Image.open(self.image_path)
            
            # Convert to RGBA format (for alpha channel support)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Save original size
            self.original_width, self.original_height = img.size
            
            # Apply scaling
            if self.scale != 1.0:
                new_width = int(self.original_width * self.scale)
                new_height = int(self.original_height * self.scale)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Apply corner radius clipping to image content
            img = self._apply_corner_radius_to_image(img)
            
            # Apply border and background
            img = self._apply_border_and_background_to_image(img)
            
            # Update texture size
            self.texture_width, self.texture_height = img.size
            
            # ボックスサイズを更新（背景・枠線を含む最終サイズ）
            self.width = self.texture_width
            self.height = self.texture_height
            
            # Convert image to NumPy array and flip vertically for OpenGL
            img_data = np.array(img)
            img_data = np.flipud(img_data)  # Flip image vertically for OpenGL coordinate system
            
            # Generate OpenGL texture
            self.texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            
            # Set texture parameters
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            
            # Upload texture data
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.texture_width, self.texture_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
            
            glBindTexture(GL_TEXTURE_2D, 0)
            self.texture_created = True
            
        except Exception as e:
            print(f"Error loading image {self.image_path}: {e}")
            self.texture_created = False
    
    def set_scale(self, scale: float):
        """Set image scale"""
        self.scale = scale
        # Need to recreate texture
        if self.texture_created:
            self.texture_created = False
        # サイズを再計算
        self.calculate_size()
        return self
    
    def render(self, time: float):
        """Render image"""
        if not self.is_visible_at(time):
            return
        
        # Create texture if not yet created
        if not self.texture_created:
            self._create_texture_now()
        
        if self.texture_id is None or not self.texture_created:
            return
        
        # Save current OpenGL state
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        
        # Enable texture
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        
        # Enable alpha blending
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Set texture environment to replace (preserves texture colors)
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        
        # Draw textured quad with corrected texture coordinates
        glBegin(GL_QUADS)
        # Bottom-left
        glTexCoord2f(0.0, 0.0)
        glVertex2f(self.x, self.y + self.texture_height)
        
        # Bottom-right
        glTexCoord2f(1.0, 0.0)
        glVertex2f(self.x + self.texture_width, self.y + self.texture_height)
        
        # Top-right
        glTexCoord2f(1.0, 1.0)
        glVertex2f(self.x + self.texture_width, self.y)
        
        # Top-left
        glTexCoord2f(0.0, 1.0)
        glVertex2f(self.x, self.y)
        glEnd()
        
        # Restore OpenGL state
        glPopAttrib()

    def calculate_size(self):
        """画像のボックスサイズを事前計算"""
        if not os.path.exists(self.image_path):
            self.width = 0
            self.height = 0
            return
        
        try:
            # 画像の情報だけを取得（実際の読み込みはしない）
            from PIL import Image
            with Image.open(self.image_path) as img:
                original_width, original_height = img.size
            
            # スケールを適用
            scaled_width = int(original_width * self.scale)
            scaled_height = int(original_height * self.scale)
            
            # パディングを含むキャンバスサイズを計算
            canvas_width = scaled_width + self.padding['left'] + self.padding['right']
            canvas_height = scaled_height + self.padding['top'] + self.padding['bottom']
            
            # 最小サイズを保証
            canvas_width = max(canvas_width, 1)
            canvas_height = max(canvas_height, 1)
            
            # ボックスサイズを更新
            self.width = canvas_width
            self.height = canvas_height
            
        except Exception as e:
            print(f"Error calculating image size {self.image_path}: {e}")
            self.width = 0
            self.height = 0
    
    def __del__(self):
        """Destructor to clean up texture"""
        if self.texture_id:
            try:
                glDeleteTextures(1, [self.texture_id])
            except:
                pass