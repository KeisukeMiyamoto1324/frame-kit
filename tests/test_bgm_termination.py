#!/usr/bin/env python3

from master_scene import MasterScene
from scene import Scene
from video_element import VideoElement
from audio_element import AudioElement
from text_element import TextElement

def test_bgm_termination():
    """Test BGM forced termination when scene is shorter than BGM"""
    
    print("=== BGM Forced Termination Test ===")
    print("Testing scenario where BGM is longer than scene duration")
    
    # Create master scene
    master_scene = MasterScene(width=1920, height=1080, fps=30)
    master_scene.set_output("bgm_termination_test.mp4")
    
    # Test scenario 1: BGM should be cut short
    print("\n--- Scenario 1: BGM Cut Short ---")
    scene1 = Scene()
    
    # Add long BGM first
    bgm_path = "sample_asset/sample-bgm.mp3"
    bgm1 = (
        AudioElement(bgm_path)
        .set_volume(0.6)
        .set_loop_until_scene_end(True)  # BGM mode
        .start_at(0)
    )
    scene1.add(bgm1)
    print(f"BGM original duration: {bgm1.original_duration:.2f}s")
    
    # Add short video (5 seconds) - this should determine scene length
    video1 = (
        VideoElement("sample_asset/sample1.mp4")
        .position(200, 200)
        .set_scale(0.4)
        .set_border((255, 0, 0), width=3)
        .set_corner_radius(15)
        .mute_audio()  # Focus on BGM
        .start_at(0)
        .set_duration(5)  # Only 5 seconds
    )
    scene1.add(video1)
    
    # Add text
    text1 = (
        TextElement("BGM Cut Test - 5 sec video", size=50, color=(255, 255, 255))
        .set_background((255, 0, 0), alpha=150, padding=15)
        .set_corner_radius(10)
        .position(200, 50)
        .start_at(0)
        .set_duration(5)
    )
    scene1.add(text1)
    
    scene1.start_at(0)
    master_scene.add(scene1)
    
    print(f"Scene 1 duration: {scene1.duration:.2f}s")
    print(f"BGM final duration: {bgm1.duration:.2f}s")
    print(f"BGM will be {'CUT SHORT' if bgm1.duration < bgm1.original_duration else 'EXTENDED'}")
    
    # Test scenario 2: BGM should loop
    print("\n--- Scenario 2: BGM Loop ---")
    scene2 = Scene()
    
    # Add same BGM
    bgm2 = (
        AudioElement(bgm_path)
        .set_volume(0.4)
        .set_loop_until_scene_end(True)
        .start_at(0)
    )
    scene2.add(bgm2)
    
    # Add longer video (15 seconds)
    video2 = (
        VideoElement("sample_asset/sample1.mp4")
        .position(700, 300)
        .set_scale(0.3)
        .set_border((0, 255, 0), width=2)
        .set_corner_radius(20)
        .mute_audio()
        .start_at(0)
        .set_duration(15)  # 15 seconds
    )
    scene2.add(video2)
    
    # Add text
    text2 = (
        TextElement("BGM Loop Test - 15 sec video", size=50, color=(255, 255, 255))
        .set_background((0, 255, 0), alpha=150, padding=15)
        .set_corner_radius(10)
        .position(700, 50)
        .start_at(0)
        .set_duration(15)
    )
    scene2.add(text2)
    
    scene2.start_at(6)  # Start after scene 1 ends
    master_scene.add(scene2)
    
    print(f"Scene 2 duration: {scene2.duration:.2f}s")
    print(f"BGM 2 final duration: {bgm2.duration:.2f}s")
    print(f"BGM 2 will {'LOOP' if bgm2.duration > bgm2.original_duration else 'BE CUT'}")
    
    # Summary
    print(f"\n=== Test Summary ===")
    print(f"Total master scene duration: {master_scene.total_duration:.2f}s")
    print(f"Scene 1: 0-{scene1.duration}s (BGM cut short)")
    print(f"Scene 2: {scene2.start_time}-{scene2.start_time + scene2.duration}s (BGM looped)")
    print(f"Number of audio elements: {len(master_scene.audio_elements)}")
    
    # Verify BGM behavior
    print(f"\n=== BGM Behavior Verification ===")
    for i, audio_elem in enumerate(master_scene.audio_elements, 1):
        if hasattr(audio_elem, 'loop_until_scene_end') and audio_elem.loop_until_scene_end:
            behavior = "LOOP" if audio_elem.duration > audio_elem.original_duration else "CUT"
            print(f"BGM {i}: {audio_elem.original_duration:.2f}s → {audio_elem.duration:.2f}s ({behavior})")
    
    # Render
    print(f"\n=== Starting Render ===")
    print("Expected result:")
    print("- Scene 1 (0-5s): BGM plays for 5s then stops")  
    print("- Scene 2 (6-21s): BGM loops for 15s then stops")
    print("- Total video: 21s with BGM properly cut/looped")
    
    master_scene.render()
    
    print("\n✅ BGM termination test completed!")

def test_bgm_edge_cases():
    """Test edge cases for BGM behavior"""
    
    print("\n=== BGM Edge Cases Test ===")
    
    # Edge case: BGM only (no other elements)
    master_scene = MasterScene(width=1920, height=1080, fps=30)
    master_scene.set_output("bgm_edge_case_test.mp4")
    
    scene = Scene()
    
    # Add BGM with no other elements
    bgm = (
        AudioElement("sample_asset/sample-bgm.mp3")
        .set_volume(0.7)
        .set_loop_until_scene_end(True)
        .start_at(0)
    )
    scene.add(bgm)
    
    print(f"BGM-only scene duration: {scene.duration:.2f}s")
    print(f"BGM duration: {bgm.duration:.2f}s")
    
    # Add a text element to give scene some duration
    text = (
        TextElement("BGM Only Test", size=80, color=(255, 255, 255))
        .set_background((0, 0, 0), alpha=180, padding=25)
        .set_corner_radius(15)
        .position(960 - 150, 500)
        .start_at(0)
        .set_duration(8)  # 8 second scene
    )
    scene.add(text)
    
    master_scene.add(scene)
    
    print(f"After adding text - scene duration: {scene.duration:.2f}s")
    print(f"BGM adjusted duration: {bgm.duration:.2f}s")
    
    master_scene.render()
    
    print("✅ BGM edge cases test completed!")

if __name__ == "__main__":
    test_bgm_termination()
    test_bgm_edge_cases()