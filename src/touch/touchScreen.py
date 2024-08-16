import cv2 as cv
from pyscrcpy import Client  # import scrcpy client
import time
import random
from typing import Union
import pathlib
import touch


__base_path__ = pathlib.Path.cwd()


class touchScreen:
    def __init__(self, devices_name, max_fps: int = 30) -> None:
        touch.AdbClient.__init__(self, devices_name, max_fps)

    def on_frame(self, client: Client, frame: cv.typing.MatLike):
        save_path = (
            __base_path__ / "resources" / "img" / "screenshot" / "screenshot.png"
        )
        if frame is not None:
            if self._save_next_frame:
                success = cv.imwrite(str(save_path), frame)
                print("截图成功" if success else "截图失败")
                self._save_next_frame = False
            cv.imshow("Video", frame)
            cv.waitKey(1)

    # 按下操作
    def touch_start(self, x: Union[int, float], y: Union[int, float]):
        self.client.control.touch(int(x), int(y))

    # 移动操作
    def touch_move(self, x: Union[int, float], y: Union[int, float]):
        self.client.control.touch(int(x), int(y))

    # 松开操作
    def touch_end(self, x: Union[int, float], y: Union[int, float]):
        self.client.control.touch(int(x), int(y))

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
