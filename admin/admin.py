from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview import RecycleView
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from sqlqueries import QueriesSQLite
from datetime import datetime, timedelta
import csv
Builder.load_file('admin/admin.kv')


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    touch_deselect_last = BooleanProperty(True)


class SelectableProductoLabel(RecycleDataViewBehavior, BoxLayout):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.ids['_hashtag'].text = str(1+index)
        self.ids['_codigo'].text = str(data['id'])
        self.ids['_articulo'].text = data['nombre'].capitalize()
        self.ids['_cantidad'].text = str(data['cantidad'])
        self.ids['_precio'].text = str("{:.2f}".format(data['precio']))
        return super(SelectableProductoLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        if super(SelectableProductoLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            rv.data[index]['seleccionado'] = True
        else:
            rv.data[index]['seleccionado'] = False


class SelectableUsuarioLabel(RecycleDataViewBehavior, BoxLayout):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.ids['_hashtag'].text = str(1+index)
        self.ids['_nombre'].text = data['nombre'].title()
        self.ids['_username'].text = data['username']
        self.ids['_tipo'].text = str(data['tipo'])
        return super(SelectableUsuarioLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        if super(SelectableUsuarioLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            rv.data[index]['seleccionado'] = True
        else:
            rv.data[index]['seleccionado'] = False


class AdminRV(RecycleView):
    def __init__(self, **kwargs):
        super(AdminRV, self).__init__(**kwargs)
        self.data = []

    def agregar_datos(self, datos):
        for dato in datos:
            dato['seleccionado'] = False
            self.data.append(dato)
        self.refresh_from_data()

    def dato_seleccionado(self):
        indice = -1
        for i in range(len(self.data)):
            if self.data[i]['seleccionado']:
                indice = i
                break
        return indice


class ProductoPopup(Popup):
    def __init__(self, agregar_callback, **kwargs):
        super().__init__(**kwargs)
        self.agregar_callback = agregar_callback

    def abrir(self, agregar, producto=None):
        if agregar:
            self.ids.producto_info_1.text = 'Agregar producto'
            self.ids.producto_codigo.disabled = False
        else:
            self.ids.producto_info_1.text = 'Modificar producto'
            self.ids.producto_codigo.text = str(producto['id'])
            self.ids.producto_codigo.disabled = True
            self.ids.producto_nombre.text = producto['nombre']
            self.ids.producto_cantidad.text = str(producto['cantidad'])
            self.ids.producto_precio.text = str(producto['precio'])
        self.open()

    def verificar_aceptar(self, codigo, nombre, cantidad, precio):
        alert1 = 'falta: '
        alert2 = ''
        validado = {}
        if not codigo:
            alert1 += 'codigo. '
            validado['id'] = False
        else:
            try:
                numeric = int(codigo)
                validado['id'] = numeric
            except:
                alert2 += 'codigo no valido.'
                validado['codigo'] = False

        if not nombre:
            alert1 += 'nombre. '
            validado['nombre'] = False
        else:
            validado['nombre'] = nombre.lower()

        if not precio:
            alert1 += 'precio. '
            validado['precio'] = False
        else:
            try:
                numeric = float(precio)
                validado['precio'] = numeric
            except:
                alert2 += 'precio no valido.'
                validado['precio'] = False

        if not cantidad:
            alert1 += 'cantidad. '
            validado['cantidad'] = False
        else:
            try:
                numeric = int(cantidad)
                validado['cantidad'] = numeric
            except:
                alert2 += 'cantidad no valida.'
                validado['cantidad'] = False

        valores = list(validado.values())
        if False in valores:
            self.ids.no_valid_notif.text = alert1+alert2
        else:
            self.ids.no_valid_notif.text = 'Validado'
            # validado['cantidad'] = int(validado['cantidad'])
            # validado['precio'] = float(validado['precio'])
            self.agregar_callback(True, validado)
            self.dismiss()


class UsuarioPopup(Popup):
    def __init__(self, agregar_callback, **kwargs):
        super().__init__(**kwargs)
        self.agregar_usuario = agregar_callback

    def abrir(self, agregar, usuario=None):
        if agregar:
            self.ids.usuario_info_1.text = 'Agregar usuario'
            self.ids.usuario_username.disabled = False
        else:
            self.ids.usuario_info_1.text = 'Modificar usuario'
            self.ids.usuario_username.text = usuario['username']
            self.ids.usuario_username.disabled = True
            self.ids.usuario_nombre.text = usuario['nombre']
            self.ids.usuario_password.text = usuario['password']
            if usuario['tipo'] == 'admin':
                self.ids.admin_tipo.state = 'down'
            else:
                self.ids.trabajador_tipo.state = 'down'
        self.open()

    def verificar_aceptar(self, usuario_username, usuario_nombre, usuario_password, admin_tipo, trabajador_tipo):
        alert1 = 'Falta: '
        validado = {}
        if not usuario_username:
            alert1 += 'Username. '
            validado['username'] = False
        else:
            validado['username'] = usuario_username

        if not usuario_nombre:
            alert1 += 'Nombre. '
            validado['nombre'] = False
        else:
            validado['nombre'] = usuario_nombre.lower()

        if not usuario_password:
            alert1 += 'Password. '
            validado['password'] = False
        else:
            validado['password'] = usuario_password

        if admin_tipo == 'normal' and trabajador_tipo == 'normal':
            alert1 += 'Tipo. '
            validado['tipo'] = False
        else:
            if admin_tipo == 'down':
                validado['tipo'] = 'admin'
            else:
                validado['tipo'] = 'trabajador'

        valores = list(validado.values())

        if False in valores:
            self.ids.no_valid_notif.text = alert1
        else:
            self.ids.no_valid_notif.text = ''
            self.agregar_usuario(True, validado)
            self.dismiss()


class CustomDropDown(DropDown):
    def __init__(self, cambiar_callback, **kwargs):
        self._succ_cb = cambiar_callback
        super().__init__(**kwargs)

    def vista(self, vista):
        if callable(self._succ_cb):
            self._succ_cb(True, vista)


class InfoVentaPopup(Popup):
    connection = QueriesSQLite.create_connection(
        "ventas/db_ventas/inventario.sqlite")

    def __init__(self, venta, **kwargs):
        super(InfoVentaPopup, self).__init__(**kwargs)
        select_item_query = ("SELECT nombre from productos WHERE id=?")
        self.venta = [{'id': producto[3], 'producto':QueriesSQLite.execute_read_query(self.connection, select_item_query, (
            producto[3],))[0][0], 'cantidad':producto[4], 'precio':producto[2], 'total':producto[4]*producto[2]} for producto in venta]
        print(self.venta)

    def mostrar(self):
        self.open()
        total_items = 0
        total_dinero = 0
        for articulo in self.venta:
            total_items += articulo['cantidad']
            total_dinero += articulo['precio']
        self.ids.total_items.text = str(total_items)
        self.ids.total_dinero.text = '$'+str('{:.2f}'.format(total_dinero))
        self.ids.info_rv.agregar_datos(self.venta)


class VistaVentas(Screen):
    def __init__(self, **kw):
        productos_actuales = []
        super().__init__(**kw)

    def crear_csv(self):
        connection = QueriesSQLite.create_connection(
            "ventas/db_ventas/inventario.sqlite")
        select_item_query = """SELECT nombre FROM productos WHERE id = ? """
        if self.ids.ventas_rv.data:
            csv_nombre = "ventas_csv/" + self.ids.date_id.text+".csv"
            productos_csv = []
            total = 0
            for venta in self.productos_actuales:
                for item in venta:
                    item_found = next(
                        (producto for producto in productos_csv if producto['id'] == item[3]), None)
                    total += item[2]*item[4]
                    if item_found:
                        item_found['cantidad'] += item[4]
                        item_found['precio_total'] = item_found['precio'] * \
                            item_found['cantidad']
                    else:
                        nombre = QueriesSQLite.execute_read_query(
                            connection, select_item_query, (item[3],))[0][0]
                        productos_csv.append(
                            {'nombre': nombre, 'id': item[3], 'cantidad': item[4], 'precio': item[2], 'precio_total': item[2]*item[4]})
            fieldname = ['nombre', 'id', 'cantidad', 'precio', 'precio_total']
            bottom = [{'precio_total': total}]
            with open(csv_nombre, 'w', encoding='UTF8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldname)
                writer.writeheader()
                writer.writerows(productos_csv)
                writer.writerows(bottom)

            pass
        else:
            self.ids.notificacion.text = 'NO HAY VENTAS PARA GUARDAR'

    def mas_info(self):
        indice = self.ids.ventas_rv.dato_seleccionado()
        if indice >= 0:
            venta = self.productos_actuales[indice]
            p = InfoVentaPopup(venta)
            p.mostrar()

    def cargar_venta(self, choice='Default'):
        connection = QueriesSQLite.create_connection(
            "ventas/db_ventas/inventario.sqlite")
        valid_input = True
        final_sum = 0
        f_inicio = datetime.strptime('01/01/00', '%d/%m/%y')
        f_fin = datetime.strptime('31/12/2099', '%d/%m/%Y')

        _ventas = []
        _total_productos = []
        select_ventas_query = """SELECT * FROM ventas WHERE fecha BETWEEN ? AND ? """
        select_productos_query = """SELECT * FROM ventas_detalle WHERE id_venta = ? """

        self.ids.ventas_rv.data = []

        if choice == 'Default':
            f_inicio = datetime.today().date()
            f_fin = f_inicio + timedelta(days=1)
            self.ids.date_id.text = str(f_inicio.strftime('%d-%m-%y'))

        elif choice == 'Date':
            date = self.ids.single_date.text
            try:
                f_elegida = datetime.strptime(date, '%d/%m/%y')
            except:
                valid_input = False
            if valid_input:
                f_inicio = f_elegida
                f_fin = f_elegida + timedelta(days=1)
                self.ids.date_id.text = f_elegida.strftime('%d-%m-%y')
        else:
            if self.ids.initial_date.text:
                initial_date = self.ids.initial_date.text
                try:
                    f_inicio = datetime.strptime(initial_date, '%d/%m/%y')
                except:
                    valid_input = False

            if self.ids.last_date.text:
                last_date = self.ids.initial_date.text
                try:
                    f_inicio = datetime.strptime(last_date, '%d/%m/%y')
                except:
                    valid_input = False

            if valid_input:
                self.ids.date_id.text = f_inicio.strftime(
                    '%d-%m-%y')+'-' + f_fin.strftime('%d-%m-%y')

        if valid_input:
            inicio_fin = (f_inicio, f_fin)
            ventas_sql = QueriesSQLite.execute_read_query(
                connection, select_ventas_query, inicio_fin)
            if ventas_sql:
                for ventas in ventas_sql:
                    final_sum += ventas[1]
                    ventas_detalle_sql = QueriesSQLite.execute_read_query(
                        connection, select_productos_query, (ventas[0],))
                    _total_productos.append(ventas_detalle_sql)
                    count = 0
                    if ventas_detalle_sql:
                        for producto in ventas_detalle_sql:
                            print(producto)
                            count += producto[4]

                        _ventas.append({'username': ventas[3], 'productos': count, 'total': ventas[1], 'fecha': datetime.strptime(
                            ventas[2], '%Y-%m-%d %H:%M:%S.%f')})
                self.ids.ventas_rv.agregar_datos(_ventas)
                self.productos_actuales = _total_productos
        self.ids.final_sum.text = '$' + str('{:.2f}'.format(final_sum))
        self.ids.initial_date.text = ''
        self.ids.last_date.text = ''
        self.ids.single_date.text = ''
        self.ids.notificacion.text = 'Datos de Ventas'


class VistaProductos(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.cargar_productos, 1)

    def actualizar_productos_vista_productos(self, productos_actualizados):
        for producto_nuevo in productos_actualizados:
            for productos_viejo in self.ids.rv_productos.data:
                if producto_nuevo['id'] == productos_viejo['id']:
                    productos_viejo['cantidad'] = producto_nuevo['cantidad']
                    break
        self.ids.rv_productos.refresh_from_data()

    def cargar_productos(self, *args):
        _productos = []
        connection = QueriesSQLite.create_connection(
            "ventas/db_ventas/inventario.sqlite")
        inventario_sql = QueriesSQLite.execute_read_query(
            connection, "SELECT * from productos")
        if inventario_sql:
            for producto in inventario_sql:
                _productos.append(
                    {'id': producto[0], 'nombre': producto[1], 'precio': producto[2], 'cantidad': producto[3]})
        self.ids.rv_productos.agregar_datos(_productos)

    def agregar_producto(self, agregar=False, validado=None):
        if agregar:
            print('validado: ', validado)
            producto_tuple = tuple(validado.values())
            connection = QueriesSQLite.create_connection(
                "ventas/db_ventas/inventario.sqlite")

            crear_producto = """
            INSERT INTO
                productos (id, nombre, precio, cantidad)
            VALUES
                (?, ?, ?, ?);
            """
            QueriesSQLite.execute_query(
                connection, crear_producto, producto_tuple)
            self.ids.rv_productos.data.append(validado)
            self.ids.rv_productos.refresh_from_data()
        else:
            popup = ProductoPopup(self.agregar_producto)
            popup.abrir(True)

    def modificar_producto(self, modificar=False, validado=None):
        indice = self.ids.rv_productos.dato_seleccionado()
        if modificar:
            producto_tuple = (
                validado['nombre'], validado['precio'], validado['cantidad'], validado['id'])
            connection = QueriesSQLite.create_connection(
                "ventas/db_ventas/inventario.sqlite")

            actualizar_producto = """
            UPDATE
                productos
            SET
                nombre=?, precio=?, cantidad=?
            WHERE
                id=?        
            """
            QueriesSQLite.execute_query(
                connection, actualizar_producto, producto_tuple)
            self.ids.rv_productos.data[indice]['nombre'] = validado['nombre']
            self.ids.rv_productos.data[indice]['precio'] = validado['precio']
            self.ids.rv_productos.data[indice]['cantidad'] = validado['cantidad']
            self.ids.rv_productos.refresh_from_data()
        elif indice >= 0:
            producto = self.ids.rv_productos.data[indice]
            popup = ProductoPopup(self.modificar_producto)
            popup.abrir(False, producto)

    def eliminar_producto(self):
        indice = self.ids.rv_productos.dato_seleccionado()
        if indice >= 0:
            producto_tuple = (self.ids.rv_productos.data[indice]['id'], )
            connection = QueriesSQLite.create_connection(
                "ventas/db_ventas/inventario.sqlite")
            borrar_producto = """
            DELETE from productos where id=?
            """
            QueriesSQLite.execute_query(
                connection, borrar_producto, producto_tuple)
            self.ids.rv_productos.data.pop(indice)
            self.ids.rv_productos.refresh_from_data()


class VistaUsuarios(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.cargar_usuarios, 1)

    def cargar_usuarios(self, *args):
        _usuarios = []
        connection = QueriesSQLite.create_connection(
            "ventas/db_ventas/inventario.sqlite")
        usuarios_sql = QueriesSQLite.execute_read_query(
            connection, "SELECT * from usuarios")
        if usuarios_sql:
            for usuario in usuarios_sql:
                _usuarios.append(
                    {'nombre': usuario[1], 'username': usuario[0], 'password': usuario[2], 'tipo': usuario[3]})
        self.ids.rv_usuarios.agregar_datos(_usuarios)

    def agregar_usuario(self, agregar=False, validado=None):
        if agregar:
            usuario_tuple = tuple(validado.values())
            connection = QueriesSQLite.create_connection(
                "ventas/db_ventas/inventario.sqlite")
            crear_usuario = """
            INSERT INTO
                usuarios (username, nombre, password, tipo)
            VALUES
                (?,?,?,?);
            """
            QueriesSQLite.execute_query(
                connection, crear_usuario, usuario_tuple)
            self.ids.rv_usuarios.data.append(validado)
            self.ids.rv_usuarios.refresh_from_data()
        else:
            popup = UsuarioPopup(self.agregar_usuario)
            popup.abrir(True)

    def modificar_usuario(self, modificar=False, validado=None):
        indice = self.ids.rv_usuarios.dato_seleccionado()
        if modificar:
            usuario_tuple = (
                validado['nombre'], validado['password'], validado['tipo'], validado['username'])
            connection = QueriesSQLite.create_connection(
                "ventas/db_ventas/inventario.sqlite")
            actualizar = """
            UPDATE
                usuarios
            SET
                nombre=?, password=?, tipo = ?
            WHERE
                username = ?
            """
            QueriesSQLite.execute_query(connection, actualizar, usuario_tuple)
            self.ids.rv_usuarios.data[indice]['nombre'] = validado['nombre']
            self.ids.rv_usuarios.data[indice]['tipo'] = validado['tipo']
            self.ids.rv_usuarios.data[indice]['password'] = validado['password']
            self.ids.rv_usuarios.refresh_from_data()
        else:
            if indice >= 0:
                usuario = self.ids.rv_usuarios.data[indice]
                popup = UsuarioPopup(self.modificar_usuario)
                popup.abrir(False, usuario)

    def eliminar_usuario(self):
        indice = self.ids.rv_usuarios.dato_seleccionado()
        if indice >= 0:
            usuario_tuple = (self.ids.rv_usuarios.data[indice]['username'],)
            connection = QueriesSQLite.create_connection(
                "ventas/db_ventas/inventario.sqlite")
            borrar = """DELETE from usuarios where username = ?"""
            QueriesSQLite.execute_query(connection, borrar, usuario_tuple)
            self.ids.rv_usuarios.data.pop(indice)
            self.ids.rv_usuarios.refresh_from_data()


class AdminWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vista_actual = 'Productos'
        self.vista_manager = self.ids.vista_manager
        self.dropdown = CustomDropDown(self.cambiar_vista)
        self.ids.cambiar_vista.bind(on_release=self.dropdown.open)

    def cambiar_vista(self, cambio=False, vista=None):
        if cambio:
            self.vista_actual = vista
            self.vista_manager.current = self.vista_actual
            self.dropdown.dismiss()

    def actualizar_productos(self, productos):
        self.ids.vista_productos.actualizar_productos_vista_productos(
            productos)

    def signout(self):
        self.parent.parent.current = 'scrn_signin'

    def venta(self):
        self.parent.parent.current = 'scrn_ventas'

# esto es nuevo tambien en kv


class ItemVentaLabel(RecycleDataViewBehavior, BoxLayout):
    index = None

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.ids['_hashtag'].text = str(1+index)
        self.ids['_codigo'].text = data['id']
        self.ids['_articulo'].text = data['producto'].capitalize()
        self.ids['_cantidad'].text = str(data['cantidad'])
        self.ids['_precio_por_articulo'].text = str(
            "{:.2f}".format(data['precio']))+" /artículo"
        self.ids['_total'].text = str("{:.2f}".format(data['total']))
        return super(ItemVentaLabel, self).refresh_view_attrs(
            rv, index, data)

# esto es nuevo tambien en kv


class SelectableVentaLabel(RecycleDataViewBehavior, BoxLayout):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.ids['_hashtag'].text = str(1+index)
        self.ids['_username'].text = data['username']
        self.ids['_cantidad'].text = str(data['productos'])
        self.ids['_total'].text = '$ '+str("{:.2f}".format(data['total']))
        self.ids['_time'].text = str(data['fecha'].strftime("%H:%M:%S"))
        self.ids['_date'].text = str(data['fecha'].strftime("%d/%m/%Y"))
        return super(SelectableVentaLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        if super(SelectableVentaLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            rv.data[index]['seleccionado'] = True
        else:
            rv.data[index]['seleccionado'] = False


class AdminApp(App):
    def build(self):
        return AdminWindow()


if __name__ == "__main__":
    AdminApp().run()
