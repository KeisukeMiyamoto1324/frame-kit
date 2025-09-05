# FrameKit

A powerful Python-based video editor for programmatic video generation using OpenGL rendering. Create professional videos with text overlays, images, video clips, and audio mixing through a clean, fluent API.

## Features

- **🎬 Video Composition**: Combine text, images, and video clips into professional videos
- **🎨 OpenGL Rendering**: High-performance graphics rendering with real-time effects
- **🎵 Audio Integration**: Multi-track audio mixing with BGM support and FFmpeg integration
- **📝 Rich Text**: Advanced text rendering with custom fonts, backgrounds, borders, and Japanese support
- **🎞️ Video Elements**: Frame-accurate video playback with audio control and visual effects
- **🎯 Animation System**: Smooth animations for position, scale, rotation, and opacity
- **🔄 Fluent API**: Method chaining for clean, readable code
- **🌐 Cross-Platform**: Works on macOS, Linux, and Windows

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/framekit.git
cd framekit

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip3 install -e .

# Install FFmpeg for audio processing (macOS)
brew install ffmpeg
```

### Basic Example

```python
from framekit import *

# Create master scene
master_scene = MasterScene(width=1920, height=1080, fps=30)
master_scene.set_output("my_video.mp4")

# Create elements with fluent API
title = (
    TextElement("Hello FrameKit!", size=100, color=(255, 255, 255))
        .set_background((255, 0, 0), alpha=200, padding=20)
        .set_corner_radius(15)
        .position(960, 540)
        .set_duration(5)
)

image = (
    ImageElement("assets/background.jpg")
        .set_scale(0.8)
        .set_corner_radius(20)
        .position(100, 100)
        .set_duration(5)
)

# Compose scene
scene = Scene()
scene.add(title)
scene.add(image)

# Render video
master_scene.add(scene)
master_scene.render()
```

## Examples

### Japanese Dialogue Video

Create educational videos with character sprites and subtitles:

```python
from framekit import *

def create_dialogue_subtitle(text, start_time, duration=4.0):
    return (
        TextElement(text, size=42, color=(255, 255, 255))
            .set_background((0, 0, 0), alpha=200, padding=20)
            .set_corner_radius(10)
            .set_alignment('center')
            .position(960, 950)  # Bottom center
            .start_at(start_time)
            .set_duration(duration)
    )

# Japanese dialogue with timing
dialogues = [
    ("こんにちは！今日は地球について解説するのだ！", 2, 4),
    ("よろしくね～。地球は太陽系の第3惑星なのぜ。", 6, 4),
]

scene = Scene()
for text, start_time, duration in dialogues:
    subtitle = create_dialogue_subtitle(text, start_time, duration)
    scene.add(subtitle)
```

### Video with Audio Control

```python
# Video element with audio control
video = (
    VideoElement("sample_video.mp4")
        .position(100, 100)
        .set_scale(0.5)
        .set_corner_radius(25)
        .set_volume(0.8)  # 80% volume
        .set_audio_fade_in(2.0)  # 2 second fade in
        .set_duration(10)
)

# Background music that loops
bgm = (
    AudioElement("background_music.mp3")
        .set_volume(0.3)  # Lower volume for background
        .set_loop_until_scene_end(True)  # Loop until scene ends
        .start_at(0)
)

scene = Scene()
scene.add(video)
scene.add(bgm)
```

### Animations

```python
from framekit.animation import LinearAnimation, EasingAnimation

# Text with slide-in animation
text = TextElement("Animated Text!", size=80, color=(0, 255, 0))

# Position animation (slide from left)
slide_in = LinearAnimation(
    start_value=(0, 400), 
    end_value=(500, 400), 
    duration=2.0
)
text.add_position_animation(slide_in)

# Scale animation (grow effect)
grow = EasingAnimation(
    start_value=0.5, 
    end_value=1.0, 
    duration=1.5,
    easing_type='ease_out'
)
text.add_scale_animation(grow)

# Fade in
fade_in = LinearAnimation(start_value=0, end_value=255, duration=1.0)
text.add_alpha_animation(fade_in)
```

## Core Components

### VideoBase
Base class for all video elements providing:
- Position and timing control
- Fluent interface methods
- Animation support
- Visual effects (corner radius, borders)

### Elements

- **TextElement**: Rich text with custom fonts, backgrounds, borders, and multi-line support
- **ImageElement**: Static image rendering with scaling and visual effects
- **VideoElement**: Video clip playback with frame-accurate timing and audio control
- **AudioElement**: Audio playback with volume control, fading, and BGM looping

### Composition

- **Scene**: Container for grouping elements with relative timing
- **MasterScene**: Main composition manager handling OpenGL context and video export

### Animation System

- **LinearAnimation**: Smooth linear transitions
- **EasingAnimation**: Natural easing curves (ease_in, ease_out, ease_in_out)
- **BounceAnimation**: Bouncing effects
- **Animation Manager**: Coordinate multiple animations per element

## Advanced Features

### Multi-track Audio
```python
# Multiple audio sources mixed automatically
scene.add(bgm)           # Background music
scene.add(video_with_audio)  # Video soundtrack
scene.add(sound_effect)  # Additional sound effects
# All mixed with FFmpeg during export
```

### Professional Text Styling
```python
telop = (
    TextElement("Breaking News", size=60, color=(255, 255, 255))
        .set_background((255, 0, 0), alpha=200, padding=20)
        .set_border((255, 255, 255), width=2)
        .set_corner_radius(15)
        .set_alignment('center')
        .set_line_spacing(10)
)
```

### Frame-Accurate Video Timing
```python
video = (
    VideoElement("precise_timing.mp4")
        .start_at(1.5)  # Start at exactly 1.5 seconds
        .set_duration(6.25)  # Duration to exact frame
        .set_scale(0.8)
)
```

## Architecture

FrameKit uses a modern, modular architecture:

- **Package Structure**: Clean Python package with proper imports
- **Inheritance Hierarchy**: All elements extend `VideoBase`
- **Lazy Loading**: OpenGL resources created only when needed
- **Type Safety**: Full type hints with generic support
- **Fluent Interface**: Method chaining with proper type preservation

## Requirements

### Core Dependencies
- Python 3.12+
- pygame (OpenGL context)
- PyOpenGL (graphics rendering)
- opencv-python (video encoding)
- pillow (text/image processing)
- numpy (array operations)

### Audio Processing
- FFmpeg (required for audio mixing)
- mutagen (optional: audio metadata)
- librosa (optional: audio analysis)

### Installation
```bash
# Install FFmpeg
# macOS:
brew install ffmpeg
# Ubuntu/Debian:
sudo apt-get install ffmpeg
# Windows: Download from https://ffmpeg.org/

# Install optional audio libraries
pip3 install mutagen librosa
```

## Running Examples

```bash
# Activate virtual environment
source venv/bin/activate

# Run the Japanese dialogue demo
PYTHONPATH=$(pwd) python3 -m tests.basic

# Or install in development mode
pip3 install -e .
python3 -m tests.basic

# Check output
ls output/  # Generated videos appear here
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with OpenGL for high-performance graphics
- Uses FFmpeg for professional audio processing
- Inspired by modern video editing workflows
- Supports Japanese content creation

---

**Create professional videos programmatically with FrameKit's intuitive Python API**