""" algo """
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.textinput import TextInput

# inventario de prueba /ESTO DEBRIA HACERSE PARA LA BASE DE DATOS

inventario = {
    "producto1": {"id": 1, "nombre": "producto1", "cantidad": 10, "precio": 100},
    "producto2": {"id": 2, "nombre": "producto2", "cantidad": 20, "precio": 200},
    "producto3": {"id": 3, "nombre": "producto3", "cantidad": 30, "precio": 300},
}


class Ventas(BoxLayout):
    """Class representing The ROOT"""

    # """Implementacion de los Textinput"""

    def agregar_producto_id(self, codigo):
        try:
            codigo = int(codigo)
            if isinstance(codigo, int):
                for producto in inventario.values():
                    if codigo == producto['id']:
                        print("se encontro", producto)
                        break
                else:
                    print("no encontrado")
        except ValueError:
            print("entrada no valida")

    def agregar_producto_nombre(self, nombre):
        """Busqueda por nombre"""
        try:
            for producto in inventario.values():
                if nombre == producto['nombre']:
                    print("se encontro", producto)
                    break
            else:
                print("no encontrado")
        except ValueError:
            print("entrada no valida")

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

    def pagar(self):
        """Implementar un boton para definir un acnatidad"""
        print("pagar")

    def nueva_compra(self):
        """Implementar un boton para definir un acnatidad"""
        print("nueva compra")

    def cancelar(self):
        """Implementar un boton para definir un acnatidad"""
        print("cancelar")

    def imprimir(self):
        """Implementar un boton para definir un acnatidad"""
        print("imprimir")


class VentasApp(App):
    """Class representing root"""

    def build(self):
        return Ventas()


if __name__ == '__main__':
    VentasApp().run()
