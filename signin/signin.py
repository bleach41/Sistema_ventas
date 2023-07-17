from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from sqlqueries import QueriesSQLite

Builder.load_file('signin/signin.kv')


class SigninWindow(BoxLayout):
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)

    def verificar_usuario(self, username, password):
        connection = QueriesSQLite.create_connection(
            "ventas/db_ventas/inventario.sqlite")
        select_users = "SELECT * from usuarios"
        users = QueriesSQLite.execute_read_query(connection, select_users)
        if username == '' or password == '':
            self.ids.signin_notificacion.text = 'Completa el formulario'
        else:
            usuario = {}
            for user in users:
                print(user)
                print('*************')
                if username == user[0]:
                    print('###############')
                    usuario['username'] = user[0]
                    usuario['nombre'] = user[1]
                    usuario['password'] = user[2]
                    usuario['tipo'] = user[3]
                    break
            if usuario:
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!')
                if usuario['password'] == password:
                    print('@@@@@@@@@@@@@@@@@')
                    self.ids.username.text = ''
                    self.ids.password.text = ''
                    self.ids.signin_notificacion.text = ''
                    self.parent.parent.current = 'scrn_ventas'
                else:
                    self.ids.signin_notificacion.text = 'Nombre de usario incorrecto'

            else:
                self.ids.signin_notificacion.text = 'Nombre de usario incorrecto'


class SigninApp(App):
    def build(self):
        return SigninWindow()


if __name__ == '__main__':
    SigninApp().run()
