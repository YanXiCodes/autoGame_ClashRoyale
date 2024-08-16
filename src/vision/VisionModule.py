import cv2 as cv
from abc import ABC, abstractmethod

# 分为两部分 一部分是图像识别 一部分是图像操作
# 1，接收图像帧 识别上需要提取文字的位置
# 2，接收图像帧 识别上需要点击的位置
class VisionModule(ABC):
    @abstractmethod
    def extract_text_positions(self, frame):
        pass

    @abstractmethod
    def extract_click_positions(self, frame):
        pass



class ImageRecognition(VisionModule):
    def extract_text_positions(self, frame):

        text_positions = [] 
        return text_positions

    def extract_click_positions(self, frame):
     
        click_positions = [] 
        return click_positions



class ImageOperation(VisionModule):
    def extract_text_positions(self, frame):
        
        text_positions = []  
        return text_positions

    def extract_click_positions(self, frame):
     
        click_positions = []  
        return click_positions