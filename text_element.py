import os
import numpy as np
from typing import Tuple
from OpenGL.GL import *
from PIL import Image, ImageDraw, ImageFont
from video_base import VideoBase


class TextElement(VideoBase):
    """テキスト要素"""
    def __init__(self, text: str, size: int = 50, color: Tuple[int, int, int] = (255, 255, 255), font_path: str = None):
        super().__init__()
        self.text = text
        self.size = size
        self.color = color
        self.font_path = font_path
        self.texture_id = None
        self.texture_width = 0
        self.texture_height = 0
        
        # 背景ボックス設定
        self.background_color = None
        self.background_alpha = 255
        self.padding = {'top': 0, 'right': 0, 'bottom': 0, 'left': 0}
        
        # 枠線設定
        self.border_color = None
        self.border_width = 0
        
        # 複数行・配置設定
        self.alignment = 'left'  # 'left', 'center', 'right'
        self.line_spacing = 0
        
        self._create_text_texture()
    
    def set_background(self, color: Tuple[int, int, int], alpha: int = 255, padding: int = 5):
        """背景色を設定"""
        self.background_color = color
        self.background_alpha = alpha
        if isinstance(padding, int):
            self.padding = {'top': padding, 'right': padding, 'bottom': padding, 'left': padding}
        elif isinstance(padding, dict):
            self.padding.update(padding)
        # テクスチャを再作成する必要がある
        self.texture_created = False
        return self
    
    def set_border(self, color: Tuple[int, int, int], width: int = 1):
        """枠線を設定"""
        self.border_color = color
        self.border_width = width
        # テクスチャを再作成する必要がある
        self.texture_created = False
        return self
    
    def set_alignment(self, alignment: str):
        """テキスト配置を設定 ('left', 'center', 'right')"""
        if alignment in ['left', 'center', 'right']:
            self.alignment = alignment
            # テクスチャを再作成する必要がある
            self.texture_created = False
        return self
    
    def set_line_spacing(self, spacing: int):
        """行間隔を設定"""
        self.line_spacing = spacing
        # テクスチャを再作成する必要がある
        self.texture_created = False
        return self
    
    def _create_text_texture(self):
        """テキストのテクスチャを作成"""
        # テクスチャ作成は後でrender時に行う（OpenGLコンテキストが必要なため）
        self.texture_created = False
    
    def _create_texture_now(self):
        """OpenGLコンテキスト内でテクスチャを作成"""
        try:
            # フォントを読み込み
            if self.font_path and os.path.exists(self.font_path):
                font = ImageFont.truetype(self.font_path, self.size)
            else:
                try:
                    font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", self.size)
                except:
                    try:
                        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", self.size)
                    except:
                        font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # 複数行テキストを分割
        lines = self.text.split('\n')
        
        # 各行のサイズを測定
        dummy_img = Image.new('RGBA', (1, 1))
        dummy_draw = ImageDraw.Draw(dummy_img)
        
        line_info = []
        max_width = 0
        total_height = 0
        
        for i, line in enumerate(lines):
            if line.strip():  # 空行でない場合
                bbox = dummy_draw.textbbox((0, 0), line, font=font)
                line_width = bbox[2] - bbox[0]
                line_height = bbox[3] - bbox[1]
                y_offset = -bbox[1]
            else:  # 空行の場合
                line_width = 0
                ascent, descent = font.getmetrics()
                line_height = ascent
                y_offset = 0
            
            line_info.append({
                'text': line,
                'width': line_width,
                'height': line_height,
                'y_offset': y_offset
            })
            
            max_width = max(max_width, line_width)
            total_height += line_height
            if i < len(lines) - 1:  # 最後の行でなければ行間を追加
                total_height += self.line_spacing
        
        # パディングを追加
        content_width = max_width
        content_height = total_height
        
        canvas_width = content_width + self.padding['left'] + self.padding['right']
        canvas_height = content_height + self.padding['top'] + self.padding['bottom']
        
        # 最小サイズを保証
        canvas_width = max(canvas_width, 1)
        canvas_height = max(canvas_height, 1)
        
        # テクスチャ用の画像を作成
        img = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # 背景ボックスを描画
        if self.background_color is not None:
            bg_color = (*self.background_color, self.background_alpha)
            draw.rectangle([0, 0, canvas_width-1, canvas_height-1], fill=bg_color)
        
        # テキストを描画
        current_y = self.padding['top']
        
        for line_data in line_info:
            if line_data['text'].strip():  # 空行でない場合のみ描画
                # 水平位置を計算（配置設定に基づく）
                if self.alignment == 'left':
                    x_pos = self.padding['left']
                elif self.alignment == 'center':
                    x_pos = self.padding['left'] + (content_width - line_data['width']) // 2
                else:  # right
                    x_pos = self.padding['left'] + content_width - line_data['width']
                
                # テキストを描画
                draw.text((x_pos, current_y + line_data['y_offset']), 
                         line_data['text'], 
                         font=font, 
                         fill=(*self.color, 255))
            
            # 次の行の位置を計算
            current_y += line_data['height'] + self.line_spacing
        
        # 枠線を描画
        if self.border_color is not None and self.border_width > 0:
            border_color = (*self.border_color, 255)
            for i in range(self.border_width):
                draw.rectangle([i, i, canvas_width-1-i, canvas_height-1-i], 
                             outline=border_color, width=1)
        
        # 実際のテクスチャサイズを更新
        self.texture_width = canvas_width
        self.texture_height = canvas_height
        
        # 画像をNumPy配列に変換
        img_data = np.array(img)
        
        # OpenGLテクスチャを生成
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        
        # テクスチャパラメータを設定
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        
        # テクスチャデータをアップロード
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.texture_width, self.texture_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        
        glBindTexture(GL_TEXTURE_2D, 0)
        self.texture_created = True

    def render(self, time: float):
        """テキストをレンダリング"""
        if not self.is_visible_at(time):
            return
        
        # テクスチャがまだ作成されていない場合は作成
        if not self.texture_created:
            self._create_texture_now()
        
        if self.texture_id is None:
            return
        
        # テクスチャを有効にする
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        
        # アルファブレンディングを有効にする
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # 白色でテクスチャを描画（テクスチャの色がそのまま使用される）
        glColor4f(1.0, 1.0, 1.0, 1.0)
        
        # テクスチャ付きの四角形を描画
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
        
        # テクスチャを無効にする
        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)
    
    def __del__(self):
        """デストラクタでテクスチャを削除"""
        if self.texture_id:
            try:
                glDeleteTextures(1, [self.texture_id])
            except:
                pass