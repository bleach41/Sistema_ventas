from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock

PRODUCTOS = [
    {'nombre': 'Producto 1', 'precio': 10.99},
    {'nombre': 'Producto 2', 'precio': 15.99},
    {'nombre': 'Producto 3', 'precio': 7.99},
    {'nombre': 'Producto 4', 'precio': 20.99},
    {'nombre': 'Producto 5', 'precio': 12.99}
]


class MyTextInput(TextInput):
    def __init__(self, **kwargs):
        super(MyTextInput, self).__init__(**kwargs)

        self.dropdown = DropDown()
        self.dropdown.z_index = 100

        for producto in PRODUCTOS:
            btn = Button(text='{} (${:.2f})'.format(producto['nombre'], producto['precio']),
                         size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)

        self.size_hint = (1, None)
        self.height = 44

    def update_dropdown(self, text):
        self.dropdown.clear_widgets()
        for producto in PRODUCTOS:
            if text.lower() in producto['nombre'].lower():
                btn = Button(text='{} (${:.2f})'.format(producto['nombre'], producto['precio']),
                             size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
                self.dropdown.add_widget(btn)

        if self.dropdown.children:
            self.dropdown.open(self)
        else:
            self.dropdown.dismiss()

    def on_text(self, instance, text):
        self.update_dropdown(text)


class MyBoxLayout(BoxLayout):
    pass


class MainWidget(Widget):
    pass


kv = '''
<MyTextInput>:
    multiline: False

<MyBoxLayout>:
    padding: 10
    spacing: 10

    MyTextInput:
        size_hint_y: None
        height: 44


<MainWidget>:
    MyBoxLayout:
        size_hint: 0.8, 0.8
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
'''


class TestApp(App):
    def build(self):
        Builder.load_string(kv)
        return MainWidget()


if __name__ == '__main__':
    TestApp().run()
