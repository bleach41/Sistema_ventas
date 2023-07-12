from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.add_widget(Button(text="Hello, Kivy!"))


class TestApp(App):
    def build(self):
        return MyBoxLayout()


if __name__ == '__main__':
    TestApp().run()
