#!/usr/bin/env python3

from master_scene import MasterScene
from scene import Scene
from video_element import VideoElement
from audio_element import AudioElement
from text_element import TextElement

def test_bgm_comprehensive():
    """Comprehensive BGM functionality test with specific BGM file"""
    
    print("=== BGM Comprehensive Test ===")
    
    # Create master scene
    master_scene = MasterScene(width=1920, height=1080, fps=30)
    master_scene.set_output("bgm_comprehensive_test.mp4")
    
    # Create scene
    scene = Scene()
    
    # Add BGM audio that will loop until scene ends
    bgm_path = "sample_asset/sample-bgm.mp3"
    bgm_added = False
    
    try:
        bgm = (
            AudioElement(bgm_path)
            .set_volume(0.4)  # BGM volume at 40%
            .set_loop_until_scene_end(True)  # Enable BGM loop mode
            .start_at(0)  # Start BGM immediately
        )
        scene.add(bgm)
        bgm_added = True
        print(f"✅ BGM successfully added: {bgm_path}")
        print(f"   Original BGM duration: {bgm.original_duration:.2f}s")
        print(f"   BGM loop mode: {bgm.loop_until_scene_end}")
        print(f"   BGM volume: {bgm.volume}")
    except Exception as e:
        print(f"❌ BGM file error: {e}")
        print("   Test will continue without BGM")
    
    # Add multiple video elements to create a longer scene
    video_path = "sample_asset/sample1.mp4"
    
    # Video 1: 0-8 seconds
    video1 = (
        VideoElement(video_path)
        .position(100, 100)
        .set_scale(0.35)
        .set_border((255, 255, 255), width=3)
        .set_corner_radius(20)
        .set_volume(0.15)  # Lower video volume to hear BGM
        .start_at(0)
        .set_duration(8)
    )
    scene.add(video1)
    print(f"Added Video 1: 0-8s, volume: {video1.get_audio_volume()}")
    
    # Video 2: 5-12 seconds (overlapping)
    video2 = (
        VideoElement(video_path)
        .position(600, 400)
        .set_scale(0.3)
        .set_border((0, 255, 0), width=2)
        .set_corner_radius(15)
        .set_volume(0.1)  # Even lower volume
        .start_at(5)
        .set_duration(7)
    )
    scene.add(video2)
    print(f"Added Video 2: 5-12s, volume: {video2.get_audio_volume()}")
    
    # Video 3: 10-18 seconds (extending scene length)
    video3 = (
        VideoElement(video_path)
        .position(1200, 200)
        .set_scale(0.25)
        .set_border((255, 0, 255), width=2)
        .set_corner_radius(10)
        .mute_audio()  # Muted to focus on BGM
        .start_at(10)
        .set_duration(8)
    )
    scene.add(video3)
    print(f"Added Video 3: 10-18s, muted")
    
    # Add informational text elements
    title = (
        TextElement("BGM Loop Test", size=80, color=(255, 255, 255))
        .set_background((0, 0, 0), alpha=200, padding=25)
        .set_corner_radius(15)
        .position(960 - 200, 50)
        .start_at(0)
        .set_duration(5)
    )
    scene.add(title)
    
    # BGM status text
    bgm_status = "BGM: Looping until scene ends" if bgm_added else "BGM: Not available"
    status_text = (
        TextElement(bgm_status, size=50, color=(255, 255, 0))
        .set_background((0, 0, 100), alpha=180, padding=20)
        .set_corner_radius(10)
        .position(50, 200)
        .start_at(2)
        .set_duration(8)
    )
    scene.add(status_text)
    
    # Scene timeline info
    timeline_text = (
        TextElement("Video 1: 0-8s\nVideo 2: 5-12s\nVideo 3: 10-18s (muted)", 
                   size=35, color=(255, 255, 255))
        .set_background((50, 50, 50), alpha=160, padding=15)
        .set_corner_radius(8)
        .set_alignment('left')
        .set_line_spacing(8)
        .position(50, 800)
        .start_at(5)
        .set_duration(13)
    )
    scene.add(timeline_text)
    
    # Final duration info
    final_info = (
        TextElement("BGM should loop for entire 18s duration", 
                   size=45, color=(0, 255, 0))
        .set_background((0, 0, 0), alpha=180, padding=20)
        .set_corner_radius(10)
        .set_alignment('center')
        .position(960 - 300, 500)
        .start_at(15)
        .set_duration(3)
    )
    scene.add(final_info)
    
    # Add the scene to master scene
    master_scene.add(scene)
    
    print(f"\n=== Scene Analysis ===")
    print(f"Scene duration: {scene.duration:.2f}s")
    print(f"Master scene total duration: {master_scene.total_duration:.2f}s")
    print(f"Number of elements in scene: {len(scene.elements)}")
    print(f"Number of audio elements collected: {len(master_scene.audio_elements)}")
    
    # Check BGM final state after all elements are added
    if bgm_added:
        for element in scene.elements:
            if isinstance(element, AudioElement) and element.loop_until_scene_end:
                print(f"\n=== BGM Final State ===")
                print(f"BGM original duration: {element.original_duration:.2f}s")
                print(f"BGM final duration: {element.duration:.2f}s")
                print(f"BGM loop enabled: {element.loop_until_scene_end}")
                print(f"BGM start time: {element.start_time:.2f}s")
                print(f"BGM volume: {element.volume}")
                print(f"Duration extension: {element.duration - element.original_duration:.2f}s")
                break
    
    print(f"\n=== Starting Render ===")
    print("Expected result:")
    print("- BGM should start at 0s and loop until 18s")
    print("- Video audio should be mixed with BGM at lower volumes")
    print("- Total video length should be 18 seconds")
    
    # Render the video
    master_scene.render()
    
    print("\n✅ BGM comprehensive test completed!")
    print("Check output/bgm_comprehensive_test.mp4 to verify BGM looping")

if __name__ == "__main__":
    test_bgm_comprehensive()