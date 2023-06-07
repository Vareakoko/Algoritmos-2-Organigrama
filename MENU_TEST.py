import customtkinter as ctk
import os
import datetime
import random
import psycopg2
from PIL import Image


class Interfaz_Organigrama(ctk.CTkToplevel):        #Esta es la interfaz vacía donde estaría yendo el organigrama cargado
    def __init__(self, master):
        super().__init__(master)
        self.title(" ORGANIPLANNER ")
        self.geometry("800x650")
        self.state(newstate="withdraw")
        self.iconbitmap("logo3.ico")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.frame_op = ctk.CTkFrame(self)
        self.frame_op.pack(row=0, column=0, padx=0, pady=650, expand=True, fill="both")

        self.frame_org = ctk.CTkCanvas(self)
        self.frame_org.pack(row=1, column=0, padx=10, pady=10)


class FrameBotonOrganigramas(ctk.CTkFrame):         #Estos son los botones con las funciones determinadas
    def __init__(self, master):                     #para mi que load_data tiene que cambiarse para que pueda
        super().__init__(master)                    #abrir los archivos de los organigramas
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        # Añade botones para cargar organigramas o eliminarlos
        self.add_button = ctk.CTkButton(self, text="Abrir", command=self.load_data)
        self.add_button.grid(row=1, column=0, padx=20, pady=(5, 5), sticky="ew")
        self.delete_button = ctk.CTkButton(self, text="Eliminar", command=self.delete_file)
        self.delete_button.grid(row=1, column=1, padx=20, pady=(5, 5), sticky="ew")

    def load_data(self):
        # Establecer la conexión
        conexion = psycopg2.connect(
            host="localhost",
            database="DATOS_ORGANIGRAMA",
            user="postgres",
            password="cosmopolitan"
        )

        cursor = conexion.cursor()
        cursor.execute("SELECT COD_ORG, ORG, FEC FROM Organigramas")
        data = cursor.fetchall()

        # Agregar los datos a la tabla
        for row in data:
            cod_org = row[0]
            org = row[1]
            fec = row[2]

            self.add_item(f"COD_ORG: {cod_org}, ORG: {org}, FEC: {fec}")

        cursor.close()
        conexion.close()

    def delete_file(self):
        selected_item = self.get_selected_item()            #Tiene funciones que todavía no estan definidas
        if selected_item:
            file_info = self.get_item_text(selected_item)
            file_name = file_info.split(" - ")[0]

            # Establecer la conexión
            conexion = psycopg2.connect(
                host="localhost",
                database="DATOS_ORGANIGRAMA",
                user="postgres",
                password="cosmopolitan"
            )

            cursor = conexion.cursor()
            cursor.execute("DELETE FROM archivos WHERE nombre=%s", (file_name,))
            conexion.commit()

            self.load_data()

            cursor.close()
            conexion.close()


def Generar_Codigo_Unico():                     #Genera un codigo random para la funcion crear_organigrama
    codigo = str(random.randint(00000, 99999))  #el cual se guarda en la base de datos junto con el nombre
                                                #del organigrama y la fecha en la que se creo el archivo
    with open("codes.dat", "a+") as archivo:
        archivo.seek(0)  # Mover el puntero al inicio del archivo
        codigos_guardados = archivo.read().splitlines()

        while codigo in codigos_guardados:
            codigo = str(random.randint(00000, 99999))

        archivo.write(codigo + "\n")

    return codigo


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ORGANIPLANNER - Menu")
        self.geometry("800x450+250+20")  # 800x450
        self.iconbitmap('logo3.ico')
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        self.state(newstate="normal")

        # Imagenes en Version Light y Dark
        self.usuario_image = ctk.CTkImage(light_image=Image.open(os.path.join("images\\usuario_light.png")),
                                          dark_image=Image.open(os.path.join("images\\usuario_dark.png")))
        self.name_image = ctk.CTkImage(light_image=Image.open(os.path.join("images\\nombre_light.png")),
                                       size=(300, 150),
                                       dark_image=Image.open(os.path.join("images\\nombre_dark.png")))
        self.crear_image = ctk.CTkImage(light_image=Image.open(os.path.join("images\\mas_light.png")),
                                        dark_image=Image.open(os.path.join("images\\mas_dark.png")),
                                        size=(20, 20))

        # creacion del frame para navegar (usuario, apariencia y crear)
        self.navigation_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=2)

        # Estaría mejor guardar el frame del usuario en una clase, pero no tengo idea de como hacer eso
        # usuario = self.registrar_usuario() <- Crear funcion para ingresar un usuario a la BdD
        # y mostrar su user como texto en la ventana del menu. (esa ventanita donde dice usuario)
        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text=" Usuario ",
                                                   image=self.usuario_image,
                                                   compound="left",
                                                   font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # Boton de Crear Organigrama
        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=1, height=40, border_spacing=10,
                                         text=" Crear Organigrama ",
                                         fg_color="transparent", text_color=("gray10", "gray90"),
                                         hover_color=("gray70", "gray30"),
                                         image=self.crear_image, anchor="w", command=self.login)
        self.home_button.grid(row=1, column=0, sticky="ew")

        # Menu de Light y Dark
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light"],
                                                      command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # creacion del frame para el logo (donde están el icono y nombre de la aplicacion
        self.home_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.home_frame.grid(row=0, column=0, sticky="nsew")
        self.name_image = ctk.CTkLabel(self.home_frame, text="", image=self.name_image, anchor="center")
        self.name_image.grid(row=1, column=0, padx=160, pady=(20, 0), sticky="ew")

        # Creacion del frame de opciones
        self.frame_botones = FrameBotonOrganigramas(self)
        self.frame_botones.grid(row=1, column=1, padx=(100, 100), pady=(20, 150), sticky="nsew")

        # creacion del frame de los archivos de organigramas
        self.second_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # Creacion del tercer frame
        self.third_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # seleccion de un frame
        self.select_frame_by_name("home")

    def agregar_organigrama(self):      #Ingresar el nombre del Organigrama y generar sus datos
        organizacion = ctk.CTkInputDialog(text="Ingrese el nombre de su Organizacion", title=" ORGANIPLANNER ")

        codigo = Generar_Codigo_Unico()

        fecha = datetime.datetime.now().strftime("%d-%m-%y")

        self.add_data(codigo, organizacion, fecha)

    
    def add_data(cod_org, org, fec):    # Cargar los datos del Organigrama a la Base de Datos
        conexion = psycopg2.connect(
            host="localhost",
            database="DATOS_ORGANIGRAMA",
            user="postgres",
            password="cosmopolitan"
        )

        cursor = conexion.cursor()
        cursor.execute("INSERT INTO Organigramas (COD_ORG, ORG, FEC) VALUES (%s, %s, %s)",
                       (cod_org, org, fec))
        conexion.commit()

        cursor.close()
        conexion.close()

    def select_frame_by_name(self, name):
        # definir el color del boton seleccionado
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")

        # mostrar el boton elegido
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    def login(self):
        ...

    def cargar_organigrama(self):
        ...


if __name__ == "__main__":
    app = App()
    app.mainloop()
