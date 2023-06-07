import customtkinter as ctk
import os
import psycopg2


class FrameBotonOrganigramas(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid(row=1, column=0, padx=(90, 100), pady=(200, 100), sticky="nsew")

        # Add buttons for deleting and editing files
        self.delete_button = ctk.CTkButton(
            self, text="Eliminar", command=self.delete_file
        )
        self.delete_button.grid(row=2, column=0, padx=10, pady=5)
        self.edit_button = ctk.CTkButton(self, text="Editar", command=self.edit_file)
        self.edit_button.grid(row=3, column=0, padx=10, pady=5)

        # Connect to the database and load data into the table
        self.load_data()

    def load_data(self):
        # Establecer la conexión
        conexion = psycopg2.connect(
            host="localhost",
            database="DATOS_ORGANIGRAMA",
            user="postgres",
            password="cosmopolitan"
        )
        
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre, hora_realizacion FROM archivos")
        data = cursor.fetchall()

        # Limpiar la tabla antes de cargar nuevos datos
        self.clear()

        # Agregar los datos a la tabla
        for row in data:
            self.add_item(f"{row[0]} - {row[1]}")

        cursor.close()
        conexion.close()

    def delete_file(self):
        selected_item = self.get_selected_item()
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

    def edit_file(self):
        pass