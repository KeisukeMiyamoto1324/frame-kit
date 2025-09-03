from typing import List
from video_base import VideoBase


class Scene:
    """シーンクラス - 複数の要素をまとめて管理"""
    def __init__(self):
        self.elements: List[VideoBase] = []
        self.start_time = 0.0
        self.duration = 0.0
    
    def add(self, element: VideoBase):
        """要素をシーンに追加"""
        from .audio_element import AudioElement
        
        self.elements.append(element)
        
        # BGMモードでないオーディオ要素と他の要素のみがシーン時間に影響
        if not (isinstance(element, AudioElement) and getattr(element, 'loop_until_scene_end', False)):
            element_end_time = element.start_time + element.duration
            self.duration = max(self.duration, element_end_time)
        
        # BGMモードのオーディオ要素の持続時間を更新（シーン時間決定後）
        self._update_bgm_durations()
        return self
    
    def _update_bgm_durations(self):
        """BGMモードのオーディオ要素の持続時間をシーンの長さに合わせて更新"""
        from .audio_element import AudioElement
        for element in self.elements:
            if isinstance(element, AudioElement) and element.loop_until_scene_end:
                element.update_duration_for_scene(self.duration)
    
    def start_at(self, time: float):
        """シーンの開始時間を設定"""
        self.start_time = time
        return self
    
    def render(self, time: float):
        """シーン内の全要素をレンダリング"""
        scene_time = time - self.start_time
        if scene_time < 0 or scene_time > self.duration:
            return
        
        for element in self.elements:
            element.render(scene_time)