from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.button import Button


class MyPopup(Popup):
    def __init__(self, **kwargs):
        super(MyPopup, self).__init__(**kwargs)
        self.auto_dismiss = False

        self.button = Button(text='Salir', size_hint=(None, None), pos_hint={
                             'center_x': 0.5, 'center_y': 0.5})
        self.button.bind(on_press=self.dismiss_popup)
        self.content.add_widget(self.button)

    def on_touch_up(self, touch):
        if not self.collide_point(*touch.pos):
            self.auto_dismiss = True
            self.button.disabled = False
        return super(MyPopup, self).on_touch_up(touch)

    def dismiss_popup(self, *args):
        self.dismiss()
        self.auto_dismiss = False
        self.button.disabled = True


class MyApp(App):
    def build(self):
        button = Button(text='Abrir Popup', on_press=self.open_popup)
        return button

    def open_popup(self, *args):
        popup = MyPopup()
        popup.open()


if __name__ == '__main__':
    MyApp().run()
