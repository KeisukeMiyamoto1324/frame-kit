from typing import List
from video_element import VideoElement


class Scene:
    """シーンクラス - 複数の要素をまとめて管理"""
    def __init__(self):
        self.elements: List[VideoElement] = []
        self.start_time = 0.0
        self.duration = 0.0
    
    def add(self, element: VideoElement):
        """要素をシーンに追加"""
        self.elements.append(element)
        # シーンの継続時間を更新
        element_end_time = element.start_time + element.duration
        self.duration = max(self.duration, element_end_time)
        return self
    
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