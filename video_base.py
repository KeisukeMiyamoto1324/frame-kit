from typing import List, Optional, Tuple


class VideoBase:
    """動画要素の基底クラス"""
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.start_time = 0.0
        self.duration = 1.0
        self.visible = True
    
    def position(self, x: float, y: float):
        """位置を設定"""
        self.x = x
        self.y = y
        return self
    
    def set_duration(self, duration: float):
        """表示時間を設定"""
        self.duration = duration
        return self
    
    def start_at(self, time: float):
        """開始時間を設定"""
        self.start_time = time
        return self
    
    def is_visible_at(self, time: float) -> bool:
        """指定時間に表示されるかチェック"""
        return self.start_time <= time < (self.start_time + self.duration)
    
    def render(self, time: float):
        """要素をレンダリング（サブクラスで実装）"""
        pass