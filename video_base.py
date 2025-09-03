import os
import numpy as np
from typing import List, Optional, Tuple, Any, Literal
from PIL import Image, ImageDraw, ImageFont
from animation import Animation, AnimationManager, RepeatingAnimation


class VideoBase:
    """動画要素の基底クラス"""
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.start_time = 0.0
        self.duration = 1.0
        self.visible = True
        
        # 位置アンカー設定
        self.position_anchor = 'top-left'  # 'center', 'top-left', 'top-right', 'bottom-left', 'bottom-right'
        
        # 背景ボックス設定
        self.background_color = None
        self.background_alpha = 255
        self.padding = {'top': 0, 'right': 0, 'bottom': 0, 'left': 0}
        
        # 枠線設定
        self.border_color = None
        self.border_width = 0
        
        # 角丸設定
        self.corner_radius = 0
        
        # クロップ設定
        self.crop_width = None
        self.crop_height = None
        self.crop_mode = 'fill'  # 'fill' or 'fit'
        
        # ボックスサイズ（背景・枠線を含む最終的なサイズ）
        self.width = 0
        self.height = 0
        
        # テクスチャ再作成フラグ
        self.texture_created = False
        
        # アニメーション関連
        self.animation_manager = AnimationManager()
        self.base_x = 0.0  # アニメーション前の基本位置
        self.base_y = 0.0
        self.base_alpha = 255  # アニメーション前の基本透明度
        self.base_scale = 1.0  # アニメーション前の基本スケール
        self.rotation = 0.0  # 回転角度（度）
        self.scale = 1.0  # スケール値
    
    def position(self, x: float, y: float, anchor: Optional[Literal['center', 'top-left', 'top-right', 'bottom-left', 'bottom-right']] = None):
        """位置を設定
        
        Args:
            x: X座標
            y: Y座標
            anchor: 位置の基準点 ('center', 'top-left', 'top-right', 'bottom-left', 'bottom-right')
                   Noneの場合は現在の設定を維持
        """
        if anchor is not None:
            self.position_anchor = anchor
        
        self.x = x
        self.y = y
        self.base_x = x  # アニメーション用の基本位置も更新
        self.base_y = y
        return self
    
    def _calculate_anchor_offset(self, element_width: float, element_height: float) -> Tuple[float, float]:
        """アンカーに基づく位置オフセットを計算
        
        Args:
            element_width: 要素の幅
            element_height: 要素の高さ
            
        Returns:
            (offset_x, offset_y): アンカーに基づくオフセット
        """
        if self.position_anchor == 'center':
            return -element_width / 2, -element_height / 2
        elif self.position_anchor == 'top-right':
            return -element_width, 0
        elif self.position_anchor == 'bottom-left':
            return 0, -element_height
        elif self.position_anchor == 'bottom-right':
            return -element_width, -element_height
        else:  # 'top-left' (default)
            return 0, 0
    
    def get_actual_render_position(self):
        """レンダリング時の実際の位置とサイズを取得（スケール等を考慮）"""
        element_width = getattr(self, 'width', 0)
        element_height = getattr(self, 'height', 0)
        
        # アンカーに基づく位置オフセットを計算
        offset_x, offset_y = self._calculate_anchor_offset(element_width, element_height)
        
        # 実際の描画位置を計算
        actual_x = self.x + offset_x
        actual_y = self.y + offset_y
        
        return actual_x, actual_y, element_width, element_height
    
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
    
    def set_crop(self, width: int, height: int, mode: str = 'fill'):
        """クロップサイズとモードを設定
        
        Args:
            width: クロップ後の幅
            height: クロップ後の高さ  
            mode: 'fill' (はみ出し部分をクロップ) or 'fit' (全体を収める)
        """
        self.crop_width = width
        self.crop_height = height
        self.crop_mode = mode
        # テクスチャを再作成する必要がある
        self.texture_created = False
        # サイズを再計算
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
    
    def _calculate_crop_dimensions(self, original_width: int, original_height: int) -> Tuple[int, int, int, int]:
        """クロップのスケールと位置を計算
        
        Returns:
            (scaled_width, scaled_height, crop_x, crop_y)
        """
        if self.crop_width is None or self.crop_height is None:
            return original_width, original_height, 0, 0
        
        target_width = self.crop_width
        target_height = self.crop_height
        
        if self.crop_mode == 'fill':
            # アスペクト比を維持して、指定サイズを完全に埋める（はみ出し部分をクロップ）
            scale = max(target_width / original_width, target_height / original_height)
        else:  # fit
            # アスペクト比を維持して、指定サイズに収まる最大サイズ
            scale = min(target_width / original_width, target_height / original_height)
        
        # スケール後のサイズ
        scaled_width = int(original_width * scale)
        scaled_height = int(original_height * scale)
        
        # クロップ位置を計算（中央クロップ）
        crop_x = max(0, (scaled_width - target_width) // 2)
        crop_y = max(0, (scaled_height - target_height) // 2)
        
        return scaled_width, scaled_height, crop_x, crop_y
    
    def _apply_crop_to_image(self, img: Image.Image) -> Image.Image:
        """画像にクロップを適用
        
        Args:
            img: 元の画像
            
        Returns:
            クロップされた画像
        """
        if self.crop_width is None or self.crop_height is None:
            return img
        
        original_width, original_height = img.size
        scaled_width, scaled_height, crop_x, crop_y = self._calculate_crop_dimensions(original_width, original_height)
        
        # まずスケールを適用
        if scaled_width != original_width or scaled_height != original_height:
            img = img.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)
        
        # クロップを適用
        if self.crop_mode == 'fill':
            # fillモード: 指定サイズでクロップ
            crop_box = (crop_x, crop_y, crop_x + self.crop_width, crop_y + self.crop_height)
            img = img.crop(crop_box)
        else:  # fit
            # fitモード: 新しいキャンバスを作成して中央に配置
            canvas = Image.new('RGBA', (self.crop_width, self.crop_height), (0, 0, 0, 0))
            paste_x = (self.crop_width - scaled_width) // 2
            paste_y = (self.crop_height - scaled_height) // 2
            canvas.paste(img, (paste_x, paste_y), img)
            img = canvas
        
        return img

    def animate(self, property_name: str, animation: Animation):
        """プロパティにアニメーションを追加"""
        # アニメーションの開始時刻を要素の開始時刻に対して相対的に設定
        animation.start_time += self.start_time
        self.animation_manager.add_animation(property_name, animation)
        return self
    
    def animate_position(self, animation: Animation, axis: str = 'both'):
        """位置のアニメーション（便利メソッド）
        
        Args:
            animation: 使用するアニメーション
            axis: アニメーションする軸 ('x', 'y', 'both')
        """
        if axis in ['x', 'both']:
            self.animate('x', animation)
        if axis in ['y', 'both']:
            self.animate('y', animation) 
        return self
    
    def animate_fade(self, animation: Animation):
        """透明度のアニメーション（便利メソッド）"""
        self.animate('alpha', animation)
        return self
    
    def animate_scale(self, animation: Animation):
        """スケールのアニメーション（便利メソッド）"""
        self.animate('scale', animation)
        return self
    
    def animate_rotation(self, animation: Animation):
        """回転のアニメーション（便利メソッド）"""
        self.animate('rotation', animation)
        return self
    
    def animate_repeating(self, property_name: str, animation: Animation, 
                         repeat_count: int = -1, repeat_delay: float = 0.0, 
                         repeat_mode: str = 'restart'):
        """プロパティに繰り返しアニメーションを追加
        
        Args:
            property_name: アニメーションするプロパティ名
            animation: 繰り返すベースアニメーション
            repeat_count: 繰り返し回数（-1で無限）
            repeat_delay: 各繰り返し間の遅延時間（秒）
            repeat_mode: 繰り返しモード ('restart', 'reverse', 'continue')
        """
        repeating_animation = RepeatingAnimation(
            base_animation=animation,
            repeat_count=repeat_count,
            repeat_delay=repeat_delay,
            repeat_mode=repeat_mode
        )
        repeating_animation.start_time += self.start_time
        self.animation_manager.add_animation(property_name, repeating_animation)
        return self
    
    def animate_until_scene_end(self, property_name: str, animation: Animation, 
                               repeat_delay: float = 0.0, repeat_mode: str = 'restart',
                               scene_duration: float = None):
        """プロパティにシーン終了まで繰り返すアニメーションを追加
        
        Args:
            property_name: アニメーションするプロパティ名
            animation: 繰り返すベースアニメーション
            repeat_delay: 各繰り返し間の遅延時間（秒）
            repeat_mode: 繰り返しモード ('restart', 'reverse', 'continue')
            scene_duration: シーンの継続時間（Noneの場合は自動検出を試行）
        """
        # シーン継続時間を推定（実際の実装では親シーンから取得すべき）
        if scene_duration is None:
            scene_duration = self.duration  # 暫定的に要素の継続時間を使用
        
        repeating_animation = RepeatingAnimation(
            base_animation=animation,
            repeat_count=-1,
            repeat_delay=repeat_delay,
            repeat_mode=repeat_mode,
            until_scene_end=True,
            scene_duration=scene_duration
        )
        repeating_animation.start_time += self.start_time
        self.animation_manager.add_animation(property_name, repeating_animation)
        return self
    
    # 繰り返しアニメーション用の便利メソッド
    def animate_repeating_scale(self, animation: Animation, repeat_count: int = -1, 
                               repeat_delay: float = 0.0, repeat_mode: str = 'restart'):
        """スケールの繰り返しアニメーション（便利メソッド）"""
        return self.animate_repeating('scale', animation, repeat_count, repeat_delay, repeat_mode)
    
    def animate_repeating_position(self, animation: Animation, axis: str = 'both',
                                  repeat_count: int = -1, repeat_delay: float = 0.0, 
                                  repeat_mode: str = 'restart'):
        """位置の繰り返しアニメーション（便利メソッド）"""
        if axis in ['x', 'both']:
            self.animate_repeating('x', animation, repeat_count, repeat_delay, repeat_mode)
        if axis in ['y', 'both']:
            self.animate_repeating('y', animation, repeat_count, repeat_delay, repeat_mode)
        return self
    
    def animate_repeating_rotation(self, animation: Animation, repeat_count: int = -1,
                                  repeat_delay: float = 0.0, repeat_mode: str = 'restart'):
        """回転の繰り返しアニメーション（便利メソッド）"""
        return self.animate_repeating('rotation', animation, repeat_count, repeat_delay, repeat_mode)
    
    def animate_pulse_until_end(self, from_scale: float = 1.0, to_scale: float = 1.2,
                               duration: float = 1.0, repeat_delay: float = 0.0,
                               scene_duration: float = None):
        """パルス（鼓動）アニメーションをシーン終了まで繰り返す（便利メソッド）"""
        from animation import AnimationPresets
        pulse_animation = AnimationPresets.pulse(from_scale, to_scale, duration)
        return self.animate_until_scene_end('scale', pulse_animation, repeat_delay, 
                                          'restart', scene_duration)
    
    def animate_breathing_until_end(self, from_scale: float = 1.0, to_scale: float = 1.1,
                                   duration: float = 3.0, repeat_delay: float = 0.0,
                                   scene_duration: float = None):
        """呼吸のような拡大縮小をシーン終了まで繰り返す（便利メソッド）"""
        from animation import AnimationPresets
        breathing_animation = AnimationPresets.breathing(from_scale, to_scale, duration)
        return self.animate_until_scene_end('scale', breathing_animation, repeat_delay,
                                          'restart', scene_duration)
    
    def get_animated_properties(self, time: float):
        """現在時刻でのアニメーション適用後のプロパティを取得"""
        properties = {}
        
        # 位置のアニメーション
        animated_x = self.animation_manager.get_animated_value('x', time, self.base_x)
        animated_y = self.animation_manager.get_animated_value('y', time, self.base_y)
        if animated_x is not None:
            properties['x'] = animated_x
        if animated_y is not None:
            properties['y'] = animated_y
            
        # 透明度のアニメーション
        animated_alpha = self.animation_manager.get_animated_value('alpha', time, self.base_alpha)
        if animated_alpha is not None:
            properties['alpha'] = max(0, min(255, int(animated_alpha)))
            
        # スケールのアニメーション
        animated_scale = self.animation_manager.get_animated_value('scale', time, self.base_scale)
        if animated_scale is not None:
            properties['scale'] = max(0.0, animated_scale)
            
        # 回転のアニメーション
        animated_rotation = self.animation_manager.get_animated_value('rotation', time, self.rotation)
        if animated_rotation is not None:
            properties['rotation'] = animated_rotation
            
        # 色のアニメーション（背景色）
        if hasattr(self, 'color') and self.animation_manager.get_animated_value('color', time) is not None:
            animated_color = self.animation_manager.get_animated_value('color', time, getattr(self, 'color', (255, 255, 255)))
            properties['color'] = animated_color
            
        # 角丸半径のアニメーション
        animated_corner_radius = self.animation_manager.get_animated_value('corner_radius', time, self.corner_radius)
        if animated_corner_radius is not None:
            properties['corner_radius'] = max(0, animated_corner_radius)
            
        return properties
    
    def update_animated_properties(self, time: float):
        """アニメーションプロパティを現在の状態に適用"""
        animated_props = self.get_animated_properties(time)
        
        if 'x' in animated_props:
            self.x = animated_props['x']
        if 'y' in animated_props:
            self.y = animated_props['y']
        if 'alpha' in animated_props:
            self.background_alpha = animated_props['alpha']
        if 'scale' in animated_props:
            self.scale = animated_props['scale']
        if 'rotation' in animated_props:
            self.rotation = animated_props['rotation']
        if 'corner_radius' in animated_props:
            self.corner_radius = animated_props['corner_radius']
    
    def has_animations(self, time: float = None) -> bool:
        """アニメーションを持っているかチェック"""
        if time is not None:
            return self.animation_manager.has_active_animations(time)
        return len(self.animation_manager.animations) > 0

    def calculate_size(self):
        """ボックスサイズを事前計算（サブクラスでオーバーライド）"""
        pass

    def render(self, time: float):
        """要素をレンダリング（サブクラスで実装）"""
        # アニメーションプロパティを適用
        self.update_animated_properties(time)
        pass