# PYTHONPATH=$(pwd) python3 -m tests.basic

from typing import Optional
from framekit.master_scene_element import MasterScene
from framekit.scene_element import Scene
from framekit.text_element import TextElement
from framekit.audio_element import AudioElement
from framekit.image_element import ImageElement
from framekit.video_element import VideoElement

def create_dialogue_subtitle(text: str, start_time: float, duration: float = 4.0, 
                           font_path: Optional[str] = None, bold: bool = True) -> TextElement:
    """Create a centered subtitle with yukkuri style formatting.
    
    Args:
        text: Text content for the subtitle
        start_time: Start time in seconds
        duration: Duration in seconds
        font_path: Optional path to custom font
        bold: Whether to use bold text
        
    Returns:
        Configured TextElement for the subtitle
    """
    subtitle = (
        TextElement(text, size=42, color=(255, 255, 255), font_path=font_path, bold=bold)
            .set_background((0, 0, 0), alpha=200, padding={'top': 12, 'bottom': 12, 'left': 25, 'right': 25})
            .set_corner_radius(10)
            .set_alignment('center')
            .set_line_spacing(6)
            .start_at(start_time)
            .set_duration(duration)
    )
    
    # Position at bottom center of screen
    subtitle_x = (1920 - subtitle.width) // 2
    subtitle_y = 950  # Bottom area for yukkuri style
    subtitle.position(subtitle_x, subtitle_y)
    
    return subtitle

def main() -> None:
    """Main function to create and render a Japanese dialogue video.
    
    Creates a yukkuri-style video with character sprites, background images,
    Japanese dialogue subtitles, and background music.
    """
    # === Assets ===
    BG_IMAGE = "sample_asset/bg.jpg"
    BG_VIDEO = "sample_asset/bg.mp4"
    EARTH_IMAGE = "sample_asset/earth.jpg"
    REIMU_SPRITE = "sample_asset/reimu.png"
    MARISA_SPRITE = "sample_asset/marisa.png"
    BGM_FILE = "sample_asset/yukkuri_bgm.mp3"
    OUTPUT_FILE = "yukkuri_dialogue.mp4"
    FONT_PATH = "sample_asset/NotoSansJP-VariableFont_wght.ttf"  # 日本語フォント
    
    # === Video Settings ===
    VIDEO_WIDTH = 1920
    VIDEO_HEIGHT = 1080
    VIDEO_FPS = 30
    # VIDEO_DURATION = 60
    
    # === Character Positions ===
    REIMU_POS = (100, 200)
    MARISA_POS = (1400, 200)
    CHARACTER_SCALE = 0.8
    
    # === Dialogue Script ===
    dialogues = [
        ("こんにちは！今日は地球について解説するのだ！", 2, 4),
        ("よろしくね～。地球は太陽系の第3惑星なのぜ。", 6, 4),
        ("地球の直径は約12,742キロメートルで、\n表面の71%が海で覆われているのだ。", 10, 5),
        ("そうそう！そして地球には約80億人の人間が\n住んでいるのぜ～", 15, 5),
        ("地球の大気は窒素が78%、酸素が21%で\n残りの1%がその他のガスなのだ。", 20, 5),
        ("この絶妙なバランスが生命を育んでいるのぜ！", 25, 4),
        ("地球は約46億年前に誕生して、\n生命が現れたのは約35億年前なのだ。", 29, 5),
        ("すごく長い歴史があるのぜ～\n人類はまだ新参者なのだ。", 34, 4),
        ("地球の自転周期は24時間、\n公転周期は365.25日なのだ。", 38, 4),
        ("だから1年は365日で、4年に1度\nうるう年があるのぜ！", 42, 4),
        ("地球は本当に美しい惑星なのだ。\n大切にしなければいけないぜ。", 46, 5),
        ("今日の地球解説はここまでなのぜ！\nまた次回も見てくれよな～", 51, 5),
    ]
    
    # Create master scene
    master_scene = MasterScene(width=VIDEO_WIDTH, height=VIDEO_HEIGHT, fps=VIDEO_FPS)
    master_scene.set_output(OUTPUT_FILE)
    
    # Create main scene
    scene = Scene()
    
    bg = (
        VideoElement(BG_VIDEO)
            .set_scale(1.0)
            .start_at(0)
            # .set_duration(VIDEO_DURATION)
            .set_crop(1920, 1080)
            .set_loop_until_scene_end()
    )
    scene.add(bg)
    
    # Background - Earth image (centered)
    earth = (
        ImageElement(EARTH_IMAGE)
            .set_scale(1.0)
            .start_at(0)
            # .set_duration(VIDEO_DURATION)
            .position(VIDEO_WIDTH//2, VIDEO_HEIGHT//2, anchor="center")
            .set_crop(800, 600)
    )
    scene.add(earth)
    
    # video = (
    #     VideoElement(BG_VIDEO)
    #         .set_scale(0.5)
    # )
    # scene.add(video)
    
    # Character sprites
    # Reimu (left side)
    reimu = (
        ImageElement(REIMU_SPRITE)
            .position(200, 900, "center")
            .set_scale(CHARACTER_SCALE)
            .start_at(0)
            # .set_duration(VIDEO_DURATION)
            .set_crop(200, 200)
    )
    scene.add(reimu)
    
    # Marisa (right side)
    marisa = (
        ImageElement(MARISA_SPRITE)
            .position(1720, 900, "center")
            .set_scale(CHARACTER_SCALE)
            .start_at(0)
            # .set_duration(VIDEO_DURATION)
            .set_crop(200, 200)
    )
    scene.add(marisa)
    
    # Add all dialogue subtitles
    for text, start_time, duration in dialogues:
        subtitle = create_dialogue_subtitle(text, start_time, duration, font_path=FONT_PATH)
        scene.add(subtitle)
    
    # Background music
    bgm = (
        AudioElement(BGM_FILE)
            # .set_volume(0.2)
            .set_loop_until_scene_end(True)
            .start_at(0)
    )
    scene.add(bgm)
    
    # Add scene to master scene and render
    master_scene.add(scene)
    master_scene.render()

if __name__ == "__main__":
    main()