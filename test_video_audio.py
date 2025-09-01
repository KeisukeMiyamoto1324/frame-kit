#!/usr/bin/env python3

from master_scene import MasterScene
from scene import Scene
from video_element import VideoElement
from audio_element import AudioElement
from text_element import TextElement

def test_video_audio():
    """Test video with audio extraction and playback"""
    
    # Create master scene (shorter duration for testing)
    master_scene = MasterScene(width=1920, height=1080, fps=30)
    master_scene.set_output("video_audio_test.mp4")
    
    # Create scene
    scene = Scene()
    
    # Add a test video with audio (make sure this file exists)
    video_path = "sample_asset/sample1.mp4"
    video = (
        VideoElement(video_path)
        .position(100, 100)
        .set_scale(0.5)
        .set_border((255, 255, 255))
        .set_corner_radius(15)
        .start_at(0)
        .set_duration(10)  # 10 seconds for testing
    )
    scene.add(video)

    # Add title text
    title = (
        TextElement("Video Audio Test", size=80, color=(255, 255, 255))
        .set_background((0, 0, 0), alpha=180, padding=20)
        .set_corner_radius(10)
        .position(960 - 200, 50)  # Center horizontally
        .start_at(0)
        .set_duration(3)
    )
    scene.add(title)
    
    # Add the scene to master scene
    master_scene.add(scene)
    
    # Render the video
    print("Starting video render with audio extraction...")
    master_scene.render()
    
    print("Test completed!")

if __name__ == "__main__":
    test_video_audio()