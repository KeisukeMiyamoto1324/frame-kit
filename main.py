import os
import warnings

# Pygame関連の環境変数を事前に設定
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# pkg_resources警告を抑制
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*pkg_resources.*")

from master_scene import MasterScene
from scene import Scene
from text_element import Text
from image_element import ImageElement


def main():
    """Main function - Video creation demo with text and image"""
    # Create master scene
    master_scene = MasterScene(width=1920, height=1080, fps=60)
    master_scene.set_output("text_and_image_demo.mp4")
    
    # Create scene
    scene = Scene()
    
    # Create text elements (positioned near screen center)
    text1 = (
        Text("Hello", size=100, color=(255, 0, 0))
            .position(960, 300)
            .set_duration(3)
    )
    text2 = (
        Text("World", size=80, color=(0, 255, 0))
            .position(960, 400)
            .set_duration(5)
            .start_at(1)
    )
    
    # Create image element
    image1 = (
        ImageElement("sample.jpg")
            .position(500, 500)
            .set_scale(0.5)
            .set_duration(4)
            .start_at(0.5)
    )
    
    # Add elements to scene
    scene.add(text1)
    scene.add(text2)
    scene.add(image1)
    
    # Add scene to master scene
    master_scene.add(scene)
    
    # Execute rendering
    master_scene.render()


if __name__ == "__main__":
    main()