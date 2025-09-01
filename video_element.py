import os
import cv2
import numpy as np
from OpenGL.GL import *
from PIL import Image
from video_base import VideoBase


class VideoElement(VideoBase):
    """Video clip element for rendering video files"""
    def __init__(self, video_path: str, scale: float = 1.0):
        super().__init__()
        self.video_path = video_path
        self.scale = scale
        self.texture_id = None
        self.texture_width = 0
        self.texture_height = 0
        self.original_width = 0
        self.original_height = 0
        self.video_capture = None
        self.fps = 30.0
        self.total_frames = 0
        self.current_frame_data = None
        self._create_video_texture()
    
    def _create_video_texture(self):
        """Initialize video texture creation"""
        # Texture creation is deferred until render time (requires OpenGL context)
        self.texture_created = False
        self._load_video_info()
    
    def _load_video_info(self):
        """Load video file information"""
        if not os.path.exists(self.video_path):
            print(f"Warning: Video file not found: {self.video_path}")
            return
        
        try:
            self.video_capture = cv2.VideoCapture(self.video_path)
            
            if not self.video_capture.isOpened():
                print(f"Error: Cannot open video file: {self.video_path}")
                return
            
            # Get video properties
            self.original_width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.original_height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.fps = self.video_capture.get(cv2.CAP_PROP_FPS)
            self.total_frames = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Calculate scaled dimensions (border/background will be applied at render time)
            base_width = int(self.original_width * self.scale)
            base_height = int(self.original_height * self.scale)
            
            # Add padding to texture dimensions
            self.texture_width = base_width + self.padding['left'] + self.padding['right']
            self.texture_height = base_height + self.padding['top'] + self.padding['bottom']
            
            print(f"Video loaded: {self.original_width}x{self.original_height}, {self.fps} fps, {self.total_frames} frames")
            
        except Exception as e:
            print(f"Error loading video info {self.video_path}: {e}")
    
    def _create_texture_now(self):
        """Create OpenGL texture"""
        if self.texture_id is None:
            self.texture_id = glGenTextures(1)
        
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        
        # Set texture parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        
        glBindTexture(GL_TEXTURE_2D, 0)
        self.texture_created = True
    
    def _get_frame_at_time(self, video_time: float):
        """Get video frame at specific time"""
        if self.video_capture is None or not self.video_capture.isOpened():
            return None
        
        # Calculate frame number based on time
        frame_number = int(video_time * self.fps)
        frame_number = max(0, min(frame_number, self.total_frames - 1))
        
        # Set video position to desired frame
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        
        # Read frame
        ret, frame = self.video_capture.read()
        if not ret:
            return None
        
        # Convert BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Resize if needed
        if self.scale != 1.0:
            new_width = int(self.original_width * self.scale)
            new_height = int(self.original_height * self.scale)
            frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
        
        # Add alpha channel
        alpha = np.full((frame.shape[0], frame.shape[1], 1), 255, dtype=np.uint8)
        frame = np.concatenate([frame, alpha], axis=2)
        
        # Convert to PIL Image for corner radius and border/background processing
        pil_frame = Image.fromarray(frame, 'RGBA')
        
        # Apply corner radius clipping to video frame
        pil_frame = self._apply_corner_radius_to_image(pil_frame)
        
        # Apply border and background
        pil_frame = self._apply_border_and_background_to_image(pil_frame)
        
        # Convert back to numpy array
        frame = np.array(pil_frame)
        
        # Flip vertically for OpenGL coordinate system
        frame = np.flipud(frame)
        
        return frame
    
    def set_scale(self, scale: float):
        """Set video scale"""
        self.scale = scale
        # Update texture dimensions (border/background will be applied at render time)
        if hasattr(self, 'original_width'):
            base_width = int(self.original_width * self.scale)
            base_height = int(self.original_height * self.scale)
            
            # Add padding to texture dimensions
            self.texture_width = base_width + self.padding['left'] + self.padding['right']
            self.texture_height = base_height + self.padding['top'] + self.padding['bottom']
        return self
    
    def render(self, time: float):
        """Render video frame"""
        if not self.is_visible_at(time):
            return
        
        if self.video_capture is None:
            return
        
        # Create texture if not yet created
        if not self.texture_created:
            self._create_texture_now()
        
        if self.texture_id is None:
            return
        
        # Calculate video time (time within the video clip)
        video_time = time - self.start_time
        
        # Get current frame
        frame_data = self._get_frame_at_time(video_time)
        if frame_data is None:
            return
        
        # Save current OpenGL state
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        
        # Update texture with current frame
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        
        # Upload frame data to texture (frame_data already includes border/background)
        actual_height, actual_width = frame_data.shape[:2]
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, actual_width, actual_height, 
                     0, GL_RGBA, GL_UNSIGNED_BYTE, frame_data)
        
        # Update texture dimensions with actual frame size
        self.texture_width = actual_width
        self.texture_height = actual_height
        
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
    
    def __del__(self):
        """Destructor to clean up resources"""
        if self.video_capture:
            self.video_capture.release()
        
        if self.texture_id:
            try:
                glDeleteTextures(1, [self.texture_id])
            except:
                pass