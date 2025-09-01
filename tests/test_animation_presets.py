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
from animation import AnimationPresets, LinearAnimation


def main():
    """プリセットアニメーション機能のテスト"""
    # Create master scene
    master_scene = MasterScene(width=1920, height=1080, fps=30)
    master_scene.set_output("animation_presets_test.mp4")
    
    # Create scene
    scene = Scene()
    
    # タイトル
    title = (
        TextElement("Animation Presets Demo", size=100, color=(255, 255, 255))
            .position(500, 100)
            .set_duration(20)
            .start_at(0)
            .animate_fade(AnimationPresets.fade_in(duration=1.5))
    )
    scene.add(title)
    
    # Test 1: フェードイン
    fade_in_demo = (
        TextElement("Fade In", size=70, color=(255, 200, 200))
            .position(200, 300)
            .set_duration(15)
            .start_at(2)
            .animate_fade(AnimationPresets.fade_in(duration=2.0, delay=0.5))
    )
    scene.add(fade_in_demo)
    
    # Test 2: 左からスライドイン
    slide_left_demo = (
        TextElement("Slide from Left", size=70, color=(200, 255, 200))
            .position(600, 300)
            .set_duration(15)
            .start_at(3)
            .animate('x', AnimationPresets.slide_in_from_left(distance=400, duration=1.5, delay=0.5))
    )
    scene.add(slide_left_demo)
    
    # Test 3: 右からスライドイン
    slide_right_demo = (
        TextElement("Slide from Right", size=70, color=(200, 200, 255))
            .position(1200, 300)
            .set_duration(15)
            .start_at(4)
            .animate('x', AnimationPresets.slide_in_from_right(distance=400, duration=1.5, delay=0.5))
    )
    scene.add(slide_right_demo)
    
    # Test 4: スケールアップ
    scale_up_demo = (
        TextElement("Scale Up", size=70, color=(255, 255, 200))
            .position(200, 500)
            .set_duration(15)
            .start_at(5)
            .animate_scale(AnimationPresets.scale_up(from_scale=0.0, to_scale=1.0, duration=2.0, delay=0.5))
    )
    scene.add(scale_up_demo)
    
    # Test 5: バウンスイン
    bounce_in_demo = (
        TextElement("Bounce In", size=70, color=(255, 200, 255))
            .position(600, 500)
            .set_duration(15)
            .start_at(6)
            .animate_scale(AnimationPresets.bounce_in(duration=2.5, delay=0.5))
    )
    scene.add(bounce_in_demo)
    
    # Test 6: スプリングイン
    spring_in_demo = (
        TextElement("Spring In", size=70, color=(200, 255, 255))
            .position(1200, 500)
            .set_duration(15)
            .start_at(7)
            .animate_scale(AnimationPresets.spring_in(duration=3.0, delay=0.5))
    )
    scene.add(spring_in_demo)
    
    # Test 7: 複合アニメーション（複数のプリセット組み合わせ）
    combo_demo = (
        TextElement("Combo Animation", size=80, color=(255, 150, 100))
            .position(700, 700)
            .set_duration(15)
            .start_at(8)
            .animate_fade(AnimationPresets.fade_in(duration=1.0, delay=0.0))
            .animate('x', AnimationPresets.slide_in_from_left(distance=500, duration=2.0, delay=0.2))
            .animate_scale(AnimationPresets.bounce_in(duration=2.5, delay=0.5))
    )
    scene.add(combo_demo)
    
    # Test 8: 順次登場（カスケード効果）
    cascade_words = ["Easy", "to", "use", "presets!"]
    for i, word in enumerate(cascade_words):
        cascade_text = (
            TextElement(word, size=90, color=(100 + i * 40, 255 - i * 30, 150 + i * 20))
                .position(300 + i * 250, 850)
                .set_duration(15)
                .start_at(10)
                .animate_fade(AnimationPresets.fade_in(duration=0.8, delay=i * 0.3))
                .animate('y', AnimationPresets.slide_in_from_left(distance=100, duration=1.0, delay=i * 0.3))
                .animate_scale(AnimationPresets.scale_up(from_scale=0.5, to_scale=1.0, duration=1.2, delay=i * 0.3))
        )
        scene.add(cascade_text)
    
    # Test 9: フェードアウトで終了
    fade_out_demo = (
        TextElement("Thank you!", size=120, color=(255, 255, 255))
            .position(700, 450)
            .set_duration(8)
            .start_at(15)
            .animate_fade(AnimationPresets.fade_in(duration=1.0, delay=0.5))
            .animate_fade(AnimationPresets.fade_out(duration=2.0, delay=4.0))
    )
    scene.add(fade_out_demo)
    
    # 背景画像があれば追加
    if os.path.exists("sample_asset/image.png"):
        background = (
            ImageElement("sample_asset/image.png")
                .set_crop(1920, 1080, mode='fill')
                .position(0, 0)
                .set_duration(25)
                .start_at(0)
                .animate_fade(LinearAnimation(from_value=50, to_value=50, duration=1.0))  # 薄い背景として
        )
        scene.add(background)
    
    # Add scene to master scene
    master_scene.add(scene)
    
    print("Starting to render animation presets test video...")
    master_scene.render()
    print("Animation presets test video rendering complete! Check output/animation_presets_test.mp4")


if __name__ == "__main__":
    main()