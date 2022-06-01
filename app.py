from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang.builder import Builder
from kivymd.uix.menu import MDDropdownMenu
from facial_detection.FacialDetect import FacialDetect
import cv2


class Manual(Screen):
    """Screen use for manage drone manualy and display the facial tracking image"""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.fd: FacialDetect = FacialDetect()  # initialise notre objet facial detect
        self.capture = FacialDetect.capture_video(0)  # on connecte notre camera
        self.fd.init_cascade_file()  # init cascade which u use
        # affichage d'image apres une certaine period
        Clock.schedule_interval(self.do_tracking, 1.0 / 60.0)
        self.menu = None
        self.menu_items = [
            {
                "text": f"File",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"File": self.menu_callback(x),
            },
            {
                "text": f"Preferences",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"Preferences": self.menu_callback(x),
            },
        ]
        self.menu = MDDropdownMenu(
            items=self.menu_items,
            width_mult=2,
            position="bottom",
        )

    def dropdown(self, instance):
        self.menu.caller = instance
        self.menu.elevation = 10
        self.menu.open()

    @staticmethod
    def menu_callback(text_item):
        print(text_item)

    def open_menu(self):
        pass

    def do_tracking(self, *args):
        success, image = self.capture.read()
        if not success:
            return
        image = FacialDetect.adjust_image(image, capture=self.capture)
        image_processed = self.fd.process(image)
        buffer = bytes(cv2.flip(image_processed, 0))
        texture = Texture.create(size=(image_processed.shape[1], image_processed.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.ids.track_manual_image.texture = texture


class SelectMode(Screen):
    def switch_to_manual(self):
        try:
            self.manager.switch_to(Manual(), direction='right', duration=1)
        except Exception as e:
            print(e)


class FrontFace(Screen):
    def on_enter(self):
        """Change la fenêtre principal après 7 secondes d'attente"""
        Clock.schedule_once(self.change_screen, 7)

    def change_screen(self, time):
        """Une fois l'évènement on_enter survenu, cette fonction permettra de
        switcher de la fenetre Frontface vers la fenètre WifiPage"""
        try:
            self.manager.switch_to(WifiPage(), direction='right', duration=1)
        except Exception as e:
            print(e)


class WifiPage(Screen):
    pass


class FrontApp(ScreenManager):
    pass


class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.path_to_kv_file = "manual.kv"

    def build(self):
        return Builder.load_file("frontapp.kv")


if __name__ == "__main__":
    MyApp().run()
