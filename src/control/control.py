# 调度模块 用于调用识别模块和操作模块
# 通过调用识别模块识别出的结果，调用操作模块执行相应的操作
from typing import List, Optional, Tuple
import cv2 as cv
import os
import sys
import pathlib
from pydantic import BaseModel
from sympy import N
import yaml

from src.schema import View, ViewsConfig
from src.config.path import current_path


class Control:
    def __init__(self):
        self.image_folder = current_path / "resources" / "img" / "element"
        self.image_list = [
            f for f in self.image_folder.iterdir() if f.glob(r"*.(jpg|png)")
        ]

    def run(self):
        pass

    def get_current_page(self):
        pass

    # 识别当前页面场景
    def recognize_current_view(
        self, frame
    ) -> List[View]:
        # 读取所有模板图片
        views = []
        cv.imwrite(r"D:\ClashRoyale\resources\img\screenshot\frame.png", frame)
        view_mapping = ViewsConfig.read_config()
        # 读取模板图片并进行匹配
        for image in self.image_list:
            template = cv.imread(str(image))
            
            res = cv.matchTemplate(frame, template, cv.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv.minMaxLoc(res)
            if max_val > 0.85:
                print(image.name)
                if view := view_mapping.get(image.name):
                    if view.x is None:
                        view.x = max_loc[0]
                    if view.y is None:
                        view.y = max_loc[1]
                    views.append(view)
        return views


if __name__ == "__main__":
    frame = cv.imread(r"D:\ClashRoyale\resources\img\screenshot\frame.png")
    con = Control()
    print(frame.shape)
    print(con.recognize_current_view(frame))
