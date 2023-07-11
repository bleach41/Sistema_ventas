""" algo """
from kivy.app import App
# from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
# import kivy.properties as BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior


# inventario de prueba /ESTO DEBRIA HACERSE PARA LA BASE DE DATOS

class Property:
    ''' Tuve que implementar property porque no se importa de kivy '''

    def __init__(self, defaultvalue=None, options=None, **kwargs):
        self.name = None
        self.observers = []
        self.dependencies = []
        self.fbinds = {}
        self.bindings = []
        self.cache = {}
        self.defaultvalue = defaultvalue
        self.options = options or {}
        self.kwargs = kwargs


class BooleanProperty(Property):
    ''' Adds selection and focus behaviour to the view. '''

    def __init__(self, defaultvalue=True, **kw):
        super().__init__(defaultvalue=defaultvalue, **kw)


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):

    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': str(x)} for x in range(100)]


inventario = {
    "producto1": {"id": 1, "nombre": "producto1", "cantidad": 10, "precio": 100},
    "producto2": {"id": 2, "nombre": "producto2", "cantidad": 20, "precio": 200},
    "producto3": {"id": 3, "nombre": "producto3", "cantidad": 30, "precio": 300},
}

# IMPLEMENTACION DE RV/RecyleVi


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
