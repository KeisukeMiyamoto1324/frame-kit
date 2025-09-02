import os
from master_scene import MasterScene
from scene import Scene
from text_element import TextElement
from audio_element import AudioElement
from image_element import ImageElement
from animation import AnimationPresets

def create_subtitle(text, start_time, duration=4.0):
    """Create a centered subtitle at the bottom of the screen"""
    subtitle = (
        TextElement(text, size=48, color=(255, 255, 255))
            .set_background((0, 0, 0), alpha=180, padding={'top': 15, 'bottom': 15, 'left': 30, 'right': 30})
            .set_corner_radius(12)
            .set_alignment('center')
            .set_line_spacing(8)
            .start_at(start_time)
            .set_duration(duration)
    )
    
    # Position at bottom center of screen
    subtitle_x = (1920 - subtitle.width) // 2
    subtitle_y = 900  # Bottom area of 1080p screen
    subtitle.position(subtitle_x, subtitle_y)
    
    return subtitle

def create_title(text, start_time, duration=3.0):
    """Create a large centered title"""
    title = (
        TextElement(text, size=80, color=(255, 255, 255))
            .set_background((30, 144, 255), alpha=200, padding={'top': 25, 'bottom': 25, 'left': 50, 'right': 50})
            .set_corner_radius(20)
            .set_alignment('center')
            .start_at(start_time)
            .set_duration(duration)
    )
    
    title_x = (1920 - title.width) // 2
    title_y = (1080 - title.height) // 2
    title.position(title_x, title_y)
    
    return title

def main():
    # Create master scene with 1920x1080 resolution at 30fps
    master_scene = MasterScene(width=1920, height=1080, fps=30)
    master_scene.set_output("computer_science_history.mp4")
    
    # Create main scene
    scene = Scene()
    
    # Add background image
    background = (
        ImageElement("sample_asset/bg.png")
            .set_crop(1920, 1080, mode='fill')  # Fill entire 1080p screen
            .position(0, 0)  # Position at top-left
            .start_at(0)
    )
    scene.add(background)
    
    # Add background music
    bgm = (
        AudioElement("sample_asset/sample-bgm.mp3")
            .set_volume(0.3)  # Set to 50% volume for background
            .set_loop_until_scene_end(True)  # Loop until scene ends
            .start_at(0)
    )
    scene.add(bgm)
    
    # Title sequence
    main_title = create_title("The History of Computer Science", 1, 4)
    scene.add(main_title)
    
    # Subtitle sequence with computer science history
    subtitles = [
        ("Welcome to the fascinating journey\nthrough the history of computer science!", 6, 4),
        ("Computer science didn't start with modern computers.\nIt began with ancient mathematical concepts.", 11, 5),
        ("Around 300 BC, Euclid developed algorithms\nfor finding the greatest common divisor.", 17, 5),
        ("In the 9th century, Persian mathematician\nAl-Khwarizmi gave us the word 'algorithm'.", 23, 5),
        ("The 1600s brought us binary numbers\nthanks to Gottfried Leibniz.", 29, 4),
        ("Charles Babbage designed the first\nmechanical computer in the 1830s.", 34, 4),
    ]
    
    for text, start_time, duration in subtitles:
        subtitle = create_subtitle(text, start_time, duration)
        scene.add(subtitle)
    
    # Add some chapter titles with sound effects
    chapter_titles = [
        ("Ancient Origins", 16, 2),
        ("Mechanical Era", 33, 2),
        ("Electronic Age", 44, 2),
        ("Modern Computing", 61, 2),
        ("Future Frontiers", 72, 2)
    ]
    
    for text, start_time, duration in chapter_titles:
        # Add sound effect for each chapter
        effect_sound = (
            AudioElement("sample_asset/sample-effect.mp3")
                .set_volume(1.0)  # Full volume for effect to be clearly audible
                .set_duration(2.0)  # Explicit duration for effect sound
                .start_at(start_time)
        )
        scene.add(effect_sound)
        
        chapter_title = (
            TextElement(text, size=60, color=(255, 215, 0))
                .set_background((0, 0, 0), alpha=150, padding=20)
                .set_corner_radius(15)
                .set_alignment('center')
                .start_at(start_time)
                .set_duration(duration)
        )
        chapter_title_x = (1920 - chapter_title.width) // 2
        chapter_title_y = 200
        chapter_title.position(chapter_title_x, chapter_title_y)
        scene.add(chapter_title)
    
    # 犬の画像（4000x3000px → 0.1倍で400x300px）をテロップの上、画面右側に配置
    dog_pulse = (
        ImageElement("sample_asset/dog.jpg")
            # .set_scale(0.5)
            # .set_border([127, 127, 127], 5)
            .position(100, 100)
            .set_duration(master_scene.total_duration or 90)
            .start_at(0)
            .animate_pulse_until_end(
                from_scale=0.3,
                to_scale=0.45,
                duration=1.5,
                repeat_delay=0.1,
                scene_duration=master_scene.total_duration or 90
            )
            .set_corner_radius(20)
    )
    scene.add(dog_pulse)
    
    # Add scene to master scene
    master_scene.add(scene)
    
    # Set background duration to match total duration
    background.set_duration(master_scene.total_duration)
    
    print("Starting to render computer science history video...")
    master_scene.render()
    print("Video rendering complete! Check output/computer_science_history.mp4")

if __name__ == "__main__":
    main()