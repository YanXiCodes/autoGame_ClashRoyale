import cv2 as cv
from cv2 import Mat
import numpy as np
from pprint import pprint
import pytesseract


def preprocess_image(image: Mat):
    target_height, target_width = 320, 320
    image = cv.resize(image, (target_width, target_height))
    image = image.astype(np.float32)
    image = np.transpose(image, (2, 0, 1))  # 转换为 [channels, height, width]
    image = np.expand_dims(
        image, axis=0
    )  # 添加批次维度，转换为 [batch_size, channels, height, width]
    return image


def predict(image):
    data = pytesseract.image_to_data(image,lang='chi_sim', output_type=pytesseract.Output.DICT)
    # 提取文字及其位置信息
    text_positions = []
    for i in range(len(data["text"])):
        if int(data["conf"][i]) > 0:  # 过滤掉置信度为0的结果
            text_info = {
                "text": data["text"][i],
                "left": data["left"][i],
                "top": data["top"][i],
                "width": data["width"][i],
                "height": data["height"][i],
            }
            text_positions.append(text_info)

    return text_positions


if __name__ == "__main__":
    image = cv.imread(r"D:\\ClashRoyale\\docs\\images\\flow\\1723708311817.png")
    
    pprint(predict(image))
