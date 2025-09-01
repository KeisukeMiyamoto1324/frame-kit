# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based video editor that programmatically generates videos using OpenGL rendering and text elements. The project creates video content by composing scenes with various elements like text overlays and renders them to MP4 files.

## Development Setup

The project uses a Python virtual environment:
- **Virtual Environment**: `venv/` directory contains the Python virtual environment  
- **Python Version**: Python 3.12
- **Main Entry Points**: `main.py` or `sample.py` both demonstrate video creation

### Running the Application

```bash
# Activate the virtual environment (macOS/Linux)
source venv/bin/activate

# Run the main video editor (either works)
python main.py
# or
python sample.py
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

1. **VideoBase** (`video_element.py`): Base class for all video elements
   - Handles positioning, timing, and visibility logic
   - Provides fluent interface methods (position, set_duration, start_at)
   - All elements inherit from this class

2. **Text** (`text_element.py`): Text rendering component
   - Creates OpenGL textures from text using PIL/Pillow
   - Supports custom fonts, colors, and sizes
   - Handles macOS system font fallback (Arial.ttf → Helvetica.ttc → default)
   - Lazy texture creation (only when OpenGL context is available)

3. **Scene** (`scene.py`): Container for multiple video elements
   - Groups elements and manages their collective timing
   - Handles scene-relative time calculations
   - Can be positioned at specific times in the timeline

4. **MasterScene** (`master_scene.py`): Main video composition manager
   - Handles overall video settings (width, height, fps, output filename)
   - Manages pygame/OpenGL context and rendering pipeline
   - Exports final video using OpenCV with progress tracking
   - Hidden window rendering using SDL video driver settings

### Project Structure

```
video-editer/
├── main.py              # Main application entry point
├── sample.py            # Alternative demo script
├── video_element.py     # Base class for all video elements
├── text_element.py      # Text rendering implementation
├── scene.py             # Scene container class
├── master_scene.py      # Main video composition manager
├── output/              # Generated video files
└── venv/                # Python virtual environment
```

### Output Structure

- Videos are saved to the `output/` directory (auto-created)
- Default output format is MP4 with mp4v codec
- Standard example creates `output/text_demo.mp4`

## Development Patterns

### Creating Video Elements

Elements use a fluent interface pattern:
```python
text = (
    Text("Hello", size=100, color=(255, 0, 0))
        .position(960, 540)
        .set_duration(3)
        .start_at(1)
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
from text_element import Text

# Create master scene
master_scene = MasterScene(width=1920, height=1080, fps=60)
master_scene.set_output("my_video.mp4")

# Create and populate scene
scene = Scene()
text = Text("Hello World", size=100, color=(255, 0, 0)).position(960, 540)
scene.add(text)

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
- Always use pip3 instead pip