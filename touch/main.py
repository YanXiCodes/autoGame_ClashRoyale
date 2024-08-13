import cv2 as cv
from pyscrcpy import Client # import scrcpy client
from adbutils import AdbDevice


def on_frame(client: Client, frame: cv.typing.MatLike):
    cv.imshow('Video', frame)
    cv.waitKey(1)


if __name__ == '__main__':
    client = Client("emulator-5554", max_fps=60, max_size=900)

    client.on_frame(on_frame)
    client.start()