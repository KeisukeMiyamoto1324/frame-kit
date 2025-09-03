import os
import cv2
import numpy as np
from OpenGL.GL import *
from PIL import Image
from video_base import VideoBase
from audio_element import AudioElement


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
        self.audio_element = None
        self.loop_until_scene_end = False
        self.original_duration = 0.0
        self._create_video_texture()
        # 初期化時にサイズを計算
        self.calculate_size()
        # オーディオ要素を作成（遅延作成）
        self.audio_element = None
        self._audio_element_created = False
    
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
            
            # Set duration to video length
            if self.fps > 0 and self.total_frames > 0:
                video_duration = self.total_frames / self.fps
                self.duration = video_duration
                self.original_duration = video_duration
            
            print(f"Video loaded: {self.original_width}x{self.original_height}, {self.fps} fps, {self.total_frames} frames, duration: {self.duration:.2f}s")
            
        except Exception as e:
            print(f"Error loading video info {self.video_path}: {e}")
    
    def _create_audio_element(self):
        """Create audio element from video file"""
        if self._audio_element_created:
            return
            
        try:
            # VideoElementと同じタイミングでオーディオを再生するようにAudioElementを作成
            self.audio_element = AudioElement(self.video_path, volume=1.0)
            # VideoElementと同じstart_timeとdurationを設定
            self._sync_audio_timing()
            self._audio_element_created = True
            print(f"Audio element created for video: {self.video_path}")
        except Exception as e:
            print(f"Warning: Could not create audio element for {self.video_path}: {e}")
            self.audio_element = None
    
    def _sync_audio_timing(self):
        """Synchronize audio element timing with video element"""
        if self.audio_element:
            print(f"Syncing audio timing: start_time={self.start_time}, duration={self.duration}")
            self.audio_element.start_at(self.start_time)
            self.audio_element.set_duration(self.duration)
            print(f"Audio element timing set: start_time={self.audio_element.start_time}, duration={self.audio_element.duration}")
    
    def get_audio_element(self):
        """Get the associated audio element"""
        return self.audio_element
    
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
        
        # Convert to PIL Image for crop and corner radius and border/background processing
        pil_frame = Image.fromarray(frame, 'RGBA')
        
        # Apply crop if specified
        pil_frame = self._apply_crop_to_image(pil_frame)
        
        # Apply corner radius clipping to video frame
        pil_frame = self._apply_corner_radius_to_image(pil_frame)
        
        # Apply border and background
        pil_frame = self._apply_border_and_background_to_image(pil_frame)
        
        # ボックスサイズを更新（背景・枠線を含む最終サイズ）
        self.width = pil_frame.size[0]
        self.height = pil_frame.size[1]
        
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
            
            # ボックスサイズも更新（推定値、実際は描画時に正確な値が設定される）
            border_size = self.border_width * 2 if self.border_color else 0
            self.width = self.texture_width + border_size
            self.height = self.texture_height + border_size
        return self
    
    def start_at(self, start_time: float):
        """Set start time and update audio element timing"""
        super().start_at(start_time)
        self._ensure_audio_element()
        self._sync_audio_timing()
        return self
    
    def set_duration(self, duration: float):
        """Set duration and update audio element timing"""
        super().set_duration(duration)
        self._ensure_audio_element()
        self._sync_audio_timing()
        return self
    
    def _ensure_audio_element(self):
        """Ensure audio element is created before using it"""
        if not self._audio_element_created:
            self._create_audio_element()
    
    def set_volume(self, volume: float):
        """Set audio volume (0.0 to 1.0)"""
        self._ensure_audio_element()
        if self.audio_element:
            self.audio_element.set_volume(volume)
        return self
    
    def set_audio_fade_in(self, duration: float):
        """Set audio fade in duration"""
        self._ensure_audio_element()
        if self.audio_element:
            self.audio_element.set_fade_in(duration)
        return self
    
    def set_audio_fade_out(self, duration: float):
        """Set audio fade out duration"""
        self._ensure_audio_element()
        if self.audio_element:
            self.audio_element.set_fade_out(duration)
        return self
    
    def mute_audio(self):
        """Mute video audio"""
        self._ensure_audio_element()
        if self.audio_element:
            self.audio_element.mute()
        return self
    
    def unmute_audio(self):
        """Unmute video audio"""
        self._ensure_audio_element()
        if self.audio_element:
            self.audio_element.unmute()
        return self
    
    def get_audio_volume(self):
        """Get current audio volume"""
        self._ensure_audio_element()
        if self.audio_element:
            return self.audio_element.volume
        return 0.0
    
    def set_loop_until_scene_end(self, loop: bool = True):
        """Set whether to loop video until scene/master scene ends"""
        self.loop_until_scene_end = loop
        if loop:
            print(f"Video loop mode enabled for: {self.video_path}")
        return self
    
    def update_duration_for_scene(self, scene_duration: float):
        """Update duration to match scene duration when in loop mode"""
        if self.loop_until_scene_end:
            # ビデオはシーンの長さに合わせて調整（ループまたは強制終了）
            if scene_duration > 0:  # シーンに他の要素がある場合のみ
                self.duration = scene_duration
                if scene_duration > self.original_duration:
                    print(f"Video will loop: original {self.original_duration:.2f}s → extended to {scene_duration:.2f}s")
                elif scene_duration < self.original_duration:
                    print(f"Video will be cut: original {self.original_duration:.2f}s → cut to {scene_duration:.2f}s")
                else:
                    print(f"Video duration matches scene: {scene_duration:.2f}s")
                
                # オーディオ要素も同期
                self._ensure_audio_element()
                if self.audio_element and hasattr(self.audio_element, 'update_duration_for_scene'):
                    self.audio_element.update_duration_for_scene(scene_duration)
    
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
        
        # Handle looping if enabled
        if self.loop_until_scene_end and video_time >= self.original_duration:
            video_time = video_time % self.original_duration
        
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
        
        # Get actual render position using anchor calculation
        # Temporarily set the current size for anchor calculation
        original_width, original_height = self.width, self.height
        self.width, self.height = actual_width, actual_height
        
        render_x, render_y, _, _ = self.get_actual_render_position()
        
        # Restore original size
        self.width, self.height = original_width, original_height
        
        # Enable alpha blending
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Set texture environment to replace (preserves texture colors)
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        
        # Draw textured quad with corrected texture coordinates
        glBegin(GL_QUADS)
        # Bottom-left
        glTexCoord2f(0.0, 0.0)
        glVertex2f(render_x, render_y + self.texture_height)
        
        # Bottom-right
        glTexCoord2f(1.0, 0.0)
        glVertex2f(render_x + self.texture_width, render_y + self.texture_height)
        
        # Top-right
        glTexCoord2f(1.0, 1.0)
        glVertex2f(render_x + self.texture_width, render_y)
        
        # Top-left
        glTexCoord2f(0.0, 1.0)
        glVertex2f(render_x, render_y)
        glEnd()
        
        # Restore OpenGL state
        glPopAttrib()

    def calculate_size(self):
        """動画のボックスサイズを事前計算"""
        if not hasattr(self, 'original_width') or self.original_width == 0:
            self.width = 0
            self.height = 0
            return
        
        # スケールを適用
        scaled_width = int(self.original_width * self.scale)
        scaled_height = int(self.original_height * self.scale)
        
        # クロップが設定されている場合はクロップサイズを使用
        if self.crop_width is not None and self.crop_height is not None:
            content_width = self.crop_width
            content_height = self.crop_height
        else:
            content_width = scaled_width
            content_height = scaled_height
        
        # パディングを含むキャンバスサイズを計算
        canvas_width = content_width + self.padding['left'] + self.padding['right']
        canvas_height = content_height + self.padding['top'] + self.padding['bottom']
        
        # 最小サイズを保証
        canvas_width = max(canvas_width, 1)
        canvas_height = max(canvas_height, 1)
        
        # ボックスサイズを更新
        self.width = canvas_width
        self.height = canvas_height
    
    def __del__(self):
        """Destructor to clean up resources"""
        if self.video_capture:
            self.video_capture.release()
        
        if self.texture_id:
            try:
                glDeleteTextures(1, [self.texture_id])
            except:
                pass