import os
import cv2
import numpy as np
from typing import List
from tqdm import tqdm
from OpenGL.GL import *
from OpenGL.GLU import *
from scene import Scene

# Pygameの警告を抑制
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

# オーディオ処理用ライブラリの試行インポート
try:
    import subprocess
    HAS_FFMPEG = True
except ImportError:
    HAS_FFMPEG = False


class MasterScene:
    """マスターシーンクラス - 全体の動画を管理"""
    def __init__(self, width: int = 1920, height: int = 1080, fps: int = 60):
        self.width = width
        self.height = height
        self.fps = fps
        self.scenes: List[Scene] = []
        self.total_duration = 0.0
        self.output_filename = "output_video.mp4"
        self.audio_elements = []  # オーディオ要素を追跡
    
    def add(self, scene: Scene):
        """シーンを追加"""
        self.scenes.append(scene)
        # 全体の継続時間を更新
        scene_end_time = scene.start_time + scene.duration
        self.total_duration = max(self.total_duration, scene_end_time)
        
        # オーディオ要素を収集
        self._collect_audio_elements(scene)
        return self
    
    def _collect_audio_elements(self, scene: Scene):
        """シーンからオーディオ要素を収集"""
        from audio_element import AudioElement
        for element in scene.elements:
            if isinstance(element, AudioElement):
                self.audio_elements.append(element)
                print(f"Audio element found: {element.audio_path}")
    
    def set_output(self, filename: str):
        """出力ファイル名を設定"""
        self.output_filename = filename
        return self
    
    def _init_opengl(self):
        """OpenGLの初期設定"""
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        # 座標系を設定（左上が原点、ピクセル座標系）
        glOrtho(0, self.width, self.height, 0, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # ブレンディングを有効にしてアルファ値を使用可能に
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    def _setup_video_writer(self):
        """動画書き込み設定"""
        # 出力ディレクトリを作成
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # オーディオ要素がある場合は一時ファイル、ない場合は指定ファイル名
        if self.audio_elements:
            # 一時ファイル名を作成
            base_name = os.path.splitext(self.output_filename)[0]
            temp_filename = f"{base_name}_temp_video_only.mp4"
            full_path = os.path.join(output_dir, temp_filename)
        else:
            full_path = os.path.join(output_dir, self.output_filename)
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        video_writer = cv2.VideoWriter(full_path, fourcc, self.fps, (self.width, self.height))
        
        if not video_writer.isOpened():
            raise Exception(f"動画ファイル {full_path} を作成できませんでした")
        
        print(f"動画ファイル {full_path} の作成を開始しました")
        return video_writer, full_path
    
    def _capture_frame(self):
        """現在の画面をキャプチャ"""
        pixels = glReadPixels(0, 0, self.width, self.height, GL_RGB, GL_UNSIGNED_BYTE)
        image = np.frombuffer(pixels, dtype=np.uint8)
        image = image.reshape((self.height, self.width, 3))
        image = np.flipud(image)  # OpenGLは左下が原点なので上下反転
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        return image
    
    def _create_audio_mix(self, video_path: str):
        """FFmpegを使ってビデオにオーディオを追加"""
        if not self.audio_elements:
            print("No audio elements found, skipping audio mixing")
            return video_path
        
        if not HAS_FFMPEG:
            print("Warning: subprocess not available, cannot mix audio")
            return video_path
        
        # FFmpegが利用可能かチェック
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Warning: FFmpeg not found, cannot mix audio")
            print("Install FFmpeg to enable audio mixing:")
            print("  macOS: brew install ffmpeg")
            print("  Ubuntu: sudo apt install ffmpeg")
            return video_path
        
        output_dir = "output"
        final_output = os.path.join(output_dir, self.output_filename)
        
        # 複数のオーディオファイルを処理するためのコマンド構築
        cmd = ['ffmpeg', '-y', '-i', video_path]
        
        # 存在するオーディオファイルのみを追加
        valid_audio_files = []
        for audio_element in self.audio_elements:
            if os.path.exists(audio_element.audio_path):
                cmd.extend(['-i', audio_element.audio_path])
                valid_audio_files.append(audio_element)
                print(f"Adding audio: {audio_element.audio_path}")
            else:
                print(f"Warning: Audio file not found, skipping: {audio_element.audio_path}")
        
        if not valid_audio_files:
            print("No valid audio files found, keeping video-only output")
            return video_path
        
        # 複雑なオーディオミキシングを避けて、最初のオーディオファイルのみ使用
        if len(valid_audio_files) == 1:
            cmd.extend(['-c:v', 'copy', '-c:a', 'aac', '-shortest', final_output])
        else:
            # 複数ファイルの場合は警告を出して最初のファイルのみ使用
            print(f"Warning: Multiple audio files found. Using only the first one: {valid_audio_files[0].audio_path}")
            cmd = ['ffmpeg', '-y', '-i', video_path, '-i', valid_audio_files[0].audio_path, 
                   '-c:v', 'copy', '-c:a', 'aac', '-shortest', final_output]
        
        try:
            print("Mixing audio with video using FFmpeg...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Audio mixing completed: {final_output}")
                # 一時ファイルを削除
                if os.path.exists(video_path) and "temp_video_only" in video_path:
                    os.remove(video_path)
                    print(f"Temporary video file deleted: {video_path}")
                return final_output
            else:
                print(f"FFmpeg error: {result.stderr}")
                print("Keeping video-only output")
                return video_path
        except Exception as e:
            print(f"Error during audio mixing: {e}")
            print("Keeping video-only output")
            return video_path
    
    def render(self):
        """動画をレンダリング"""
        # 環境設定（ウィンドウを非表示）
        os.environ['SDL_VIDEODRIVER'] = 'cocoa'
        os.environ['SDL_VIDEO_WINDOW_POS'] = '-1000,-1000'
        
        # Pygameを初期化
        pygame.init()
        
        # OpenGLウィンドウを作成
        screen = pygame.display.set_mode(
            (self.width, self.height), 
            pygame.DOUBLEBUF | pygame.OPENGL | pygame.HIDDEN
        )
        
        # OpenGLを初期化
        self._init_opengl()
        
        # 動画書き込み設定
        video_writer, video_path = self._setup_video_writer()
        
        try:
            total_frames = int(self.total_duration * self.fps)
            print(f"動画生成開始... (総フレーム数: {total_frames})")
            
            # tqdmでプログレスバーを表示
            with tqdm(total=total_frames, desc="Rendering", unit="frames") as pbar:
                for frame_num in range(total_frames):
                    current_time = frame_num / self.fps
                    
                    # 画面をクリア
                    glClear(GL_COLOR_BUFFER_BIT)
                    
                    # 全シーンをレンダリング
                    for scene in self.scenes:
                        scene.render(current_time)
                    
                    # 描画を確定
                    pygame.display.flip()
                    
                    # フレームをキャプチャして動画に書き込み
                    frame = self._capture_frame()
                    video_writer.write(frame)
                    
                    # プログレスバーを更新
                    pbar.update(1)
            
            if self.audio_elements:
                print(f"ビデオ部分の保存完了: {video_path}")
            else:
                print(f"動画ファイルの保存完了: {video_path}")
            
        finally:
            # クリーンアップ
            video_writer.release()
            pygame.quit()
            
            # オーディオミキシング（ビデオ作成後）
            if self.audio_elements:
                final_output = self._create_audio_mix(video_path)
                print(f"最終動画ファイル: {final_output}")
            else:
                print(f"最終動画ファイル: {video_path}")