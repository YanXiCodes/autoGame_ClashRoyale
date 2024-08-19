import cv2 as cv
from pyscrcpy import Client  # import scrcpy client
from pyscrcpy import control
import time
import random
from typing import Union
import pathlib
from pyscrcpy import Client

__base_path__ = pathlib.Path.cwd()

def display(frame: cv.typing.MatLike):
    cv.imshow("Video", frame)
    cv.waitKey(1)


class TouchScreen:    
    def __init__(self, client: Client) -> None:
        # 创建scrcpy客户端
        self.client = client
        self._save_next_frame: bool = False  # 标志位，指示是否保存下一帧

    # 按下操作
    def touch_start(self, x: Union[int, float], y: Union[int, float]):
        self.client.control.touch(x=int(x), y=int(y))

    # 移动操作
    def touch_move(self, x: Union[int, float], y: Union[int, float]):
        self.client.control.touch(x=int(x), y=int(y))

    # 松开操作
    def touch_end(self, x: Union[int, float], y: Union[int, float]):
        self.client.control.touch(x=int(x), y=int(y))

    # 点击操作(在指定位置按下并松开)
    def tap(self, x: Union[int, float], y: Union[int, float]):
        self.touch_start(x, y)
        time.sleep(0.01)
        self.touch_end(x, y)

    # 截图操作(直接从on_frame中获取)
    def take_screenshot(self):
        # 设置标志位，在下一帧回调时保存帧
        self._save_next_frame = True

    # 滑动操作
    def swipe(
        self,
        x1: Union[int, float],
        y1: Union[int, float],
        x2: Union[int, float],
        y2: Union[int, float],
        duration: Union[int, float],
    ):
        pass
