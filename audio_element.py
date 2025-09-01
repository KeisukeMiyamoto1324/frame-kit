import os
import numpy as np
from typing import Optional
from video_base import VideoBase

# オーディオライブラリのインポートを試行
try:
    import mutagen
    from mutagen import File as MutagenFile
    HAS_MUTAGEN = True
except ImportError:
    HAS_MUTAGEN = False

try:
    import librosa
    HAS_LIBROSA = True
except ImportError:
    HAS_LIBROSA = False


class AudioElement(VideoBase):
    """Audio element for playing audio files"""
    def __init__(self, audio_path: str, volume: float = 1.0):
        super().__init__()
        self.audio_path = audio_path
        self.volume = volume
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
            # mutagenを使ってオーディオ情報を取得
            if HAS_MUTAGEN:
                audio_file = MutagenFile(self.audio_path)
                if audio_file is not None and hasattr(audio_file, 'info'):
                    self.duration = float(audio_file.info.length)
                    print(f"Audio loaded (mutagen): {self.audio_path}, duration: {self.duration:.2f}s")
                    return
            
            # librosaを使ってオーディオ情報を取得
            if HAS_LIBROSA:
                try:
                    y, sr = librosa.load(self.audio_path, sr=None)
                    self.duration = len(y) / sr
                    self.sample_rate = sr
                    print(f"Audio loaded (librosa): {self.audio_path}, duration: {self.duration:.2f}s, sr: {sr}")
                    return
                except Exception as librosa_error:
                    print(f"Librosa failed: {librosa_error}")
            
            # フォールバック: ファイル名からの推定またはデフォルト値
            print(f"Warning: Could not determine audio duration for {self.audio_path}")
            print("Install 'mutagen' or 'librosa' for proper audio file support:")
            print("  pip3 install mutagen")
            print("  pip3 install librosa")
            self.duration = 10.0  # デフォルト値
            
        except Exception as e:
            print(f"Error loading audio info {self.audio_path}: {e}")
            self.duration = 10.0  # デフォルト値
    
    def set_volume(self, volume: float):
        """Set audio volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        return self
    
    def _get_audio_at_time(self, audio_time: float):
        """Get audio data at specific time"""
        # オーディオの場合、実際の音声データの処理は
        # 外部のオーディオライブラリ（pygame, pyaudio等）に依存するため
        # ここではプレースホルダーとして実装
        return None
    
    def render(self, time: float):
        """Render audio (no visual output for audio elements)"""
        if not self.is_visible_at(time):
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
        # オーディオ要素用のクリーンアップ
        pass