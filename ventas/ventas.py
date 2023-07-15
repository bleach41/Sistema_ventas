""""h"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup import Popup
from kivy.properties import BooleanProperty  # Aqui da error


# inventario de prueba /ESTO DEBRIA HACERSE PARA LA BASE DE DATOS
inventario = [
    {"id": 111, "nombre": "leche", "cantidad": 10, "precio": 100},
    {"id": 222, "nombre": "huevo", "cantidad": 20, "precio": 200},
    {"id": 333, "nombre": "arroz", "cantidad": 30, "precio": 300},
    {"id": 444, "nombre": "arroz negro", "cantidad": 30, "precio": 200},
    {"id": 555, "nombre": "azucar", "cantidad": 30, "precio": 100},
    {"id": 666, "nombre": "frijoles", "cantidad": 30, "precio": 500},
]


class AgregarProductoPopup(Popup):
    def __init__(self, input_nombre, gregar_producto_rvs_callback, **kwargs):
        super().__init__(**kwargs)
        self.input_nombre = input_nombre
        self.agregar_producto_rv = gregar_producto_rvs_callback

    def coincidencia_product(self):
        self.open()
        for nombre in inventario:
            print("##################", nombre)
            if nombre['nombre'].lower().find(self.input_nombre.lower()) >= 0:
                producto = {}
                producto = {
                    "id": nombre['id'],
                    "nombre": nombre['nombre'],
                    "cantidad": nombre['cantidad'],
                    "precio": nombre['precio']
                }
                self.ids.rvs.agregar_articulo(producto)

    def select_producto_popup(self):
        indice = self.ids.rvs.producto_seleccionado_rvs()
        if indice >= 0:
            producto = self.ids.rvs.data[indice]
            articulo = {}
            articulo['id'] = producto['id']
            articulo['nombre'] = producto['nombre']
            articulo['precio'] = producto['precio']
            articulo['cantidad_carrito'] = 1
            articulo['cantidad_inventario'] = producto['cantidad']
            articulo['precio_total'] = producto['precio']
            if callable(self.agregar_producto_rv):
                self.agregar_producto_rv(articulo)
            self.dismiss()

# AKI SE BORRRO LA IMPLEMENTACION DE BOOLEANPROPERTY PORQUE AUNKE
# LA IMPORTACION DA ERROR SI SE ESTA USANDO...ESTO SE HABIA HECHO
# PARA CONVENCION DEL VS CODE
# class Property:
#     ''' Tuve que implementar property porque no se importa de kivy '''

#     def __init__(self, defaultvalue=None, options=None, **kwargs):
#         self.name = None
#         self.observers = []
#         self.dependencies = []
#         self.fbinds = {}
#         self.bindings = []
#         self.cache = {}
#         self.defaultvalue = defaultvalue
#         self.options = options or {}
#         self.kwargs = kwargs


# class BooleanProperty(Property):
#     ''' Adds selection and focus behaviour to the view. '''

#     def __init__(self, defaultvalue=True, **kw):
#         super().__init__(defaultvalue=defaultvalue, **kw)


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):

    ''' Adds selection and focus behaviour to the view. '''
    touch_deselect_last = BooleanProperty(True)


class SelectableLabelBoxLayaout(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    # background_color: ListProperty([0, 0, 0, 0])

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        self.ids['numero'].text = str(1+index)
        self.ids['nombre_p'].text = data['nombre'].capitalize()
        self.ids['cantidad_p'].text = str(data['cantidad_carrito'])
        self.ids['precio_p'].text = str("{:.2f}".format(data['precio']))
        self.ids['total_p'].text = str("{:.2f}".format(data['precio_total']))
        return super(SelectableLabelBoxLayaout, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabelBoxLayaout, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            rv.data[index]["seleccionado"] = True
            print("selection changed to {0}".format(rv.data[index]))
        else:
            rv.data[index]["seleccionado"] = False
            print("selection removed for {0}".format(rv.data[index]))

# SelectableLabel para al Popup


class SelectableLabelBoxLayaoutPopup(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        self.ids['id'].text = str(data['id'])
        self.ids['nombre_p'].text = data['nombre']
        self.ids['cantidad_p'].text = str(data['cantidad'])
        self.ids['precio_p'].text = str("{:.2f}".format(data['precio']))
        return super(SelectableLabelBoxLayaoutPopup, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabelBoxLayaoutPopup, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            rv.data[index]["seleccionado"] = True
            print("selection changed to {0}".format(rv.data[index]))
        else:
            rv.data[index]["seleccionado"] = False
            print("selection removed for {0}".format(rv.data[index]))

# POPUP PARA CAMBIAR LA CANTIDAD


class CambiarCantidadPopup(Popup):
    def __init__(self, data, actualizar_articulo_callback, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.actualizar_articulo = actualizar_articulo_callback
        self.ids.producto.text = "producto: " + self.data['nombre']
        self.ids.cantidad.text = "cant: " + str(self.data['cantidad_carrito'])

    def validar_cantidad_popup(self, text_input):
        try:
            nueva_cant = int(text_input)
            print(text_input, nueva_cant)
            self.ids.invalid_cantidad.text = ''
            self.actualizar_articulo(nueva_cant)
            self.dismiss()
        except:
            self.ids.invalid_cantidad.text = "Cantidad no valida"


class NuevaCompraPopup(Popup):
    def __init__(self, nueva_compra_callback, **kwargs):
        super().__init__(**kwargs)
        self.nueva_compra = nueva_compra_callback
        self.ids.aceptar_nueva_compra.bind(on_release=self.dismiss)


class RV(RecycleView):
    """IMPLEMENTACION DE RV/RecyleVi"""

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []
        self.modificar_cantidad = None

    def agregar_articulo(self, articulo):
        articulo['seleccionado'] = False
        indice = -1
        if self.data:
            for i in range(len(self.data)):
                if articulo['id'] == self.data[i]['id']:
                    indice = i
            if indice >= 0:
                self.data[indice]['cantidad_carrito'] += 1
                self.data[indice]['precio_total'] = self.data[indice]['precio'] * \
                    self.data[indice]['cantidad_carrito']
                self.refresh_from_data()
            else:
                self.data.append(articulo)
        else:
            self.data.append(articulo)

    def producto_seleccionado_rvs(self):
        indice = -1
        for i in range(len(self.data)):
            if self.data[i]['seleccionado']:
                indice = i
                break
        return indice

    def eliminar_product_rv(self):
        indice = self.producto_seleccionado_rvs()
        precio = 0
        if indice >= 0:
            self._layout_manager.deselect_node(
                self._layout_manager._last_selected_node)
            precio = self.data[indice]['precio_total']
            self.data.pop(indice)
            self.refresh_from_data()
        return precio

    def modificar_cantidad_rv(self):
        indice = self.producto_seleccionado_rvs()
        if indice >= 0:
            popup = CambiarCantidadPopup(
                self.data[indice], self.actualizar_articulo)
            popup.open()

    def actualizar_articulo(self, nueva_cant):
        indice = self.producto_seleccionado_rvs()
        if indice >= 0:
            if nueva_cant == 0:
                self.data.pop(indice)
                self._layout_manager.deselect_node(
                    self._layout_manager._last_selected_node)
            else:
                self.data[indice]['cantidad_carrito'] = nueva_cant
                self.data[indice]['precio_total'] = self.data[indice]['precio'] * nueva_cant
                self.refresh_from_data()
                nuevo_total = 0
                for data in self.data:
                    nuevo_total += data['precio_total']
                self.modificar_cantidad(False, nuevo_total)


class PagarPopup(Popup):
    def __init__(self, total, pagado_callback, **kwargs):
        super(PagarPopup, self).__init__(**kwargs)
        self.total = total
        self.pagado = pagado_callback
        self.ids.total.text = '$'+'{:.2f}'.format(self.total)
        self.ids.boton_pagar.bind(on_release=self.dismiss)

    def mostrar_cambio(self):
        recibido = self.ids.recibido.text
        try:
            cambio = float(recibido)-float(self.total)
            if cambio >= 0:
                self.ids.cambio.text = '$'+'{:.2f}'.format(cambio)
                self.ids.boton_pagar.disabled = False
            else:
                self.ids.cambio.text = 'Faltan: '+'$'+'{:.2f}'.format(cambio)
        except:
            self.ids.cambio.text = 'Pago no valido'
# esto serviria igual
    # def terminar_pago(self):
    #     self.dismiss()
    #     self.pagado()


class Ventas(BoxLayout):
    """Class representing The ROOT"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total = 0.0
        self.ids.rvs.modificar_cantidad = self.modificar_cantidad

    def agregar_producto_id(self, codigo):
        """agregar producto el RV"""
        try:
            codigo = int(codigo)
            if isinstance(codigo, int):
                for producto in inventario:
                    if codigo == producto['id']:
                        articulo = {}
                        articulo['id'] = producto['id']
                        articulo['nombre'] = producto['nombre']
                        articulo['precio'] = producto['precio']
                        articulo['cantidad_carrito'] = 1
                        articulo['cantidad_inventario'] = producto['cantidad']
                        articulo['precio_total'] = producto['precio']
                        self.agregar_producto_rv(articulo)
                        self.ids.buscar_x_id.text = ''
                        print("se encontro", articulo)
                        break
                else:
                    print("no encontrado")
        except ValueError:
            print("entrada no valida")

    def agregar_producto_rv(self, articulo):
        self.ids.rvs.agregar_articulo(articulo)
        self.total += articulo['precio']
        self.ids.subtotal.text = "$" + "{:.2f}".format(self.total)

    def agregar_producto_nombre(self, nombre):
        """Busqueda por nombre"""
        popup = AgregarProductoPopup(nombre, self.agregar_producto_rv)
        popup.coincidencia_product()

    # """Implementacion de los botones"""

    def admin(self):
        """Implementar boton para loguear"""
        print("presionaste admin")

    def salir(self):
        """Implementar boton para salir del user"""
        print("saliendo")

    def eliminar_product(self):
        """Implementar boton para eliminar u producto"""
        menos_precio = self.ids.rvs.eliminar_product_rv()
        self.total -= menos_precio
        self.ids.subtotal.text = "$"+"{:.2f}".format(self.total)

    def modificar_cantidad(self, cambio=True, nuevo_total=None):
        """Implementar un boton para definir un acnatidad"""
        if cambio:
            self.ids.rvs.modificar_cantidad_rv()
            print("cantidad:")
        else:
            self.total = nuevo_total
            self.ids.subtotal.text = "$"+"{:.2f}".format(self.total)

    def pagar(self):
        """Implementar un boton para definir un acnatidad"""
        if self.ids.rvs.data:
            popup = PagarPopup(self.total, self.pagado)
            popup.open()
        else:
            self.ids.notificacion_falla.text = 'No hay nada que pagar'
        print("pagar")

    def pagado(self):
        self.ids.notificacion_exito.text = 'PAGO CORRECTO'
        self.ids.notificacion_falla.text = ''
        self.ids.total.text = "$"+"{:.2f}".format(self.total)
        self.ids.buscar_x_id.disabled = True
        self.ids.buscar_x_nombre.disabled = False

        nueva_cantidad = []
        for producto in self.ids.rvs.data:
            cantidad = producto['cantidad_inventario'] - \
                producto['cantidad_carrito']
            if cantidad >= 0:
                nueva_cantidad.append(
                    {'id': producto['id'], 'cantidad': cantidad})
            else:
                nueva_cantidad.append({'id': producto['id'], 'cantidad': 0})
        for i in nueva_cantidad:
            resultado = next(
                (producto for producto in inventario if producto['id'] == i['id']), None)
            resultado['cantidad'] = i['cantidad']

    def nueva_compra(self, desde_popup=False):
        """Implementar un boton para definir un acnatidad"""
        if desde_popup:
            self.ids.rvs.data = []
            self.total = 0.0
            self.ids.subtotal.text = '00.00'
            self.ids.total.text = '00.00'
            self.ids.notificacion_exito.text = 'PAGO CORRECTO'
            self.ids.notificacion_falla.text = ''
            self.ids.notificacion_exito.text = ''
            self.ids.buscar_x_id.disabled = False
            self.ids.buscar_x_nombre.disabled = False
            self.ids.rvs.refresh_from_data()
        elif len(self.ids.rvs.data):
            popup = NuevaCompraPopup(self.nueva_compra)
            popup.open()

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
