import os
import cv2
import numpy as np
from typing import Optional
from video_base import VideoBase


class AudioElement(VideoBase):
    """Audio element for playing audio files"""
    def __init__(self, audio_path: str, volume: float = 1.0):
        super().__init__()
        self.audio_path = audio_path
        self.volume = volume
        self.audio_capture = None
        self.sample_rate = 44100
        self.total_samples = 0
        self.channels = 2
        self.current_audio_data = None
        self._load_audio_info()
        # 初期化時にサイズを計算（オーディオは視覚的要素がないため0）
        self.calculate_size()
    
    def _load_audio_info(self):
        """Load audio file information"""
        if not os.path.exists(self.audio_path):
            print(f"Warning: Audio file not found: {self.audio_path}")
            return
        
        try:
            # OpenCVを使ってオーディオ情報を取得
            self.audio_capture = cv2.VideoCapture(self.audio_path)
            
            if not self.audio_capture.isOpened():
                print(f"Error: Cannot open audio file: {self.audio_path}")
                return
            
            # オーディオプロパティを取得
            fps = self.audio_capture.get(cv2.CAP_PROP_FPS)
            total_frames = int(self.audio_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # オーディオの長さを計算
            if fps > 0 and total_frames > 0:
                audio_duration = total_frames / fps
                self.duration = audio_duration
            
            print(f"Audio loaded: {self.audio_path}, duration: {self.duration:.2f}s")
            
        except Exception as e:
            print(f"Error loading audio info {self.audio_path}: {e}")
    
    def set_volume(self, volume: float):
        """Set audio volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        return self
    
    def _get_audio_at_time(self, audio_time: float):
        """Get audio data at specific time"""
        if self.audio_capture is None or not self.audio_capture.isOpened():
            return None
        
        # オーディオの場合、実際の音声データの処理は
        # 外部のオーディオライブラリ（pygame, pyaudio等）に依存するため
        # ここではプレースホルダーとして実装
        return None
    
    def render(self, time: float):
        """Render audio (no visual output for audio elements)"""
        if not self.is_visible_at(time):
            return
        
        if self.audio_capture is None:
            return
        
        # Calculate audio time (time within the audio clip)
        audio_time = time - self.start_time
        
        # オーディオの場合、視覚的なレンダリングは不要
        # 実際のオーディオ再生は外部システムで処理される
        pass
    
    def get_audio_data_at_time(self, time: float):
        """Get audio data for external audio system"""
        if not self.is_visible_at(time):
            return None
        
        if self.audio_capture is None:
            return None
        
        # Calculate audio time (time within the audio clip)
        audio_time = time - self.start_time
        
        # Return audio metadata for external processing
        return {
            'audio_path': self.audio_path,
            'audio_time': audio_time,
            'volume': self.volume,
            'start_time': self.start_time,
            'duration': self.duration
        }
    
    def calculate_size(self):
        """オーディオのボックスサイズを事前計算（視覚的要素なし）"""
        # オーディオ要素は視覚的な表示がないため、サイズは0
        self.width = 0
        self.height = 0
    
    def __del__(self):
        """Destructor to clean up resources"""
        if self.audio_capture:
            self.audio_capture.release()