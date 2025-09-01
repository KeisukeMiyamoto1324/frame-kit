#!/usr/bin/env python3

from master_scene import MasterScene
from scene import Scene
from video_element import VideoElement
from audio_element import AudioElement
from text_element import TextElement

def test_bgm_functionality():
    """Test BGM (background music) functionality"""
    
    # Create master scene
    master_scene = MasterScene(width=1920, height=1080, fps=30)
    master_scene.set_output("bgm_test.mp4")
    
    # Create scene
    scene = Scene()
    
    # Add BGM audio that will loop until scene ends
    bgm_path = "/Users/keisukemiyamoto/Project/video-editer/sample_asset/sample-bgm.mp3"
    try:
        bgm = (
            AudioElement(bgm_path)
            .set_volume(0.3)  # Lower volume for background music
            .set_loop_until_scene_end(True)  # Enable BGM mode
            .start_at(0)
        )
        scene.add(bgm)
        print(f"BGM added: {bgm_path}")
    except Exception as e:
        print(f"BGM file not found: {e}")
        # BGMファイルがない場合はテストを続行
        print("Continuing test without BGM...")
    
    # Add video elements that will determine the total scene duration
    video_path = "sample_asset/sample1.mp4"
    
    # First video (0-6 seconds)
    video1 = (
        VideoElement(video_path)
        .position(100, 100)
        .set_scale(0.4)
        .set_border((255, 255, 255))
        .set_corner_radius(15)
        .set_volume(0.1)  # Lower volume so BGM is audible
        .start_at(0)
        .set_duration(6)
    )
    scene.add(video1)
    
    # Second video (3-10 seconds, overlapping)
    video2 = (
        VideoElement(video_path)
        .position(600, 300)
        .set_scale(0.3)
        .set_border((0, 255, 0))
        .set_corner_radius(25)
        .set_volume(0.1)  # Lower volume so BGM is audible
        .start_at(3)
        .set_duration(7)
    )
    scene.add(video2)
    
    # Add text elements
    title = (
        TextElement("BGM Test - Background Music Loop", size=60, color=(255, 255, 255))
        .set_background((0, 0, 0), alpha=180, padding=20)
        .set_corner_radius(10)
        .position(960 - 300, 50)
        .start_at(0)
        .set_duration(5)
    )
    scene.add(title)
    
    info_text = (
        TextElement("BGM should loop until scene ends\nVideos have reduced volume", 
                   size=40, color=(255, 255, 0))
        .set_background((0, 0, 0), alpha=120, padding=15)
        .set_corner_radius(8)
        .set_alignment('center')
        .set_line_spacing(5)
        .position(960 - 200, 800)
        .start_at(5)
        .set_duration(5)
    )
    scene.add(info_text)
    
    # Add the scene to master scene
    master_scene.add(scene)
    
    print(f"Scene duration: {scene.duration:.2f}s")
    print(f"Master scene total duration: {master_scene.total_duration:.2f}s")
    
    # Check BGM duration after scene setup
    for element in scene.elements:
        if isinstance(element, AudioElement) and element.loop_until_scene_end:
            print(f"BGM final duration: {element.duration:.2f}s (original: {element.original_duration:.2f}s)")
    
    # Render the video
    print("Starting BGM test render...")
    master_scene.render()
    
    print("BGM test completed!")

if __name__ == "__main__":
    test_bgm_functionality()