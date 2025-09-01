import os
import warnings

# Pygame関連の環境変数を事前に設定
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# pkg_resources警告を抑制
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*pkg_resources.*")

from master_scene import MasterScene
from scene import Scene
from text_element import Text


def main():
    """メイン関数 - 動画作成のデモ"""
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


if __name__ == "__main__":
    main()