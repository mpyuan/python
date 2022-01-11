import cv2
import requests


def get_photo():
    cap = cv2.VideoCapture(0)
    f, frame = cap.read()
    cv2.imwrite('image.jpg', frame)
    cap.release()


def show_image():
    # 读取图片
    image = cv2.imread('D:/tmp/w_20210804090742.jpg')
    # 加载人脸模型库
    face_model = cv2.CascadeClassifier('D:/Programs/Python/Python37/Lib/site-packages/cv2/data/haarcascade_frontalface_alt.xml')
    # 图片进行灰度处理
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # 人脸检测
    faces = face_model.detectMultiScale(gray)
    print(faces)
    # 标记人脸
    for (x, y, w, h) in faces:
    #   #  1.原始图片；2坐标点；3.矩形宽高 4.颜色值(RGB)；5.线框
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # 显示图片窗口
    cv2.imshow('fdafad', image)
    # 窗口暂停
    cv2.waitKey(0)
    # 销毁窗口
    cv2.destroyAllWindows()

    exit(0)

    image = cv2.imread('D:/tmp/w_20210804090701.jpg')

    face_model = cv2.CascadeClassifier('plugins/opencv/haarcascade_frontlcatface.xml')

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    faces = face_model.detectMultiScale(gray)

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('dfadfa', image)

    cv2.waitKey(0)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    # get_photo()
    show_image()
    # data = dict(key1='value1',key2='value2')
    # r = requests.post('https://httpbin.org/post',data=data)
    # print(r.content)
    # print(r.text)
    # print(r.status_code)
    # print(r.encoding)
    # print(r.apparent_encoding)
    # print(r.raise_for_status)
    # print(r.headers)
    # print(r.url)
    # print(r.ok)
    # help(r)
