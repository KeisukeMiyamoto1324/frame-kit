# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based video editor that programmatically generates videos using OpenGL rendering and text elements. The project creates video content by composing scenes with various elements like text overlays and renders them to MP4 files.

## Development Setup

The project uses a Python virtual environment:
- **Virtual Environment**: `venv/` directory contains the Python virtual environment  
- **Python Version**: Python 3.12
- **Main Entry Points**: 
  - `main.py`: Basic demo with text, image, and video elements
  - `test_telop_features.py`: Advanced telop features demo (backgrounds, borders, multiline text)
  - `test_corner_radius.py`: Corner radius demo for all element types

### Running the Application

```bash
# Activate the virtual environment (macOS/Linux)
source venv/bin/activate

# Run the main video editor demo
python main.py

# Run telop features demo (text with backgrounds, borders, multiline)
python test_telop_features.py

# Run corner radius demo (rounded corners for all element types)
python test_corner_radius.py
```

### Key Dependencies

Core libraries required for video generation:
- **pygame**: Window management and OpenGL context
- **PyOpenGL**: Low-level OpenGL graphics rendering  
- **numpy**: Array operations for image data
- **opencv-python**: Video encoding and file output
- **pillow**: Text rendering and image manipulation
- **tqdm**: Progress bars during rendering

## Core Architecture

The video editor is built around a modular class-based architecture:

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

5. **Scene** (`scene.py`): Container for multiple video elements
   - Groups elements and manages their collective timing
   - Handles scene-relative time calculations
   - Can be positioned at specific times in the timeline

6. **MasterScene** (`master_scene.py`): Main video composition manager
   - Handles overall video settings (width, height, fps, output filename)
   - Manages pygame/OpenGL context and rendering pipeline
   - Exports final video using OpenCV with progress tracking
   - Hidden window rendering using SDL video driver settings

### Project Structure

```
video-editer/
├── main.py              # Basic demo script 
├── test_telop_features.py # Advanced telop features demo
├── test_corner_radius.py # Corner radius demo
├── video_base.py        # Base class for all video elements
├── text_element.py      # Text rendering implementation
├── image_element.py     # Image rendering implementation
├── video_element.py     # Video clip rendering implementation
├── scene.py             # Scene container class
├── master_scene.py      # Main video composition manager
├── sample_asset/        # Sample media files (images, videos)
├── output/              # Generated video files
├── prompt.txt           # Development notes and planned features
└── venv/                # Python virtual environment
```

### Output Structure

- Videos are saved to the `output/` directory (auto-created)
- Default output format is MP4 with mp4v codec
- Example outputs: 
  - `output/text_image_video_demo.mp4` (basic demo)
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

# Video element with border and corner radius
video = (
    VideoElement("sample_asset/sample.mp4")
        .position(100, 100)
        .set_scale(0.3)
        .set_border((127, 127, 127))
        .set_corner_radius(25)
        .set_duration(6)
        .start_at(1.5)
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
master_scene = MasterScene(width=1920, height=1080, fps=60)
master_scene.set_output("my_video.mp4")

# Create and populate scene
scene = Scene()
text = TextElement("Hello World", size=100, color=(255, 0, 0)).position(960, 540)
image = ImageElement("sample_asset/image.jpg").position(500, 500).set_scale(0.5)
video = VideoElement("sample_asset/video.mp4").position(100, 100).set_scale(0.3)

scene.add(text)
scene.add(image)
scene.add(video)

# Render video
master_scene.add(scene)
master_scene.render()
```

### Coordinate System

- Uses pixel coordinates with origin at top-left (0, 0)
- Standard video dimensions: 1920x1080
- Text positioning is based on top-left corner of text bounds

## Platform Considerations

- **macOS**: Uses system fonts like Arial.ttf and Helvetica.ttc
- **Cross-platform**: Falls back to default fonts if system fonts unavailable  
- **Hidden Window**: Renders off-screen using SDL video driver settings
- **Environment**: Suppresses pygame support prompts and pkg_resources warnings
- Always use pip3 instead of pip

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