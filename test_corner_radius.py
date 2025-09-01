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
from image_element import ImageElement
from video_element import VideoElement


def main():
    """Test corner radius functionality with all element types"""
    # Create master scene
    master_scene = MasterScene(width=1920, height=1080, fps=30)
    master_scene.set_output("corner_radius_test.mp4")
    
    # Create scene
    scene = Scene()
    
    # Test 1: Text element with corner radius and background
    text1 = (
        TextElement("Rounded Text", size=80, color=(255, 255, 255))
            .set_background((255, 100, 100), alpha=200, padding=20)
            .set_corner_radius(15)
            .position(100, 100)
            .set_duration(5)
            .start_at(0)
    )
    
    # Test 2: Text element with corner radius, background, and border
    text2 = (
        TextElement("Rounded Border Text", size=60, color=(255, 255, 255))
            .set_background((100, 150, 255), alpha=180, padding=15)
            .set_border((255, 255, 0), width=5)
            .set_corner_radius(25)
            .position(100, 250)
            .set_duration(5)
            .start_at(1)
    )
    
    # Test 3: Image element with corner radius and border
    image1 = (
        ImageElement("sample_asset/sample.jpg")
            .position(600, 100)
            .set_scale(0.4)
            .set_border((0, 255, 0), width=8)
            .set_corner_radius(30)
            .set_duration(5)
            .start_at(0.5)
    )
    
    # Test 4: Video element with corner radius and border
    video1 = (
        VideoElement("sample_asset/sample.mp4")
            .position(1200, 100)
            .set_scale(0.3)
            .set_border((255, 0, 255), width=6)
            .set_corner_radius(20)
            .set_duration(5)
            .start_at(1.5)
    )
    
    # Test 5: Multiline text with corner radius
    multiline = (
        TextElement("Multiline\nRounded\nText Element", size=50, color=(0, 255, 255))
            .set_background((50, 50, 50), alpha=200, padding=20)
            .set_border((0, 255, 255), width=3)
            .set_corner_radius(18)
            .set_alignment('center')
            .set_line_spacing(8)
            .position(100, 450)
            .set_duration(5)
            .start_at(2)
    )
    
    # Test 6: Large corner radius
    text3 = (
        TextElement("Big Radius", size=70, color=(255, 255, 255))
            .set_background((200, 0, 200), alpha=220, padding=30)
            .set_corner_radius(50)
            .position(600, 400)
            .set_duration(5)
            .start_at(2.5)
    )
    
    # Test 7: Zero corner radius (should work like before)
    text4 = (
        TextElement("No Radius", size=60, color=(255, 255, 255))
            .set_background((100, 100, 100), alpha=200, padding=15)
            .set_border((255, 255, 255), width=3)
            .set_corner_radius(0)
            .position(1200, 400)
            .set_duration(5)
            .start_at(3)
    )
    
    # Add all elements to scene
    scene.add(text1)
    scene.add(text2)
    scene.add(image1)
    scene.add(video1)
    scene.add(multiline)
    scene.add(text3)
    scene.add(text4)
    
    # Add scene to master scene
    master_scene.add(scene)
    
    # Execute rendering
    print("Testing corner radius functionality...")
    master_scene.render()
    print("Corner radius test video generated: output/corner_radius_test.mp4")


if __name__ == "__main__":
    main()