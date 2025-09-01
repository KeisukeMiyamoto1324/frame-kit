import os
import numpy as np
from typing import Tuple
from OpenGL.GL import *
from PIL import Image
from video_element import VideoElement


class ImageElement(VideoElement):
    """;œÅ """
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
    
    def _create_image_texture(self):
        """;œn∆Øπ¡„í\"""
        # ∆Øπ¡„\oågrenderBkLFOpenGL≥Û∆≠π»L≈Åj_Å	
        self.texture_created = False
    
    def _create_texture_now(self):
        """OpenGL≥Û∆≠π»Ög∆Øπ¡„í\"""
        if not os.path.exists(self.image_path):
            print(f"Warning: Image file not found: {self.image_path}")
            return
        
        try:
            # ;œí≠º
            img = Image.open(self.image_path)
            
            # RGBAbk	€¢Î’°¡„ÛÕÎ˛‹	
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Cnµ§∫í›X
            self.original_width, self.original_height = img.size
            
            # π±¸ÍÛ∞i(
            if self.scale != 1.0:
                new_width = int(self.original_width * self.scale)
                new_height = int(self.original_height * self.scale)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # ∆Øπ¡„µ§∫íÙ∞
            self.texture_width, self.texture_height = img.size
            
            # ;œíNumPyMk	€
            img_data = np.array(img)
            
            # OpenGL∆Øπ¡„í
            self.texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            
            # ∆Øπ¡„—È·¸øí-ö
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            
            # ∆Øπ¡„«¸øí¢√◊Ì¸…
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.texture_width, self.texture_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
            
            glBindTexture(GL_TEXTURE_2D, 0)
            self.texture_created = True
            
        except Exception as e:
            print(f"Error loading image {self.image_path}: {e}")
            self.texture_created = False
    
    def set_scale(self, scale: float):
        """π±¸Îí-ö"""
        self.scale = scale
        # ∆Øπ¡„nç\L≈Å
        if self.texture_created:
            self.texture_created = False
        return self
    
    def render(self, time: float):
        """;œíÏÛ¿ÍÛ∞"""
        if not self.is_visible_at(time):
            return
        
        # ∆Øπ¡„L~`\UåfDjD4o\
        if not self.texture_created:
            self._create_texture_now()
        
        if self.texture_id is None:
            return
        
        # ∆Øπ¡„í	πkYã
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        
        # ¢Î’°÷ÏÛ«£Û∞í	πkYã
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # }rg∆Øπ¡„íœ;∆Øπ¡„nrL]n~~(Uåã	
        glColor4f(1.0, 1.0, 1.0, 1.0)
        
        # ∆Øπ¡„ÿMn€“bíœ;
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(self.x, self.y)
        
        glTexCoord2f(1.0, 0.0)
        glVertex2f(self.x + self.texture_width, self.y)
        
        glTexCoord2f(1.0, 1.0)
        glVertex2f(self.x + self.texture_width, self.y + self.texture_height)
        
        glTexCoord2f(0.0, 1.0)
        glVertex2f(self.x, self.y + self.texture_height)
        glEnd()
        
        # ∆Øπ¡„í!πkYã
        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)
    
    def __del__(self):
        """«π»ÈØøg∆Øπ¡„íJd"""
        if self.texture_id:
            try:
                glDeleteTextures(1, [self.texture_id])
            except:
                pass