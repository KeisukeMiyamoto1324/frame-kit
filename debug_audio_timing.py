#!/usr/bin/env python3

from video_element import VideoElement

def test_audio_timing():
    """Test audio timing synchronization"""
    print("Testing VideoElement audio timing...")
    
    # Create video element
    video_path = "sample_asset/sample1.mp4"
    video = VideoElement(video_path)
    
    print(f"Initial video timing: start_time={video.start_time}, duration={video.duration}")
    if video.audio_element:
        print(f"Initial audio timing: start_time={video.audio_element.start_time}, duration={video.audio_element.duration}")
    else:
        print("No audio element initially")
    
    # Test method chaining
    print("\nTesting method chaining...")
    video = (video
             .start_at(5.0)
             .set_duration(10.0)
             .set_volume(0.8)
             .set_audio_fade_in(2.0)
             .mute_audio())
    
    print(f"After chaining - Video timing: start_time={video.start_time}, duration={video.duration}")
    if video.audio_element:
        print(f"After chaining - Audio timing: start_time={video.audio_element.start_time}, duration={video.audio_element.duration}")
        print(f"Audio volume: {video.audio_element.volume}")
        print(f"Audio is_muted: {video.audio_element.is_muted}")
        print(f"Audio fade_in_duration: {video.audio_element.fade_in_duration}")
    else:
        print("No audio element after chaining")

if __name__ == "__main__":
    test_audio_timing()