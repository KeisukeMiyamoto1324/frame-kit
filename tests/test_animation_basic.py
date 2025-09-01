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
    BounceAnimation, SpringAnimation, KeyframeAnimation, AnimationPresets
)


def main():
    """基本的なアニメーション機能のテスト"""
    # Create master scene
    master_scene = MasterScene(width=1920, height=1080, fps=30)
    master_scene.set_output("animation_basic_test.mp4")
    
    # Create scene
    scene = Scene()
    
    # Test 1: フェードインテキスト
    fade_in_text = (
        TextElement("Fade In Animation", size=80, color=(255, 255, 255))
            .position(100, 100)
            .set_duration(5)
            .start_at(0)
            .animate_fade(AnimationPresets.fade_in(duration=2.0, delay=0.5))
    )
    scene.add(fade_in_text)
    
    # Test 2: 左からスライドイン
    slide_text = (
        TextElement("Slide In From Left", size=60, color=(0, 255, 255))
            .position(960, 300)  # 最終位置
            .set_duration(6)
            .start_at(1)
            .animate('x', LinearAnimation(from_value=-300, to_value=960, duration=1.5, delay=0.5))
    )
    scene.add(slide_text)
    
    # Test 3: バウンススケールアニメーション
    bounce_text = (
        TextElement("Bounce Scale", size=70, color=(255, 100, 100))
            .position(500, 500)
            .set_duration(8)
            .start_at(2)
            .animate_scale(BounceAnimation(from_value=0.0, to_value=1.0, duration=2.5, delay=0.2))
    )
    scene.add(bounce_text)
    
    # Test 4: 回転アニメーション
    rotation_text = (
        TextElement("Rotating Text", size=50, color=(255, 255, 0))
            .position(1200, 200)
            .set_duration(10)
            .start_at(3)
            .animate_rotation(LinearAnimation(from_value=0, to_value=360, duration=4.0, delay=0.5))
    )
    scene.add(rotation_text)
    
    # Test 5: 複合アニメーション（位置 + スケール + 回転）
    complex_text = (
        TextElement("Complex Animation", size=60, color=(255, 0, 255))
            .position(960, 700)  # 最終位置
            .set_duration(12)
            .start_at(4)
            .animate('x', EaseOutAnimation(from_value=100, to_value=960, duration=3.0, delay=0.0))
            .animate('y', EaseInOutAnimation(from_value=900, to_value=700, duration=3.0, delay=0.0))
            .animate_scale(SpringAnimation(from_value=0.2, to_value=1.2, duration=2.5, delay=0.5))
            .animate_rotation(LinearAnimation(from_value=0, to_value=180, duration=3.5, delay=0.0))
    )
    scene.add(complex_text)
    
    # Test 6: キーフレームアニメーション
    keyframe_text = (
        TextElement("Keyframe Animation", size=55, color=(0, 255, 0))
            .position(400, 850)
            .set_duration(10)
            .start_at(6)
            .animate('y', KeyframeAnimation({
                0.0: 850,
                0.3: 200,
                0.6: 600,
                1.0: 400
            }, duration=4.0, delay=0.5, interpolation='ease_in_out'))
    )
    scene.add(keyframe_text)
    
    # Test 7: 画像アニメーション（存在する場合のみ）
    if os.path.exists("sample_asset/image.png"):
        animated_image = (
            ImageElement("sample_asset/image.png")
                .set_scale(0.3)
                .position(1400, 500)  # 最終位置
                .set_duration(15)
                .start_at(0)
                .animate('x', EaseInAnimation(from_value=1920, to_value=1400, duration=2.0, delay=1.0))
                .animate_scale(LinearAnimation(from_value=0.1, to_value=0.3, duration=1.5, delay=1.5))
                .animate_rotation(LinearAnimation(from_value=0, to_value=720, duration=6.0, delay=2.0))
                .animate_fade(LinearAnimation(from_value=255, to_value=100, duration=2.0, delay=10.0))
        )
        scene.add(animated_image)
    
    # Test 8: フェードアウト（最後）
    fade_out_text = (
        TextElement("Fade Out Ending", size=90, color=(255, 255, 255))
            .position(600, 500)
            .set_duration(5)
            .start_at(12)
            .animate_fade(LinearAnimation(from_value=255, to_value=0, duration=2.0, delay=2.5))
    )
    scene.add(fade_out_text)
    
    # Add scene to master scene
    master_scene.add(scene)
    
    print("Starting to render basic animation test video...")
    master_scene.render()
    print("Animation test video rendering complete! Check output/animation_basic_test.mp4")


if __name__ == "__main__":
    main()