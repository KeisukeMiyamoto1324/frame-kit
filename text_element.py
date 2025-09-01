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
        
        # 複数行・配置設定
        self.alignment = 'left'  # 'left', 'center', 'right'
        self.line_spacing = 0
        
        self._create_text_texture()
        # 初期化時にサイズを計算
        self.calculate_size()
    
    
    def set_alignment(self, alignment: str):
        """テキスト配置を設定 ('left', 'center', 'right')"""
        if alignment in ['left', 'center', 'right']:
            self.alignment = alignment
            # テクスチャを再作成する必要がある
            self.texture_created = False
            # サイズを再計算
            self.calculate_size()
        return self
    
    def set_line_spacing(self, spacing: int):
        """行間隔を設定"""
        self.line_spacing = spacing
        # テクスチャを再作成する必要がある
        self.texture_created = False
        # サイズを再計算
        self.calculate_size()
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
                line_height = font.getmetrics()[0]  # ascent only
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
        
        # テキスト用の画像を作成（パディングなし）
        content_width = max_width
        content_height = total_height
        
        # 最小サイズを保証
        content_width = max(content_width, 1)
        content_height = max(content_height, 1)
        
        # テキスト用の画像を作成
        img = Image.new('RGBA', (content_width, content_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # テキストを描画
        current_y = 0
        
        for line_data in line_info:
            if line_data['text'].strip():  # 空行でない場合のみ描画
                # 水平位置を計算（配置設定に基づく）
                if self.alignment == 'left':
                    x_pos = 0
                elif self.alignment == 'center':
                    x_pos = (content_width - line_data['width']) // 2
                else:  # right
                    x_pos = content_width - line_data['width']
                
                # テキストを描画
                draw.text((x_pos, current_y + line_data['y_offset']), 
                         line_data['text'], 
                         font=font, 
                         fill=(*self.color, 255))
            
            # 次の行の位置を計算
            current_y += line_data['height'] + self.line_spacing
        
        # 背景と枠線を適用
        img = self._apply_border_and_background_to_image(img)
        
        # 実際のテクスチャサイズを更新
        self.texture_width = img.size[0]
        self.texture_height = img.size[1]
        
        # ボックスサイズを更新（背景・枠線を含む最終サイズ）
        self.width = self.texture_width
        self.height = self.texture_height
        
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

    def calculate_size(self):
        """テキストのボックスサイズを事前計算"""
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
        
        max_width = 0
        total_height = 0
        
        for i, line in enumerate(lines):
            if line.strip():  # 空行でない場合
                bbox = dummy_draw.textbbox((0, 0), line, font=font)
                line_width = bbox[2] - bbox[0]
                line_height = bbox[3] - bbox[1]
            else:  # 空行の場合
                line_width = 0
                line_height = font.getmetrics()[0]  # ascent only
            
            max_width = max(max_width, line_width)
            total_height += line_height
            if i < len(lines) - 1:  # 最後の行でなければ行間を追加
                total_height += self.line_spacing
        
        # コンテンツサイズ
        content_width = max(max_width, 1)
        content_height = max(total_height, 1)
        
        # パディングを含むキャンバスサイズを計算
        canvas_width = content_width + self.padding['left'] + self.padding['right']
        canvas_height = content_height + self.padding['top'] + self.padding['bottom']
        
        # 最小サイズを保証
        canvas_width = max(canvas_width, 1)
        canvas_height = max(canvas_height, 1)
        
        # ボックスサイズを更新
        self.width = canvas_width
        self.height = canvas_height

    def render(self, time: float):
        """テキストをレンダリング"""
        if not self.is_visible_at(time):
            return
        
        # アニメーションプロパティを適用
        self.update_animated_properties(time)
        
        # テクスチャがまだ作成されていない場合は作成
        if not self.texture_created:
            self._create_texture_now()
        
        if self.texture_id is None:
            return
        
        # 変換行列を保存
        glPushMatrix()
        
        # 中心点を基準に変換を適用
        center_x = self.x + self.texture_width / 2
        center_y = self.y + self.texture_height / 2
        
        # 中心点に移動
        glTranslatef(center_x, center_y, 0)
        
        # 回転を適用
        if hasattr(self, 'rotation') and self.rotation != 0:
            glRotatef(self.rotation, 0, 0, 1)
        
        # スケールを適用
        if hasattr(self, 'scale') and self.scale != 1.0:
            glScalef(self.scale, self.scale, 1.0)
        
        # 中心点を戻す
        glTranslatef(-center_x, -center_y, 0)
        
        # テクスチャを有効にする
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        
        # アルファブレンディングを有効にする
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # アルファ値を適用（アニメーション考慮）
        alpha_value = 1.0
        if hasattr(self, 'background_alpha'):
            alpha_value = self.background_alpha / 255.0
        glColor4f(1.0, 1.0, 1.0, alpha_value)
        
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
        
        # 変換行列を復元
        glPopMatrix()
    
    def __del__(self):
        """デストラクタでテクスチャを削除"""
        if self.texture_id:
            try:
                glDeleteTextures(1, [self.texture_id])
            except:
                pass