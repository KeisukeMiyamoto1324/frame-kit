import os, sys
import warnings

# Pygame関連の環境変数を事前に設定
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# pkg_resources警告を抑制
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*pkg_resources.*")

# 親ディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from master_scene import MasterScene
from scene import Scene
from text_element import TextElement
from image_element import ImageElement
from animation import (
    LinearAnimation, EaseInAnimation, EaseOutAnimation, EaseInOutAnimation,
    BounceAnimation, SpringAnimation, KeyframeAnimation, ColorAnimation,
    AnimationPresets
)


def main():
    """高度なアニメーション機能のテスト"""
    # Create master scene
    master_scene = MasterScene(width=1920, height=1080, fps=30)
    master_scene.set_output("animation_advanced_test.mp4")
    
    # Create scene
    scene = Scene()
    
    # Test 1: 波のようなテキスト登場
    wave_texts = []
    wave_text_content = "WAVE ANIMATION"
    for i, char in enumerate(wave_text_content):
        if char != ' ':  # スペースはスキップ
            char_text = (
                TextElement(char, size=120, color=(255, 100 + i * 10, 255 - i * 10))
                    .position(200 + i * 80, 200)
                    .set_duration(12)
                    .start_at(0)
                    .animate('y', KeyframeAnimation({
                        0.0: 800,
                        0.4: 100,
                        0.7: 150,
                        1.0: 200
                    }, duration=2.0, delay=i * 0.1, interpolation='ease_out'))
                    .animate_scale(SpringAnimation(from_value=0.1, to_value=1.0, 
                                                 duration=1.5, delay=i * 0.1))
            )
            scene.add(char_text)
    
    # Test 2: 螺旋軌道アニメーション
    spiral_text = (
        TextElement("Spiral Path", size=60, color=(0, 255, 255))
            .position(960, 540)  # 中心位置
            .set_duration(15)
            .start_at(2)
    )
    
    # 螺旋軌道のキーフレームを生成
    import math
    spiral_keyframes_x = {}
    spiral_keyframes_y = {}
    center_x, center_y = 960, 540
    
    for i in range(21):  # 20分割
        t = i / 20.0
        angle = t * 4 * math.pi  # 2回転
        radius = 200 * (1 - t)  # 徐々に小さくなる半径
        
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        
        spiral_keyframes_x[t] = x
        spiral_keyframes_y[t] = y
    
    spiral_text.animate('x', KeyframeAnimation(spiral_keyframes_x, duration=6.0, delay=1.0))
    spiral_text.animate('y', KeyframeAnimation(spiral_keyframes_y, duration=6.0, delay=1.0))
    spiral_text.animate_rotation(LinearAnimation(from_value=0, to_value=720, duration=6.0, delay=1.0))
    scene.add(spiral_text)
    
    # Test 3: エラスティック（弾性）アニメーション
    elastic_text = (
        TextElement("Elastic Motion", size=80, color=(255, 255, 0))
            .position(1400, 300)
            .set_duration(10)
            .start_at(4)
            .animate('x', SpringAnimation(from_value=0, to_value=1400, 
                                        duration=3.0, delay=0.5, 
                                        stiffness=0.3, damping=0.6))
            .animate_scale(SpringAnimation(from_value=2.0, to_value=1.0, 
                                         duration=2.5, delay=0.8))
    )
    scene.add(elastic_text)
    
    # Test 4: 段階的フェード（連鎖アニメーション）
    cascade_texts = []
    cascade_phrases = ["Cascading", "Animation", "Effect", "Demo"]
    for i, phrase in enumerate(cascade_phrases):
        cascade_text = (
            TextElement(phrase, size=70, color=(255, 150, 50))
                .position(300, 600 + i * 100)
                .set_duration(12)
                .start_at(6)
                .animate_fade(LinearAnimation(from_value=0, to_value=255, 
                                           duration=1.0, delay=i * 0.3))
                .animate('x', EaseOutAnimation(from_value=-200, to_value=300,
                                             duration=1.5, delay=i * 0.3))
        )
        scene.add(cascade_text)
    
    # Test 5: パルス（鼓動）アニメーション
    pulse_text = (
        TextElement("Pulsing Heart", size=90, color=(255, 50, 50))
            .position(700, 800)
            .set_duration(15)
            .start_at(8)
    )
    
    # パルスのキーフレーム
    pulse_keyframes = {
        0.0: 1.0,
        0.1: 1.3,
        0.2: 1.0,
        0.3: 1.2,
        0.4: 1.0,
        0.6: 1.0,
        1.0: 1.0
    }
    
    pulse_text.animate_scale(KeyframeAnimation(pulse_keyframes, duration=1.5, delay=0.0))
    # パルスを繰り返すために複数のアニメーションを追加
    for repeat in range(1, 5):
        pulse_text.animate_scale(KeyframeAnimation(pulse_keyframes, 
                                                 duration=1.5, delay=repeat * 1.8))
    scene.add(pulse_text)
    
    # Test 6: 3D回転風アニメーション
    rotation_3d_text = (
        TextElement("3D-Style Rotation", size=80, color=(100, 255, 100))
            .position(1200, 700)
            .set_duration(12)
            .start_at(10)
    )
    
    # 3D回転を模擬するためのスケール変化
    scale_3d_keyframes = {
        0.0: 1.0,
        0.25: 0.2,  # 横から見た状態（薄く）
        0.5: 1.0,
        0.75: 0.2,
        1.0: 1.0
    }
    
    rotation_3d_text.animate_rotation(LinearAnimation(from_value=0, to_value=360, duration=4.0, delay=0.5))
    rotation_3d_text.animate_scale(KeyframeAnimation(scale_3d_keyframes, duration=4.0, delay=0.5))
    scene.add(rotation_3d_text)
    
    # Test 7: 地震効果（シェイク）
    shake_text = (
        TextElement("EARTHQUAKE!", size=100, color=(255, 0, 0))
            .position(500, 400)
            .set_duration(8)
            .start_at(12)
    )
    
    # シェイク効果のキーフレーム
    import random
    shake_keyframes_x = {}
    shake_keyframes_y = {}
    base_x, base_y = 500, 400
    
    for i in range(41):  # 40分割で細かく震える
        t = i / 40.0
        intensity = max(0, 1.0 - t) * 20  # 徐々に収束
        
        shake_x = base_x + random.uniform(-intensity, intensity)
        shake_y = base_y + random.uniform(-intensity, intensity)
        
        shake_keyframes_x[t] = shake_x
        shake_keyframes_y[t] = shake_y
    
    shake_text.animate('x', KeyframeAnimation(shake_keyframes_x, duration=3.0, delay=1.0))
    shake_text.animate('y', KeyframeAnimation(shake_keyframes_y, duration=3.0, delay=1.0))
    scene.add(shake_text)
    
    # Add scene to master scene
    master_scene.add(scene)
    
    print("Starting to render advanced animation test video...")
    master_scene.render()
    print("Advanced animation test video rendering complete! Check output/animation_advanced_test.mp4")


if __name__ == "__main__":
    main()