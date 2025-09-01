#!/usr/bin/env python3

from master_scene import MasterScene
from scene import Scene
from video_element import VideoElement
from audio_element import AudioElement
from text_element import TextElement

def test_bgm_simple():
    """Simple BGM loop test"""
    
    print("=== Simple BGM Test ===")
    
    # Create master scene (short test)
    master_scene = MasterScene(width=1920, height=1080, fps=30)
    master_scene.set_output("bgm_simple_test.mp4")
    
    # Create scene
    scene = Scene()
    
    # Add BGM first
    bgm_path = "sample_asset/sample.mp3"

    bgm = (
        AudioElement(bgm_path)
        .set_volume(0.5)  # 50% volume for BGM
        .set_loop_until_scene_end(True)  # Enable loop mode
        .start_at(0)
    )
    scene.add(bgm)

    # Add simple title
    title = (
        TextElement("BGM Loop Test - 12 seconds", size=60, color=(255, 255, 255))
        .set_background((0, 0, 0), alpha=180, padding=20)
        .set_corner_radius(10)
        .position(960 - 250, 100)
        .start_at(0)
        .set_duration(12)
    )
    scene.add(title)
    
    # Add scene to master
    master_scene.add(scene)
    
    print(master_scene.total_duration)
    
    master_scene.render()
    
    
    print("✅ Simple BGM test completed!")

if __name__ == "__main__":
    test_bgm_simple()