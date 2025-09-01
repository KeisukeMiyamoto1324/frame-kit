import os
import warnings

# Pygame関連の環境変数を事前に設定
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# pkg_resources警告を抑制
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*pkg_resources.*")

from text_element import TextElement
from image_element import ImageElement
from video_element import VideoElement


def test_box_sizes():
    """Test box size properties for all element types"""
    print("Testing element box size properties...")
    
    # Test TextElement box size
    print("\n=== TextElement Box Size Test ===")
    text1 = TextElement("Hello World", size=50, color=(255, 255, 255))
    print(f"Text (no background): {text1.width}x{text1.height}")
    
    text2 = (TextElement("Hello with Background", size=60, color=(255, 255, 255))
             .set_background((255, 100, 100), alpha=200, padding=20))
    print(f"Text (with background, padding=20): {text2.width}x{text2.height}")
    
    text3 = (TextElement("Hello with Border", size=40, color=(255, 255, 255))
             .set_border((0, 255, 0), width=5))
    print(f"Text (with border, width=5): {text3.width}x{text3.height}")
    
    text4 = (TextElement("Multi\nLine\nText", size=50, color=(255, 255, 255))
             .set_background((100, 100, 200), alpha=180, padding=15)
             .set_border((255, 255, 0), width=3)
             .set_corner_radius(10)
             .set_alignment('center')
             .set_line_spacing(5))
    print(f"Multiline text (full styling): {text4.width}x{text4.height}")
    
    # Test ImageElement box size
    print("\n=== ImageElement Box Size Test ===")
    if os.path.exists("sample_asset/sample.jpg"):
        image1 = ImageElement("sample_asset/sample.jpg")
        print(f"Image (no styling): {image1.width}x{image1.height}")
        
        image2 = (ImageElement("sample_asset/sample.jpg")
                  .set_scale(0.5)
                  .set_border((255, 0, 255), width=8)
                  .set_corner_radius(15))
        print(f"Image (scale=0.5, border=8, radius=15): {image2.width}x{image2.height}")
    else:
        print("sample_asset/sample.jpg not found - skipping image tests")
    
    # Test VideoElement box size
    print("\n=== VideoElement Box Size Test ===")
    if os.path.exists("sample_asset/sample.mp4"):
        video1 = VideoElement("sample_asset/sample.mp4")
        print(f"Video (no styling): {video1.width}x{video1.height}")
        
        video2 = (VideoElement("sample_asset/sample.mp4")
                  .set_scale(0.3)
                  .set_border((0, 255, 255), width=6)
                  .set_corner_radius(20))
        print(f"Video (scale=0.3, border=6, radius=20): {video2.width}x{video2.height}")
    else:
        print("sample_asset/sample.mp4 not found - skipping video tests")
    
    # Test usage example: centering elements
    print("\n=== Usage Example: Element Positioning ===")
    screen_width, screen_height = 1920, 1080
    
    title = (TextElement("Centered Title", size=80, color=(255, 255, 255))
             .set_background((50, 50, 50), alpha=200, padding=30)
             .set_corner_radius(15))
    
    # Center the title on screen
    title_x = (screen_width - title.width) // 2
    title_y = (screen_height - title.height) // 2
    title.position(title_x, title_y)
    
    print(f"Title size: {title.width}x{title.height}")
    print(f"Centered position: ({title.x}, {title.y})")
    
    # Position subtitle below title
    subtitle = (TextElement("Subtitle Text", size=40, color=(200, 200, 200))
                .set_background((30, 30, 30), alpha=180, padding=15)
                .set_corner_radius(8))
    
    subtitle_x = (screen_width - subtitle.width) // 2
    subtitle_y = title.y + title.height + 20  # 20px gap below title
    subtitle.position(subtitle_x, subtitle_y)
    
    print(f"Subtitle size: {subtitle.width}x{subtitle.height}")
    print(f"Positioned below title: ({subtitle.x}, {subtitle.y})")
    
    print("\nBox size properties test completed!")


if __name__ == "__main__":
    test_box_sizes()