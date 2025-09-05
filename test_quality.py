#!/usr/bin/env python3
"""
Quality settings test script for FrameKit.

This script tests the new quality settings (low, medium, high) to ensure:
1. Text renders smoothly without jagged edges
2. Corner radius renders smoothly 
3. Elements are positioned correctly at all quality levels
4. No elements appear small or misplaced
"""

from framekit.master_scene_element import MasterScene
from framekit.scene_element import Scene
from framekit.text_element import TextElement
from framekit.image_element import ImageElement

def create_test_scene():
    """Create a test scene with various elements to test quality rendering."""
    scene = Scene()
    
    # Test text with corner radius (the main issue mentioned)
    text1 = (
        TextElement("高品質テスト！", size=60, color=(255, 255, 255))
            .set_background((100, 150, 200), alpha=200, padding=20)
            .set_corner_radius(15)  # This should be smooth at higher quality
            .position(100, 100)
            .start_at(0)
            .set_duration(3)
    )
    scene.add(text1)
    
    # Test text with different corner radius
    text2 = (
        TextElement("Corner Radius Test", size=40, color=(255, 255, 0))
            .set_background((200, 100, 100), alpha=180, padding=15)
            .set_corner_radius(25)  # Larger radius
            .position(100, 250)
            .start_at(0)
            .set_duration(3)
    )
    scene.add(text2)
    
    # Test positioned elements to ensure they don't appear small or misplaced
    text3 = (
        TextElement("位置テスト", size=50, color=(0, 255, 0))
            .set_background((50, 50, 150), alpha=220, padding=10)
            .set_corner_radius(8)
            .position(960, 540, anchor="center")  # Center of 1920x1080
            .start_at(0)
            .set_duration(3)
    )
    scene.add(text3)
    
    # Test bottom-right positioned element
    text4 = (
        TextElement("右下", size=35, color=(255, 0, 255))
            .set_background((150, 150, 50), alpha=200, padding=8)
            .set_corner_radius(12)
            .position(1820, 980, anchor="bottom-right")
            .start_at(0)
            .set_duration(3)
    )
    scene.add(text4)
    
    return scene

def test_quality_level(quality: str):
    """Test a specific quality level."""
    print(f"\n=== Testing quality: {quality} ===")
    
    # Create master scene with specified quality
    master_scene = MasterScene(width=1920, height=1080, fps=30, quality=quality)
    master_scene.set_output(f"quality_test_{quality}.mp4")
    
    # Add test scene
    scene = create_test_scene()
    master_scene.add(scene)
    
    print(f"Render scale for {quality}: {master_scene.render_scale}x")
    print(f"Render dimensions: {master_scene.render_width} x {master_scene.render_height}")
    print(f"Output dimensions: {master_scene.width} x {master_scene.height}")
    
    # Render the video
    try:
        master_scene.render()
        print(f"✓ Successfully rendered {quality} quality video")
    except Exception as e:
        print(f"✗ Error rendering {quality} quality: {e}")
        raise

def main():
    """Run quality tests for all levels."""
    print("FrameKit Quality Settings Test")
    print("==============================")
    
    # Test all quality levels
    quality_levels = ["low", "medium", "high"]
    
    for quality in quality_levels:
        test_quality_level(quality)
    
    print("\n=== Test Results ===")
    print("Check the output videos:")
    print("- quality_test_low.mp4 (1x rendering - current behavior)")
    print("- quality_test_medium.mp4 (2x supersampling)")  
    print("- quality_test_high.mp4 (4x supersampling)")
    print("\nLook for:")
    print("1. Smooth text rendering (no jagged edges)")
    print("2. Smooth corner radius (no pixelated curves)")
    print("3. Correct element positioning and sizing")
    print("4. No elements appearing small or misplaced")

if __name__ == "__main__":
    main()