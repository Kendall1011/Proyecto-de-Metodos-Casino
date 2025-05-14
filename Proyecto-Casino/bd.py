# bd.py

import pyodbc

# Conexión única a la base de datos
def conectar():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-TEIIL4V\\SQLSERVERDEV2022;'
        'DATABASE=RuletaDBMetodos;'
        'UID=SaysaProject;'
        'PWD=leogon10'
    )


def guardar_resultado(numero, color):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Giros (Numero, Color) VALUES (?, ?)", (numero, color))
        conn.commit()
        conn.close()
        print(f"📌 Guardado: Número {numero}, Color {color}")
    except Exception as e:
        print(f"❌ Error al guardar en BD: {e}")
