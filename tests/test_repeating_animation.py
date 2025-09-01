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
    LinearAnimation, EaseInOutAnimation, RepeatingAnimation, AnimationPresets
)


def main():
    """繰り返しアニメーション機能のテスト"""
    # Create master scene
    master_scene = MasterScene(width=1920, height=1080, fps=30)
    master_scene.set_output("repeating_animation_test.mp4")
    
    # Create scene
    scene = Scene()
    
    # Test 1: 基本的な繰り返しアニメーション（5回繰り返し）
    repeat_basic = (
        TextElement("5x Repeat", size=70, color=(255, 200, 200))
            .position(200, 100)
            .set_duration(20)
            .start_at(0)
            .animate_repeating_scale(
                AnimationPresets.pulse(from_scale=1.0, to_scale=1.5, duration=1.5),
                repeat_count=5,
                repeat_delay=0.3,
                repeat_mode='restart'
            )
    )
    scene.add(repeat_basic)
    
    # Test 2: 無限繰り返しアニメーション
    repeat_infinite = (
        TextElement("Infinite Pulse", size=70, color=(200, 255, 200))
            .position(700, 100)
            .set_duration(20)
            .start_at(0)
            .animate_repeating_scale(
                AnimationPresets.pulse(from_scale=1.0, to_scale=1.3, duration=1.0),
                repeat_count=-1,  # 無限繰り返し
                repeat_delay=0.2,
                repeat_mode='restart'
            )
    )
    scene.add(repeat_infinite)
    
    # Test 3: 往復アニメーション（reverseモード）
    repeat_reverse = (
        TextElement("Reverse Mode", size=70, color=(200, 200, 255))
            .position(1300, 100)
            .set_duration(20)
            .start_at(0)
            .animate_repeating_scale(
                LinearAnimation(from_value=1.0, to_value=1.4, duration=1.2),
                repeat_count=8,
                repeat_delay=0.1,
                repeat_mode='reverse'
            )
    )
    scene.add(repeat_reverse)
    
    # Test 4: シーン終了まで繰り返すアニメーション
    until_scene_end = (
        TextElement("Until Scene End", size=80, color=(255, 255, 100))
            .position(200, 300)
            .set_duration(20)
            .start_at(2)
            .animate_until_scene_end(
                'scale',
                AnimationPresets.breathing(from_scale=1.0, to_scale=1.2, duration=2.5),
                repeat_delay=0.5,
                scene_duration=18  # 18秒間繰り返し
            )
    )
    scene.add(until_scene_end)
    
    # Test 5: 位置の繰り返しアニメーション（左右に揺れる）
    wiggle_position = (
        TextElement("Wiggle Position", size=60, color=(255, 150, 255))
            .position(960, 500)  # 中央位置
            .set_duration(20)
            .start_at(0)
            .animate_repeating_position(
                LinearAnimation(from_value=-50, to_value=50, duration=0.8),
                axis='x',  # x軸のみ
                repeat_count=-1,
                repeat_delay=0.1,
                repeat_mode='reverse'
            )
    )
    scene.add(wiggle_position)
    
    # Test 6: 回転の繰り返しアニメーション
    spin_forever = (
        TextElement("Spinning!", size=70, color=(100, 255, 255))
            .position(200, 700)
            .set_duration(20)
            .start_at(1)
            .animate_repeating_rotation(
                LinearAnimation(from_value=0, to_value=360, duration=2.0),
                repeat_count=-1,
                repeat_delay=0.0,
                repeat_mode='restart'
            )
    )
    scene.add(spin_forever)
    
    # Test 7: 複合繰り返しアニメーション
    complex_repeat = (
        TextElement("Complex Repeat", size=60, color=(255, 100, 100))
            .position(1400, 500)
            .set_duration(20)
            .start_at(3)
            .animate_repeating_scale(
                AnimationPresets.pulse(from_scale=0.8, to_scale=1.3, duration=1.0),
                repeat_count=-1,
                repeat_delay=0.2
            )
            .animate_repeating_rotation(
                LinearAnimation(from_value=0, to_value=180, duration=2.5),
                repeat_count=-1,
                repeat_delay=0.5,
                repeat_mode='reverse'
            )
    )
    scene.add(complex_repeat)
    
    # Test 8: 画像の繰り返しアニメーション（存在する場合）
    if os.path.exists("sample_asset/image.png"):
        image_repeat = (
            ImageElement("sample_asset/image.png")
                .set_scale(0.2)
                .position(1400, 700)
                .set_duration(20)
                .start_at(0)
                .animate_pulse_until_end(
                    from_scale=0.2,
                    to_scale=0.3,
                    duration=1.8,
                    repeat_delay=0.3,
                    scene_duration=20
                )
        )
        scene.add(image_repeat)
    
    # Test 9: 呼吸のようなアニメーション
    breathing_text = (
        TextElement("Breathing", size=90, color=(150, 255, 150))
            .position(700, 800)
            .set_duration(20)
            .start_at(0)
            .animate_breathing_until_end(
                from_scale=1.0,
                to_scale=1.15,
                duration=4.0,
                repeat_delay=0.5,
                scene_duration=20
            )
    )
    scene.add(breathing_text)
    
    # Add scene to master scene
    master_scene.add(scene)
    
    print("Starting to render repeating animation test video...")
    master_scene.render()
    print("Repeating animation test video rendering complete! Check output/repeating_animation_test.mp4")


if __name__ == "__main__":
    main()