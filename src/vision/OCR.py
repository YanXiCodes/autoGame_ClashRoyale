import cv2 as cv
from cv2 import Mat
import numpy as np
from pprint import pprint
import pytesseract


class OCR:
    def __init__(self, lang="chi_sim", config=r"--oem 3 --psm 6"):
        self.lang = lang
        self.config = config

    def preprocess_image(self, image: Mat) -> Mat:
        """
        预处理图像：转换为灰度图像并进行二值化处理。
        """
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        _, binary = cv.threshold(gray, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
        return binary

    def predict(self, image: Mat) -> list:
        """
        使用 Tesseract OCR 识别图像中的文字，并返回文字及其位置信息。
        """
        data = pytesseract.image_to_data(
            image,
            lang=self.lang,
            output_type=pytesseract.Output.DICT,
            config=self.config,
        )
        text_positions = []
        for i in range(len(data["text"])):
            if int(data["conf"][i]) > 0:  # 过滤掉置信度小于0的结果
                text_info = {
                    "text": data["text"][i],
                    "left": data["left"][i],
                    "top": data["top"][i],
                    "width": data["width"][i],
                    "height": data["height"][i],
                }
                text_positions.append(text_info)
        return self.merge_text_positions(text_positions)

    def draw_bbox(self, image: Mat, text_positions: list) -> Mat:
        """
        在图像上绘制文字的边界框。
        """
        for text_info in text_positions:
            left = text_info["left"]
            top = text_info["top"]
            width = text_info["width"]
            height = text_info["height"]
            cv.rectangle(
                image, (left, top), (left + width, top + height), (0, 0, 255), 2
            )
        return image

    def merge_text_positions(self, text_positions: list) -> list:
        """
        合并相邻的单个字成词组。
        """
        if not text_positions:
            return []

        merged_positions = []
        current_text = text_positions[0]["text"]
        current_left = text_positions[0]["left"]
        current_top = text_positions[0]["top"]
        current_right = current_left + text_positions[0]["width"]
        current_bottom = current_top + text_positions[0]["height"]

        for i in range(1, len(text_positions)):
            text_info = text_positions[i]
            if text_info["left"] <= current_right + 10:  # 判断是否相邻
                current_text += text_info["text"]
                current_right = text_info["left"] + text_info["width"]
                current_bottom = max(
                    current_bottom, text_info["top"] + text_info["height"]
                )
            else:
                merged_positions.append(
                    {
                        "text": current_text,
                        "left": current_left,
                        "top": current_top,
                        "width": current_right - current_left,
                        "height": current_bottom - current_top,
                    }
                )
                current_text = text_info["text"]
                current_left = text_info["left"]
                current_top = text_info["top"]
                current_right = text_info["left"] + text_info["width"]
                current_bottom = text_info["top"] + text_info["height"]

        merged_positions.append(
            {
                "text": current_text,
                "left": current_left,
                "top": current_top,
                "width": current_right - current_left,
                "height": current_bottom - current_top,
            }
        )

        return merged_positions

    def click_position(self, image: Mat, text: str) -> tuple:
        """
        返回需要点击的文字的坐标（边界框的中心点）。
        """
        text_positions = self.predict(image)
        print(text_positions)
        for text_info in text_positions:
            if text_info["text"] == text:
                left = text_info["left"]
                top = text_info["top"]
                width = text_info["width"]
                height = text_info["height"]
                return (left + width // 2, top + height // 2)
            elif text_info["text"].startswith(text[:int(len(text) * 0.5)]):
                left = text_info["left"]
                top = text_info["top"]
                width = text_info["width"]
                height = text_info["height"]
                return (left + width // 2, top + height // 2)
        return None


# if __name__ == "__main__":
#     image = cv.imread(r"D:\\ClashRoyale\\docs\\images\\flow\\1723708311817.png")
#     ocr = OCR()
#     click_text = "暂不更改"
#     click_position = ocr.click_position(image, click_text)
#     if click_position:
#         cv.circle(image, click_position, 5, (0, 255, 0), -1)
#         cv.imshow("Click Image", image)
#         cv.waitKey(0)
#     else:
#         print(f"未找到文字：{click_text}")
