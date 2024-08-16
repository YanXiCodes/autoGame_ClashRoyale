import subprocess
import cv2 as cv
from pyscrcpy import Client  # import scrcpy client
import time
import random
from typing import Union

# 获取当前路径


# 启动脚本时 scrcpy自动连接至默认设备
class AdbClient:
    # 初始化
    # 默认为第一个设备

    def __init__(self, devices_name: str, max_fps: int = 30) -> Client:
        self.devices_name = devices_name
        if self.devices_name is None:
            self.devices_name = self.get_default_device()
        # 创建scrcpy客户端
        self.client = Client(self.devices_name, max_fps=max_fps)
        self._save_next_frame: bool = False  # 标志位，指示是否保存下一帧

    # 获取第一个设备
    def get_default_device(self) -> str:
        result = subprocess.run(
            ["adb", "devices"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        lines = result.stdout.splitlines()
        devices = [
            line.split()[0]
            for line in lines
            if "device" in line and "devices" not in line
        ]
        if not devices:
            raise RuntimeError("No ADB devices found")
        return devices[0]
