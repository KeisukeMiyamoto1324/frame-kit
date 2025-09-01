import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import cv2
import math
import os
from typing import List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont


class VideoElement:
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


class Text(VideoElement):
    """テキスト要素"""
    def __init__(self, text: str, size: int = 50, color: Tuple[int, int, int] = (255, 255, 255), font_path: str = None):
        super().__init__()
        self.text = text
        self.size = size
        self.color = color
        self.font_path = font_path
        self.texture_id = None
        self.texture_width = 0
        self.texture_height = 0
        self._create_text_texture()
    
    def _create_text_texture(self):
        """テキストのテクスチャを作成"""
        # テクスチャ作成は後でrender時に行う（OpenGLコンテキストが必要なため）
        self.texture_created = False
    
    def _create_texture_now(self):
        """OpenGLコンテキスト内でテクスチャを作成"""
        try:
            # フォントを読み込み
            if self.font_path and os.path.exists(self.font_path):
                font = ImageFont.truetype(self.font_path, self.size)
            else:
                try:
                    font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", self.size)
                except:
                    try:
                        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", self.size)
                    except:
                        font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # テキストのサイズを測定（より正確な方法）
        dummy_img = Image.new('RGBA', (1, 1))
        dummy_draw = ImageDraw.Draw(dummy_img)
        
        # テキストのバウンディングボックスを取得
        bbox = dummy_draw.textbbox((0, 0), self.text, font=font)
        text_width = max(bbox[2] - bbox[0], 1)
        text_height = max(bbox[3] - bbox[1], 1)
        
        # フォントのアセント/ディセントを考慮してパディングを追加
        ascent, descent = font.getmetrics()
        total_height = ascent + descent
        y_offset = -bbox[1]  # テキストの上端を0に合わせる
        
        # より大きめのキャンバスを作成（パディング込み）
        canvas_width = text_width + 10  # 左右に5pxずつパディング
        canvas_height = max(total_height, text_height) + 10  # 上下に5pxずつパディング
        
        # テクスチャ用の画像を作成
        img = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # テキストを中央に描画（パディングを考慮）
        draw.text((5, 5 + y_offset), self.text, font=font, fill=(*self.color, 255))
        
        # 実際のテクスチャサイズを更新
        text_width = canvas_width
        text_height = canvas_height
        
        # 画像をNumPy配列に変換
        img_data = np.array(img)
        
        # OpenGLテクスチャを生成
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        
        # テクスチャパラメータを設定
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        
        # テクスチャデータをアップロード
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_width, text_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        
        self.texture_width = text_width
        self.texture_height = text_height
        
        glBindTexture(GL_TEXTURE_2D, 0)
        self.texture_created = True

    def render(self, time: float):
        """テキストをレンダリング"""
        if not self.is_visible_at(time):
            return
        
        # テクスチャがまだ作成されていない場合は作成
        if not self.texture_created:
            self._create_texture_now()
        
        if self.texture_id is None:
            return
        
        # テクスチャを有効にする
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        
        # アルファブレンディングを有効にする
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # 白色でテクスチャを描画（テクスチャの色がそのまま使用される）
        glColor4f(1.0, 1.0, 1.0, 1.0)
        
        # テクスチャ付きの四角形を描画
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(self.x, self.y)
        
        glTexCoord2f(1.0, 0.0)
        glVertex2f(self.x + self.texture_width, self.y)
        
        glTexCoord2f(1.0, 1.0)
        glVertex2f(self.x + self.texture_width, self.y + self.texture_height)
        
        glTexCoord2f(0.0, 1.0)
        glVertex2f(self.x, self.y + self.texture_height)
        glEnd()
        
        # テクスチャを無効にする
        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)
    
    def __del__(self):
        """デストラクタでテクスチャを削除"""
        if self.texture_id:
            try:
                glDeleteTextures(1, [self.texture_id])
            except:
                pass


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
                
                # 進捗表示
                if frame_num % (self.fps * 1) == 0:  # 1秒ごと
                    progress = (frame_num / total_frames) * 100
                    print(f"進捗: {frame_num}/{total_frames} フレーム ({progress:.1f}%)")
            
            print(f"動画保存完了: output/{self.output_filename}")
            
        finally:
            # クリーンアップ
            video_writer.release()
            pygame.quit()


# 使用例
if __name__ == "__main__":
    # マスターシーンを作成
    master_scene = MasterScene(width=1920, height=1080, fps=60)
    master_scene.set_output("text_demo.mp4")
    
    # シーンを作成
    scene = Scene()
    
    # テキスト要素を作成（位置は画面の中央付近）
    text1 = (
        Text("Hello", size=100, color=(255, 0, 0))
            .position(960, 540)
            .set_duration(3)
    )
    text2 = (
        Text("World", size=80, color=(0, 255, 0))
            .position(960, 640)
            .set_duration(5)
            .start_at(1)
    )
    
    # シーンに追加
    scene.add(text1)
    scene.add(text2)
    
    # マスターシーンに追加
    master_scene.add(scene)
    
    # レンダリング実行
    master_scene.render()