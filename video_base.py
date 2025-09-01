import os
import numpy as np
from typing import List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont


class VideoBase:
    """動画要素の基底クラス"""
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.start_time = 0.0
        self.duration = 1.0
        self.visible = True
        
        # 背景ボックス設定
        self.background_color = None
        self.background_alpha = 255
        self.padding = {'top': 0, 'right': 0, 'bottom': 0, 'left': 0}
        
        # 枠線設定
        self.border_color = None
        self.border_width = 0
        
        # 角丸設定
        self.corner_radius = 0
        
        # ボックスサイズ（背景・枠線を含む最終的なサイズ）
        self.width = 0
        self.height = 0
        
        # テクスチャ再作成フラグ
        self.texture_created = False
    
    def position(self, x: float, y: float):
        """位置を設定"""
        self.x = x
        self.y = y
        return self
    
    def set_duration(self, duration: float):
        """表示時間を設定"""
        self.duration = duration
        return self
    
    def start_at(self, time: float):
        """開始時間を設定"""
        self.start_time = time
        return self
    
    def is_visible_at(self, time: float) -> bool:
        """指定時間に表示されるかチェック"""
        return self.start_time <= time < (self.start_time + self.duration)
    
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
        # サイズを再計算
        self.calculate_size()
        return self
    
    def set_border(self, color: Tuple[int, int, int], width: int = 1):
        """枠線を設定"""
        self.border_color = color
        self.border_width = width
        # テクスチャを再作成する必要がある
        self.texture_created = False
        # サイズを再計算
        self.calculate_size()
        return self
    
    def set_corner_radius(self, radius: float):
        """角丸半径を設定"""
        self.corner_radius = max(0, radius)  # 負の値は0に補正
        # テクスチャを再作成する必要がある
        self.texture_created = False
        # サイズを再計算（角丸は通常サイズに影響しないが、将来の拡張のため）
        self.calculate_size()
        return self

    def _apply_border_and_background_to_image(self, img: Image.Image) -> Image.Image:
        """画像に背景と枠線を適用するヘルパーメソッド"""
        # 元の画像サイズを取得
        original_width, original_height = img.size
        
        # パディングを含むキャンバスサイズを計算
        canvas_width = original_width + self.padding['left'] + self.padding['right']
        canvas_height = original_height + self.padding['top'] + self.padding['bottom']
        
        # 最小サイズを保証
        canvas_width = max(canvas_width, 1)
        canvas_height = max(canvas_height, 1)
        
        # キャンバス用の画像を作成
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        canvas = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
        
        # 背景ボックスを描画
        if self.background_color is not None:
            draw = ImageDraw.Draw(canvas)
            bg_color = (*self.background_color, self.background_alpha)
            
            if self.corner_radius > 0:
                # 角丸背景を描画
                draw.rounded_rectangle([0, 0, canvas_width-1, canvas_height-1], 
                                     radius=self.corner_radius, fill=bg_color)
            else:
                # 通常の四角形背景を描画
                draw.rectangle([0, 0, canvas_width-1, canvas_height-1], fill=bg_color)
        
        # 元の画像をパディング位置に合成
        canvas.paste(img, (self.padding['left'], self.padding['top']), img)
        
        # 枠線を描画
        if self.border_color is not None and self.border_width > 0:
            draw = ImageDraw.Draw(canvas)
            border_color = (*self.border_color, 255)
            
            if self.corner_radius > 0:
                # 角丸枠線を描画
                for i in range(self.border_width):
                    # 内側に向かって角丸半径を調整
                    current_radius = max(0, self.corner_radius - i)
                    draw.rounded_rectangle([i, i, canvas_width-1-i, canvas_height-1-i], 
                                         radius=current_radius, outline=border_color, width=1)
            else:
                # 通常の四角形枠線を描画
                for i in range(self.border_width):
                    draw.rectangle([i, i, canvas_width-1-i, canvas_height-1-i], 
                                 outline=border_color, width=1)
        
        return canvas
    
    def _apply_corner_radius_to_image(self, img: Image.Image) -> Image.Image:
        """画像コンテンツ自体に角丸クリッピングを適用"""
        if self.corner_radius <= 0:
            return img
        
        # 画像サイズを取得
        width, height = img.size
        
        # 角丸半径がサイズより大きい場合は調整
        radius = min(self.corner_radius, width // 2, height // 2)
        
        # 角丸マスクを作成
        mask = Image.new('L', (width, height), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, width, height], radius=radius, fill=255)
        
        # RGBAモードに変換
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # マスクを適用して角丸にクリッピング
        img.putalpha(mask)
        
        return img

    def calculate_size(self):
        """ボックスサイズを事前計算（サブクラスでオーバーライド）"""
        pass

    def render(self, time: float):
        """要素をレンダリング（サブクラスで実装）"""
        pass