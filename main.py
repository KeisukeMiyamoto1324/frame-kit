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
    """Main function - Video creation demo with text, image, and video"""
    # Create master scene
    master_scene = MasterScene(width=1920, height=1080, fps=60)
    master_scene.set_output("text_image_video_demo.mp4")
    
    # Create scene
    scene1 = Scene()
    scene2 = Scene()
    
    # Create text elements (positioned near screen center)
    text1 = (
        TextElement("Hello", size=100, color=(255, 0, 0))
            .position(960, 300)
            .set_duration(3)
    )

    text2 = (
        TextElement("World", size=80, color=(0, 255, 0))
            .position(960, 400)
            .set_duration(5)
            # .start_at(1)
            .set_border(color=[127, 127, 127])
    )
    
    # Create image element
    image1 = (
        ImageElement("sample_asset/sample.jpg")
            .position(500, 500)
            .set_scale(0.5)
            .set_duration(4)
            # .start_at(0.5)
            .set_border(color=[127, 127, 127])
    )
    
    # Create video element
    video1 = (
        VideoElement("sample_asset/sample.mp4")
            .position(100, 100)
            .set_scale(0.3)
            .set_duration(6)
            # .start_at(1.5)
            .set_border(color=[127, 127, 127])
    )
    
    # Add elements to scene
    scene1.add(text1)
    scene2.add(text2)
    scene1.add(image1)
    scene2.add(video1)
    
    # Add scene to master scene
    master_scene.add(scene1)
    master_scene.add(scene2)
    
    # Execute rendering
    master_scene.render()


if __name__ == "__main__":
    main()