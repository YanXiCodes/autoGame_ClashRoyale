from pprint import pprint
from time import sleep
from threading import Thread
from .control.control import Control
from .touch.touchScreen import TouchScreen, display
from pyscrcpy import Client
from functools import partial


class Main:
    def __init__(self, devices_name, max_fps: int = 30) -> None:
        self.client = Client(devices_name, max_fps=max_fps)
        self.touch_screen = TouchScreen(self.client)
        self.thread = Thread(target=self.identify, daemon=True)
        self.control = Control()
        self.frame = None

    # 点击操作
    def identify(self):
        while True:
            if self.frame is not None:
                views= self.control.recognize_current_view(
                    self.frame
                )
                pprint(f"当前界面：{views}")
                if views:
                    for view in views:
                        self.touch_screen.tap(view.x, view.y) # type: ignore
                        sleep(5)
                sleep(0.1)

    def run(self):
        @self.touch_screen.client.on_frame
        def _(client, frame):
            self.frame = frame
            display(frame)

        self.thread.start()
        self.touch_screen.client.start()
