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
        self._create_text_texture()
    
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
        
        # テキストのサイズを測定（より正確な方法）
        dummy_img = Image.new('RGBA', (1, 1))
        dummy_draw = ImageDraw.Draw(dummy_img)
        
        # テキストのバウンディングボックスを取得
        bbox = dummy_draw.textbbox((0, 0), self.text, font=font)
        text_width = max(bbox[2] - bbox[0], 1)
        text_height = max(bbox[3] - bbox[1], 1)
        
        # フォントのアセント/ディセントを考慮してパディングを追加
        ascent, descent = font.getmetrics()
        total_height = ascent + descent
        y_offset = -bbox[1]  # テキストの上端を0に合わせる
        
        # より大きめのキャンバスを作成（パディング込み）
        canvas_width = text_width + 10  # 左右に5pxずつパディング
        canvas_height = max(total_height, text_height) + 10  # 上下に5pxずつパディング
        
        # テクスチャ用の画像を作成
        img = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # テキストを中央に描画（パディングを考慮）
        draw.text((5, 5 + y_offset), self.text, font=font, fill=(*self.color, 255))
        
        # 実際のテクスチャサイズを更新
        text_width = canvas_width
        text_height = canvas_height
        
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
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_width, text_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        
        self.texture_width = text_width
        self.texture_height = text_height
        
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