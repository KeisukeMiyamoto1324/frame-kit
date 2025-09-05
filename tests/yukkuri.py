# PYTHONPATH=$(pwd) python3 -m tests.yukkuri

from typing import Optional
from framekit.master_scene_element import MasterScene
from framekit.scene_element import Scene
from framekit.text_element import TextElement
from framekit.audio_element import AudioElement
from framekit.image_element import ImageElement
from framekit.video_element import VideoElement
from framekit.animation import AnimationPresets

VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
VIDEO_FPS = 60

master = MasterScene(width=VIDEO_WIDTH, height=VIDEO_HEIGHT, fps=VIDEO_FPS, quality="low")
master.set_output("yukkuri.mp4")

scene = Scene()

title = (
    TextElement("This is a title of this video.", size=20)
        .position(VIDEO_WIDTH//3, VIDEO_HEIGHT//3, "center")
        .set_duration(30)
        # .set_background(color=[0, 0, 0], padding=20)
        .set_corner_radius(10)
        .animate_until_scene_end('scale', AnimationPresets.pulse(from_scale=1.0, to_scale=1.2, duration=2.0), 
                                repeat_delay=0, repeat_mode='restart')
)

bg = (
    ImageElement("sample_asset/bg.jpg")
        .set_crop(400, 400, mode="fill")
        .position(VIDEO_WIDTH//3, VIDEO_HEIGHT//3, "center")
        .set_loop_until_scene_end()
        .start_at(0)
)

scene.add(bg)
scene.add(title)

master.add(scene)
master.render()
