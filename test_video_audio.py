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
    
    # Add a test video with audio and audio control features
    video_path = "sample_asset/sample1.mp4"
    
    # Add another video with different audio settings
    video2 = (
        VideoElement(video_path)
        .position(600, 300)
        .set_scale(0.3)
        .set_border((0, 255, 0))
        .set_corner_radius(25)
        .set_volume(0.1)  # Set volume to 50%
        # .mute_audio()  # Start muted
        .start_at(5)
        .set_duration(5)
    )
    scene.add(video2)
    
    # Add the scene to master scene
    master_scene.add(scene)
    
    # Render the video
    print("Starting video render with audio extraction...")
    master_scene.render()
    
    print("Test completed!")

if __name__ == "__main__":
    test_video_audio()