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


class MasterScene:
    """マスターシーンクラス - 全体の動画を管理"""
    def __init__(self, width: int = 1920, height: int = 1080, fps: int = 60):
        self.width = width
        self.height = height
        self.fps = fps
        self.scenes: List[Scene] = []
        self.total_duration = 0.0
        self.output_filename = "output_video.mp4"
    
    def add(self, scene: Scene):
        """シーンを追加"""
        self.scenes.append(scene)
        # 全体の継続時間を更新
        scene_end_time = scene.start_time + scene.duration
        self.total_duration = max(self.total_duration, scene_end_time)
        return self
    
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
        
        full_path = os.path.join(output_dir, self.output_filename)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        video_writer = cv2.VideoWriter(full_path, fourcc, self.fps, (self.width, self.height))
        
        if not video_writer.isOpened():
            raise Exception(f"動画ファイル {full_path} を作成できませんでした")
        
        print(f"動画ファイル {full_path} の作成を開始しました")
        return video_writer
    
    def _capture_frame(self):
        """現在の画面をキャプチャ"""
        pixels = glReadPixels(0, 0, self.width, self.height, GL_RGB, GL_UNSIGNED_BYTE)
        image = np.frombuffer(pixels, dtype=np.uint8)
        image = image.reshape((self.height, self.width, 3))
        image = np.flipud(image)  # OpenGLは左下が原点なので上下反転
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        return image
    
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
        video_writer = self._setup_video_writer()
        
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
            
            print(f"動画保存完了: output/{self.output_filename}")
            
        finally:
            # クリーンアップ
            video_writer.release()
            pygame.quit()