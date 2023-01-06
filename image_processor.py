import cv2


class ImageProcessor:

    def __init__(self, image):
        self.faces = None
        self.image = image

    def detect_faces(self):
        img = cv2.imread(self.image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(
            'haarcascade_frontalface_default.xml')
        self.faces = list(face_cascade.detectMultiScale(gray, 1.1, 4))
        return self.faces
