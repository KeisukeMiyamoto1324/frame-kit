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
from image_element import ImageElement
from video_element import VideoElement


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


def main():
    """Yukkuri-style educational video about Computer Science History"""
    # Create master scene - 2 minute video at 30fps
    master_scene = MasterScene(width=1920, height=1080, fps=30)
    master_scene.set_output("computer_science_history.mp4")
    
    # Create main scene
    scene = Scene()
    
    # Title sequence
    title = (
        TextElement("The History of\nComputer Science", size=80, color=(255, 255, 255))
            .set_background((20, 50, 100), alpha=200, padding=40)
            .set_border((255, 255, 255), width=3)
            .set_corner_radius(20)
            .set_alignment('center')
            .set_line_spacing(10)
            .set_duration(5)
            .start_at(0)
    )
    title_x = (1920 - title.width) // 2
    title_y = (1080 - title.height) // 2
    title.position(title_x, title_y)
    scene.add(title)
    
    video = (
        VideoElement("sample_asset/sample1.mp4")
            .set_scale(0.5)
    )
    scene.add(video)
    
    # Series of educational subtitles with proper line breaks
    subtitles = [
        ("Welcome to today's lesson about\nthe fascinating history of computer science!", 5, 4),
        ("Computer science didn't start with modern computers.\nIt began with ancient mathematical concepts\nand calculation methods.", 9, 5),
        ("In the 1940s, pioneers like Alan Turing\nand John von Neumann laid the foundations\nfor modern computing theory.", 14, 5),
        ("Turing's work on computability and\nthe famous Turing Machine concept\nrevolutionized our understanding of computation.", 19, 6),
        ("The 1950s saw the birth of programming languages.\nFORTRAN, created by John Backus at IBM,\nwas one of the first high-level languages.", 25, 6),
        ("In 1969, ARPANET was created,\nconnecting computers across universities.\nThis became the foundation of the Internet.", 31, 6),
        ("The 1970s brought personal computing closer.\nCompanies like Apple and Microsoft\nstarted in garages and basements.", 37, 5),
        ("Object-oriented programming emerged\nwith languages like Smalltalk and C++,\nchanging how we structure code.", 42, 5),
        ("The 1990s introduced the World Wide Web,\ncreated by Tim Berners-Lee at CERN.\nThis transformed global communication.", 47, 6),
        ("Today, computer science encompasses\nartificial intelligence, quantum computing,\nand distributed systems.", 53, 5),
        ("Machine learning and neural networks,\nonce theoretical concepts,\nnow power everyday applications.", 58, 5),
        ("From simple calculations to complex AI,\ncomputer science continues to evolve\nand shape our future.", 63, 5),
        ("The journey from mechanical calculators\nto quantum computers shows\nhuman ingenuity and progress.", 68, 5),
        ("Understanding this history helps us\nappreciate modern technology\nand envision future possibilities.", 73, 5),
        ("Thank you for watching this brief journey\nthrough computer science history!\nKeep learning and exploring!", 78, 6)
    ]
    
    # Add all subtitles to the scene
    for text, start_time, duration in subtitles:
        subtitle = create_subtitle(text, start_time, duration)
        scene.add(subtitle)
    
    # Add decorative elements
    for i in range(5):
        decoration = (
            TextElement("◆", size=60, color=(100, 150, 255))
                .position(100 + i * 400, 50)
                .start_at(i * 2)
                .set_duration(8)
        )
        scene.add(decoration)
        
    # Add scene to master scene
    master_scene.add(scene)
    
    # Execute rendering
    print("Creating a 2-minute educational video about Computer Science History...")
    print("This video will include properly formatted subtitles with line breaks.")
    master_scene.render()
    print("Video completed: computer_science_history.mp4")


if __name__ == "__main__":
    main()