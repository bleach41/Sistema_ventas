""" algo """
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.textinput import TextInput


class Ventas(BoxLayout):
    """Class representing The ROOT"""

    # """Implementacion de los Textinput"""

    def agregar_producto_id(self, codigo):
        """Busqueda por id"""
        print("se mando: ", codigo)

    def agregar_producto_nombre(self, nombre):
        """Busqueda por nombre"""
        print("se mando: ", nombre)

    # """Implementacion de los botones"""

    def admin(self):
        """Implementar boton para loguear"""
        print("presionaste admin")

    def salir(self):
        """Implementar boton para salir del user"""
        print("saliendo")

    def eliminar_product(self):
        """Implementar boton para eliminar u producto"""
        print("se elimino")

    def cantidad(self):
        """Implementar un boton para definir un acnatidad"""
        print("cantidad:")


class VentasApp(App):
    """Class representing root"""

    def build(self):
        return Ventas()


if __name__ == '__main__':
    VentasApp().run()
