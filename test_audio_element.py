import os
import warnings

# Pygame関連の環境変数を事前に設定
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# pkg_resources警告を抑制
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*pkg_resources.*")

from master_scene import MasterScene
from scene import Scene
from text_element import TextElement
from audio_element import AudioElement


def main():
    """Test audio element functionality"""
    # Create master scene
    master_scene = MasterScene(width=1920, height=1080, fps=30)
    master_scene.set_output("audio_test.mp4")
    
    # Create main scene
    scene = Scene()
    
    # Add a simple text element
    text = (
        TextElement("Audio Element Test", size=100, color=(255, 255, 255))
            .set_background((0, 100, 200), alpha=200, padding=40)
            .set_corner_radius(15)
            .set_alignment('center')
            .position(960, 540)
            .set_duration(10)
            .start_at(0)
    )
    scene.add(text)
    
    # Test audio element creation (even without actual audio file)
    try:
        # Create audio element (will warn about missing file but won't crash)
        audio = (
            AudioElement("sample_asset/sample.mp3")
                .set_volume(0.8)
                .start_at(0)
                # Duration will be set automatically from audio file
        )
        scene.add(audio)
        
        print(f"Audio element created:")
        print(f"- Path: {audio.audio_path}")
        print(f"- Volume: {audio.volume}")
        print(f"- Duration: {audio.duration}")
        print(f"- Start time: {audio.start_time}")
        print(f"- Size: {audio.width}x{audio.height} (should be 0x0 for audio)")
        
        # Test getting audio data at different times
        for time in [0.5, 2.0, 5.0]:
            audio_data = audio.get_audio_data_at_time(time)
            if audio_data:
                print(f"Audio data at {time}s: {audio_data}")
        
    except Exception as e:
        print(f"Error testing audio element: {e}")
    
    # Add scene to master scene
    master_scene.add(scene)
    
    # Execute rendering
    print("Rendering video with audio element test...")
    master_scene.render()
    print("Video completed: audio_test.mp4")


if __name__ == "__main__":
    main()