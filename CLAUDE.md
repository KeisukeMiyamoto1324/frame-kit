# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based video editor that programmatically generates videos using OpenGL rendering and text elements. The project creates video content by composing scenes with various elements like text overlays and renders them to MP4 files.

## Development Setup

The project uses a Python virtual environment:
- **Virtual Environment**: `venv/` directory contains the Python virtual environment
- **Python Version**: Python 3.12 (based on venv structure)
- **Main Script**: `sample.py` contains the complete video editor implementation

### Running the Application

```bash
# Activate the virtual environment (macOS/Linux)
source venv/bin/activate

# Run the main video editor
python sample.py
```

## Core Architecture

The video editor is built around several key classes in `sample.py`:

### Core Components

1. **VideoElement** (`sample.py:12-43`): Base class for all video elements
   - Handles positioning, timing, and visibility
   - All elements inherit from this class

2. **Text** (`sample.py:46-180`): Text rendering component
   - Creates OpenGL textures from text using PIL/Pillow
   - Supports custom fonts, colors, and sizes
   - Handles font fallback for different systems

3. **Scene** (`sample.py:183-210`): Container for multiple video elements
   - Manages timing and rendering of grouped elements
   - Can be positioned at specific times in the timeline

4. **MasterScene** (`sample.py:213-330`): Main video composition manager
   - Handles overall video settings (width, height, fps)
   - Manages OpenGL context and rendering pipeline
   - Exports final video using OpenCV

### Key Dependencies

The project relies on several Python libraries:
- **pygame**: Window management and OpenGL context
- **OpenGL.GL/GLU**: Low-level graphics rendering
- **numpy**: Array operations for image data
- **cv2 (OpenCV)**: Video encoding and file output
- **PIL (Pillow)**: Text rendering and image manipulation

### Output Structure

- Videos are saved to the `output/` directory
- Default output format is MP4 with mp4v codec
- The example creates `output/text_demo.mp4`

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

### Coordinate System

- Uses pixel coordinates with origin at top-left (0, 0)
- Standard video dimensions: 1920x1080
- Text positioning is based on top-left corner of text bounds

## Platform Considerations

- **macOS**: Uses system fonts like Arial.ttf and Helvetica.ttc
- **Cross-platform**: Falls back to default fonts if system fonts unavailable
- **Hidden Window**: Renders off-screen using SDL video driver settings