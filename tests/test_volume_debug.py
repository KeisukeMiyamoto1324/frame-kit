#!/usr/bin/env python3

from master_scene import MasterScene
from scene import Scene
from video_element import VideoElement

def test_volume_debug():
    """Test volume functionality with debug output"""
    
    # Create master scene (shorter duration for testing)
    master_scene = MasterScene(width=1920, height=1080, fps=30)
    master_scene.set_output("volume_debug_test.mp4")
    
    # Create scene
    scene = Scene()
    
    # Add a test video with high volume
    video_path = "sample_asset/sample1.mp4"
    video = (
        VideoElement(video_path)
        .position(100, 100)
        .set_scale(0.3)
        .set_border((255, 255, 255))
        .set_corner_radius(15)
        .set_volume(2.0)  # High volume (200%)
        .start_at(0)
        .set_duration(5)
    )
    scene.add(video)
    
    # Check audio element properties
    print(f"Video audio element exists: {video.audio_element is not None}")
    if video.audio_element:
        print(f"Audio element volume: {video.audio_element.volume}")
        print(f"Audio element is_muted: {video.audio_element.is_muted}")
        print(f"Audio element start_time: {video.audio_element.start_time}")
        print(f"Audio element duration: {video.audio_element.duration}")
    
    # Add the scene to master scene
    master_scene.add(scene)
    
    # Render the video
    print("\nStarting video render with volume debug...")
    master_scene.render()
    
    print("Volume debug test completed!")

if __name__ == "__main__":
    test_volume_debug()