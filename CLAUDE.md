# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based video editor that programmatically generates videos using OpenGL rendering and text elements. The project creates video content by composing scenes with various elements like text overlays and renders them to MP4 files.

## Development Setup

The project uses a Python virtual environment:
- **Virtual Environment**: `venv/` directory contains the Python virtual environment  
- **Python Version**: Python 3.12
- **Main Entry Points**: 
  - `main.py`: Educational video demo with subtitles and timing
  - `test_telop_features.py`: Advanced telop features demo (backgrounds, borders, multiline text)
  - `test_corner_radius.py`: Corner radius demo for all element types

### Running the Application

```bash
# Activate the virtual environment (macOS/Linux)
source venv/bin/activate

# Run the main educational video demo (2-minute computer science history)
python main.py

# Run telop features demo (text with backgrounds, borders, multiline)
python tests/test_telop_features.py

# Run corner radius demo (rounded corners for all element types) 
python tests/test_corner_radius.py

# Test audio functionality (video with audio controls)
python tests/test_video_audio.py

# Test BGM (background music) looping functionality
python tests/test_bgm_simple.py
python tests/test_bgm_comprehensive.py
python tests/test_bgm_termination.py
```

### Development Commands

Since this is a Python project without build tools, development primarily involves:
- **Activate environment**: `source venv/bin/activate`
- **Run demos**: `python main.py` or other test files
- **Install dependencies**: `pip3 install <package>` (avoid `pip`, use `pip3`)
- **Check outputs**: Generated videos appear in `output/` directory

### Key Dependencies

Core libraries required for video generation:
- **pygame**: Window management and OpenGL context
- **PyOpenGL**: Low-level OpenGL graphics rendering  
- **numpy**: Array operations for image data
- **opencv-python**: Video encoding and file output
- **pillow**: Text rendering and image manipulation
- **tqdm**: Progress bars during rendering

Audio processing dependencies:
- **FFmpeg**: Required for audio mixing and video export with sound (install via `brew install ffmpeg` on macOS)
- **mutagen**: Audio metadata extraction (optional: `pip3 install mutagen`)
- **librosa**: Audio analysis and processing (optional: `pip3 install librosa`)

## Core Architecture

The video editor is built around a modular class-based architecture with inheritance patterns:

### Class Hierarchy and Rendering Pipeline

The architecture follows a clear inheritance structure where all visual elements extend `VideoBase`, providing consistent positioning, timing, and visual effects across all element types. The rendering pipeline uses OpenGL for real-time graphics with off-screen rendering to generate video files.

### Core Components

1. **VideoBase** (`video_base.py`): Base class for all video elements
   - Handles positioning, timing, and visibility logic
   - Provides fluent interface methods (position, set_duration, start_at)
   - All elements inherit from this class

2. **TextElement** (`text_element.py`): Text rendering component
   - Creates OpenGL textures from text using PIL/Pillow
   - Supports custom fonts, colors, and sizes
   - Handles macOS system font fallback (Arial.ttf → Helvetica.ttc → default)
   - Lazy texture creation (only when OpenGL context is available)

3. **ImageElement** (`image_element.py`): Image rendering component
   - Loads and renders static image files (JPG, PNG, etc.)
   - Supports image scaling and alpha transparency
   - Uses PIL for image loading and OpenGL for texture rendering
   - Lazy texture creation with deferred loading

4. **VideoElement** (`video_element.py`): Video clip rendering component
   - Renders video files frame-by-frame using OpenCV
   - Supports video scaling and frame-accurate timing
   - Handles video format conversion (BGR to RGB) and alpha channel
   - Frame caching and OpenGL texture updates per render frame
   - **Audio Integration**: Automatically creates associated AudioElement for video soundtrack
   - **Audio Control**: Provides volume, fade, and mute controls for video audio

5. **AudioElement** (`audio_element.py`): Audio playback component
   - Handles standalone audio files (MP3, WAV, etc.) and video soundtracks
   - Supports volume control, fade in/out, and mute/unmute functionality
   - **BGM Mode**: `set_loop_until_scene_end(True)` loops audio until scene ends
   - Uses mutagen or librosa for audio metadata extraction
   - Integrates with FFmpeg for final audio mixing and synchronization

6. **Scene** (`scene.py`): Container for multiple video elements
   - Groups elements and manages their collective timing
   - Handles scene-relative time calculations
   - Can be positioned at specific times in the timeline
   - **BGM Management**: Automatically adjusts BGM duration to match scene length

7. **MasterScene** (`master_scene.py`): Main video composition manager
   - Handles overall video settings (width, height, fps, output filename)
   - Manages pygame/OpenGL context and rendering pipeline
   - Exports final video using OpenCV with progress tracking
   - Hidden window rendering using SDL video driver settings
   - **Audio Processing**: Integrates with FFmpeg for audio mixing and synchronization
   - **Multi-track Audio**: Supports multiple audio sources with volume control and timing

### Project Structure

```
video-editer/
├── main.py              # Educational video demo with complex subtitles
├── test_telop_features.py # Advanced telop features demo  
├── test_corner_radius.py # Corner radius demo
├── video_base.py        # Base class with positioning, timing, effects
├── text_element.py      # Text rendering with PIL/OpenGL integration
├── image_element.py     # Static image rendering with scaling
├── video_element.py     # Frame-by-frame video clip rendering with audio
├── audio_element.py     # Audio playback and BGM management  
├── scene.py             # Scene container for element grouping
├── master_scene.py      # OpenGL context and video export manager
├── tests/               # Test files for various functionality
├── sample_asset/        # Sample media files (images, videos)
├── output/              # Generated MP4 video files
├── prompt.txt           # Development notes (Japanese)
└── venv/                # Python virtual environment
```

### Key Architectural Patterns

- **Fluent Interface**: All elements use method chaining (`.position().set_duration().start_at()`)
- **Lazy Loading**: OpenGL textures created only when rendering context exists  
- **Inheritance**: Common functionality in `VideoBase` (positioning, timing, effects)
- **Composition**: Scenes group elements, MasterScene manages overall composition
- **Frame-accurate Timing**: Video elements handle precise frame synchronization

### Output Structure

- Videos are saved to the `output/` directory (auto-created)
- Default output format is MP4 with mp4v codec
- Example outputs: 
  - `output/computer_science_history.mp4` (main.py educational video)
  - `output/telop_features_demo.mp4` (advanced telop demo)
  - `output/corner_radius_test.mp4` (corner radius demo)

## Development Patterns

### Creating Video Elements

Elements use a fluent interface pattern:
```python
# Basic text element
text = (
    TextElement("Hello", size=100, color=(255, 0, 0))
        .position(960, 540)
        .set_duration(3)
        .start_at(1)
)

# Text with background and border (telop style)
telop = (
    TextElement("Breaking News", size=60, color=(255, 255, 255))
        .set_background((255, 0, 0), alpha=200, padding=20)
        .set_border((255, 255, 255), width=2)
        .set_corner_radius(15)
        .position(100, 100)
        .set_duration(5)
)

# Multiline text with alignment
multiline = (
    TextElement("Line 1\nLine 2\nLine 3", size=50, color=(0, 255, 0))
        .set_alignment('center')
        .set_line_spacing(10)
        .position(500, 300)
        .set_duration(4)
)

# Image element with border and corner radius
image = (
    ImageElement("sample_asset/sample.jpg")
        .position(500, 500)
        .set_scale(0.5)
        .set_border((127, 127, 127))
        .set_corner_radius(20)
        .set_duration(4)
        .start_at(0.5)
)

# Video element with border, corner radius, and audio control
video = (
    VideoElement("sample_asset/sample.mp4")
        .position(100, 100)
        .set_scale(0.3)
        .set_border((127, 127, 127))
        .set_corner_radius(25)
        .set_volume(0.8)  # 80% volume
        .set_audio_fade_in(2.0)  # 2 second fade in
        .set_duration(6)
        .start_at(1.5)
)

# Standalone audio element (BGM)
bgm = (
    AudioElement("sample_asset/background_music.mp3")
        .set_volume(0.3)  # Lower volume for background
        .set_loop_until_scene_end(True)  # Loop until scene ends
        .start_at(0)
)
```

### Scene Composition

Scenes are built by adding elements and then adding scenes to the master scene:
```python
scene = Scene()
scene.add(text_element)
master_scene.add(scene)
```

### Complete Video Creation Example

```python
from master_scene import MasterScene
from scene import Scene  
from text_element import TextElement
from image_element import ImageElement
from video_element import VideoElement

# Create master scene
master_scene = MasterScene(width=1920, height=1080, fps=30)
master_scene.set_output("my_video.mp4")

# Create and populate scene
scene = Scene()
text = TextElement("Hello World", size=100, color=(255, 0, 0)).position(960, 540)
image = ImageElement("sample_asset/image.jpg").position(500, 500).set_scale(0.5)
video = VideoElement("sample_asset/video.mp4").position(100, 100).set_scale(0.3)

scene.add(text)
scene.add(image) 
scene.add(video)
scene.add(bgm)  # Add background music

# Render video
master_scene.add(scene)
master_scene.render()
```

### Subtitle Creation Pattern

For educational videos with synchronized subtitles, use this pattern from `main.py`:

```python
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

# Usage with timed subtitles
subtitles = [
    ("Welcome to today's lesson about\nthe fascinating history of computer science!", 5, 4),
    ("Computer science didn't start with modern computers.\nIt began with ancient mathematical concepts\nand calculation methods.", 9, 5),
    # ... more subtitles
]

for text, start_time, duration in subtitles:
    subtitle = create_subtitle(text, start_time, duration)
    scene.add(subtitle)
```

### BGM (Background Music) Implementation Pattern

The codebase provides sophisticated BGM functionality that automatically handles audio looping and scene synchronization:

```python
# Basic BGM setup
bgm = (
    AudioElement("path/to/background_music.mp3")
        .set_volume(0.3)  # Lower volume for background
        .set_loop_until_scene_end(True)  # Enable BGM mode
        .start_at(0)  # Start immediately
)

# BGM behavior:
# - If BGM is shorter than scene: automatically loops until scene ends
# - If BGM is longer than scene: cuts off when scene ends  
# - BGM duration does NOT affect scene duration (other elements determine scene length)

# Multiple audio sources example
scene = Scene()
scene.add(bgm)  # Background music

# Video with its own audio (mixed with BGM)
video = (
    VideoElement("video_with_audio.mp4")
        .set_volume(0.6)  # Video audio at 60%
        .set_audio_fade_in(1.0)  # Smooth fade in
        .start_at(0)
        .set_duration(10)
)
scene.add(video)

# The final output will mix:
# - BGM looping at 30% volume
# - Video audio at 60% volume with fade in
# - Both synchronized using FFmpeg during final export
```

### Audio Integration Architecture

The audio system uses a composition pattern where:

1. **VideoElement** automatically creates an associated **AudioElement** for video soundtracks
2. **Scene** manages BGM duration adjustments based on scene length
3. **MasterScene** collects all audio sources and uses FFmpeg for final mixing
4. **FFmpeg Integration**: Handles complex audio operations like looping (`-stream_loop -1`), volume control (`volume=N`), and timing (`-itsoffset`)

### Coordinate System

- Uses pixel coordinates with origin at top-left (0, 0)
- Standard video dimensions: 1920x1080
- Text positioning is based on top-left corner of text bounds

## Platform Considerations

- **macOS**: Uses system fonts like Arial.ttf and Helvetica.ttc
- **Cross-platform**: Falls back to default fonts if system fonts unavailable  
- **Hidden Window**: Renders off-screen using SDL video driver settings
- **Environment**: Suppresses pygame support prompts and pkg_resources warnings  
- **Dependencies**: Always use `pip3` instead of `pip` for installations
- **Japanese Support**: Codebase includes Japanese comments and development notes in `prompt.txt`

### Audio Requirements

- **FFmpeg**: Required for audio mixing. Install via `brew install ffmpeg` (macOS) or system package manager
- **Audio Libraries**: Install `pip3 install mutagen` for audio metadata or `pip3 install librosa` for advanced audio processing
- **Audio Formats**: Supports MP3, WAV, AAC, and other common formats through FFmpeg
- **Video Audio**: Automatically extracts audio tracks from video files (MP4, MOV, etc.)

## Common Development Tasks

### Corner Radius Implementation

The codebase has a known issue with corner radius implementation for images and videos. When corner radius is applied to images or videos, the content in the rounded corners should not be displayed (masked out). This is mentioned in `prompt.txt` and needs to be addressed in the rendering pipeline.

### Video Timing and Synchronization

- Frame-accurate timing is handled automatically by `VideoElement`
- Subtitle timing uses floating-point seconds for precise control
- Use consistent fps settings (30 or 60) across all elements in a scene
- Educational videos typically use 30fps for smoother text rendering

## Element-Specific Methods

### All Elements (VideoBase)
- `.position(x, y)`: Set element position in pixels
- `.set_duration(seconds)`: Set how long element appears
- `.start_at(seconds)`: Set when element starts appearing
- `.set_corner_radius(radius)`: Set corner radius for rounded corners (0 = no rounding)

### TextElement
- Constructor: `TextElement(text, size=50, color=(255,255,255), font_path=None)`
- Supports RGB color tuples, automatic font fallback
- `.set_background(color, alpha=255, padding=5)`: Add background box with color and transparency
- `.set_border(color, width=1)`: Add border outline around text
- `.set_alignment(alignment)`: Set text alignment ('left', 'center', 'right') for multiline text
- `.set_line_spacing(spacing)`: Set spacing between lines in pixels for multiline text

### ImageElement  
- Constructor: `ImageElement(image_path, scale=1.0)`
- `.set_scale(scale)`: Resize image (1.0 = original size)
- `.set_border(color, width=1)`: Add border outline around image
- Supports common formats: JPG, PNG, etc.

### VideoElement
- Constructor: `VideoElement(video_path, scale=1.0)`  
- `.set_scale(scale)`: Resize video frames
- `.set_border(color, width=1)`: Add border outline around video
- Automatically handles video timing and frame extraction
- **Audio Control Methods**:
  - `.set_volume(volume)`: Set video audio volume (0.0-1.0+)
  - `.set_audio_fade_in(duration)`: Set audio fade in duration in seconds
  - `.set_audio_fade_out(duration)`: Set audio fade out duration in seconds
  - `.mute_audio()`: Mute video audio
  - `.unmute_audio()`: Unmute video audio
  - `.get_audio_volume()`: Get current audio volume

### AudioElement
- Constructor: `AudioElement(audio_path, volume=1.0)`
- `.set_volume(volume)`: Set audio volume (0.0-1.0+)
- `.set_fade_in(duration)`: Set fade in duration in seconds
- `.set_fade_out(duration)`: Set fade out duration in seconds
- `.mute()` / `.unmute()`: Mute/unmute audio
- **BGM Mode**: `.set_loop_until_scene_end(True)` - Loop audio until scene ends
- Supports MP3, WAV, and other common audio formats