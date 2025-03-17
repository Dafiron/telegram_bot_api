from Components.constants import BASE_URL, user_state,DATABASE, AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID
from DB.client import get_sql_connection
import mysql.connector
import boto3


from reportlab.lib.pagesizes import letter,landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from Components.constants import pdf_cache
import requests

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, json=payload)
    return response.json()

def fetch_codigos():
    print("Ingreso a la funcion de busqueda de codigos...")
    try:
        with get_sql_connection() as connection:
            with connection.cursor() as cursor:
                query = f"""
                SELECT codigo, nombre, peso, precio_publico
                FROM {DATABASE}.codigos;
                """
                cursor.execute(query)
                print(f"consualta a BD {query}")
                result = cursor.fetchall()
                if result:
                    print(f"se registraron resultados: primera linea: {result[0]}")
                return result
    except mysql.connector.Error as e:
        print(f"Error al consultar la tabla codigos: {e}")
        raise 

def generate_pdf(data):
    try:
        # Ruta del archivo PDF
        pdf_path = "productos.pdf"

        # Crear el documento PDF en formato horizontal
        doc = SimpleDocTemplate(pdf_path, pagesize=landscape(letter))

        # Encabezados de la tabla
        headers = ["Código", "Nombre", "Peso (kg)", "Precio Público"]

        # Agregar los encabezados y los datos
        table_data = [headers] + [[str(row[0]), row[1], str(row[2]), str(row[3])] for row in data]

        # Crear la tabla
        table = Table(table_data)

        # Estilo de la tabla
        style = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ])

        table.setStyle(style)

        # Construir el PDF
        elements = [table]
        doc.build(elements)

        print(f"PDF generado: {pdf_path}")
        return pdf_path

    except Exception as e:
        print(f"Error al generar el PDF: {e}")
        raise


def which_state(id_telegram:int)-> int:
    """
    Funcion que consulta estado del ususario, retona el estado y si esta la primera interacion.
    """
    first= False
    if id_telegram not in user_state:
        user_state[id_telegram] = 1
        first=True
    
    return user_state[id_telegram], first

def change_state(id_telegram:int,new_state:int):
    """
    Funcion que transforma el estado de un ususario.
    """
    if id_telegram not in user_state:
        print(f"imposible realizar el cambio de estado el id no se encuentra registrado")
    else:
        user_state[id_telegram] = new_state


def upload_pdf_to_public_storage(pdf_path):
    # Crear el cliente S3 con las credenciales
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name="us-east-2"  # Asegúrate de usar la región correcta
    )
    bucket_name = "test.bot.telegram"
    object_name = "productos.pdf"

    # Subir el archivo al bucket
    print("subiendo archivo?")
    s3.upload_file(pdf_path, bucket_name, object_name)
    print("liena de subida ejecutada...")

    # Devolver la URL pública
    return f"https://{bucket_name}.s3.us-east-2.amazonaws.com/{object_name}"

def is_data_changed(new_data):
    """
    Compara los datos actuales con los datos almacenados en el diccionario.
    Retorna True si los datos han cambiado, False si son iguales.
    """
    print("comparacion de is_data_changed")
    if pdf_cache["data"] is None:
        return True  # Si no hay datos previos, asumimos que los datos han cambiado
    return tuple(map(tuple, pdf_cache["data"])) != tuple(map(tuple, new_data))