import os
import warnings

# Pygame関連の環境変数を事前に設定
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# pkg_resources警告を抑制
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*pkg_resources.*")

from master_scene import MasterScene
from scene import Scene
from text_element import TextElement


def main():
    """Demo to test new telop features"""
    # Create master scene
    master_scene = MasterScene(width=1920, height=1080, fps=30)
    master_scene.set_output("telop_features_demo.mp4")
    
    # Create scene
    scene = Scene()
    
    # Test 1: Text with background box
    text1 = (
        TextElement("Background Box", size=80, color=(255, 255, 255))
            .set_background((0, 100, 200), alpha=200, padding=20)  # Blue semi-transparent background, 20px padding
            .position(100, 100)
            .set_duration(3)
            .start_at(0)
    )
    
    # Test 2: Text with border (no background)
    text2 = (
        TextElement("Border Text", size=60, color=(255, 100, 100))
            .set_border((255, 0, 0), width=3)  # Red 3px border
            .position(100, 250)
            .set_duration(3)
            .start_at(1)
    )
    
    # Test 3: Background and border both
    text3 = (
        TextElement("Background + Border", size=70, color=(255, 255, 255))
            .set_background((50, 50, 50), alpha=180, padding=15)  # Gray background
            .set_border((255, 255, 0), width=2)  # Yellow border
            .position(100, 400)
            .set_duration(3)
            .start_at(2)
    )
    
    # Test 4: Multiline text (left aligned)
    multiline_text1 = (
        TextElement("Multiline Text\nTest Sample\nLeft Aligned", size=50, color=(0, 255, 0))
            .set_background((0, 0, 0), alpha=150, padding=10)
            .set_line_spacing(5)  # 5px line spacing
            .set_alignment('left')
            .position(500, 100)
            .set_duration(4)
            .start_at(1.5)
    )
    
    # Test 5: Multiline text (center aligned)
    multiline_text2 = (
        TextElement("Multiline Text\nTest Sample\nCenter Aligned", size=50, color=(255, 255, 0))
            .set_background((100, 0, 100), alpha=150, padding=10)
            .set_line_spacing(10)  # 10px line spacing
            .set_alignment('center')
            .position(800, 100)
            .set_duration(4)
            .start_at(2)
    )
    
    # Test 6: Multiline text (right aligned)
    multiline_text3 = (
        TextElement("Multiline Text\nTest Sample\nRight Aligned", size=50, color=(0, 255, 255))
            .set_background((100, 100, 0), alpha=150, padding=10)
            .set_line_spacing(15)  # 15px line spacing
            .set_alignment('right')
            .position(1200, 100)
            .set_duration(4)
            .start_at(2.5)
    )
    
    # Test 7: News-style ticker (bottom of screen)
    news_telop = (
        TextElement("BREAKING NEWS: New telop features implemented! Background, border, and multiline support added.", 
                   size=40, color=(255, 255, 255))
            .set_background((255, 0, 0), alpha=220, padding={'top': 10, 'bottom': 10, 'left': 30, 'right': 30})
            .set_border((255, 255, 255), width=2)
            .set_alignment('center')
            .position(100, 950)  # Bottom of screen
            .set_duration(5)
            .start_at(3)
    )
    
    # Test 8: Subtitle-style text
    subtitle = (
        TextElement("This is subtitle-like\nmultiline text", 
                   size=45, color=(255, 255, 255))
            .set_background((0, 0, 0), alpha=180, padding=15)
            .set_line_spacing(8)
            .set_alignment('center')
            .position(600, 800)  # Lower part of screen
            .set_duration(4)
            .start_at(4)
    )
    
    # Add all elements to scene
    scene.add(text1)
    scene.add(text2)
    scene.add(text3)
    scene.add(multiline_text1)
    scene.add(multiline_text2)
    scene.add(multiline_text3)
    scene.add(news_telop)
    scene.add(subtitle)
    
    # Add scene to master scene
    master_scene.add(scene)
    
    # Execute rendering
    print("Generating demo video for new telop features...")
    master_scene.render()


if __name__ == "__main__":
    main()