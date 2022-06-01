import cv2


class FacialDetect:
    """This class is available to do facial recognition on the image"""

    def __init__(self):
        self.width = 600
        self.height = 300
        self.error_marge = 150
        self.facial_classifier = "./facial_detection/Ressources/Classifiers/haarcascade_frontalface_alt2.xml"
        self.profile_classifier = "./facial_detection/Ressources/Classifiers/haarcascade_profileface.xml"
        self.face_cascade = None
        self.profile_cascade = None

    @staticmethod
    def capture_video(num):
        """Allow u to choise which camera, u want to use"""
        return cv2.VideoCapture(num)

    def resize_image(self, image):
        dimension = (self.width, self.height)
        return cv2.resize(image, dimension, interpolation=cv2.INTER_AREA)

    @staticmethod
    def adjust_image(image, capture):
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        dimension = (width, height)
        return cv2.resize(image, dimension, interpolation=cv2.INTER_AREA)

    def init_cascade_file(self):
        try:
            with open(self.facial_classifier):
                pass
            with open(self.profile_classifier):
                pass
        except IOError:
            print("fichier %s inexistant")
            exit(-1)
        self.face_cascade = cv2.CascadeClassifier(self.facial_classifier)
        self.profile_cascade = cv2.CascadeClassifier(self.profile_classifier)

    def process(self, image):
        # debut de la gestion de la reconnaissance
        tab_face = []
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        result = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4, minSize=(5, 5))
        for x, y, w, h in result:
            tab_face.append([x, y, x + w, y + h])
        result = self.profile_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4)
        for x, y, w, h in result:
            tab_face.append([x, y, x + w, y + h])
        result = self.profile_cascade.detectMultiScale(cv2.flip(gray, 1), scaleFactor=1.2, minNeighbors=4)
        for x, y, w, h in result:
            tab_face.append([self.width - x, y, self.width - (x + w), y + h])
        index = 0
        for x, y, x2, y2 in tab_face:
            if not index \
                    or (x - tab_face[index - 1][0] > self.error_marge or y - tab_face[index - 1][1] > self.error_marge):
                cv2.rectangle(image, (x, y), (x2, y2), (0, 0, 255), 2)
            index += 1

        return image
