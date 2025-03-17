from dotenv import load_dotenv
from DB.client import get_sql_connection
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

states={
    1:"start",
    2:"progress",
    3:"orders",
    4:"debts"
}

POSSIBILITY ={
    1:[1,"lista de productos","1. lista de productos", "1. listas de productos"],
    2:[2,"2. hacer un pedido","hacer un pedido", "hacer pedido"],
    3:[3, "3. consultar mis pedidos adeudados","consultar mis pedidos adeudados"],
    4:[4,"4. reclamos","reclamos","reclamo"],
    5:[5,"nesecito comunicarme con un representante.", "representante","nesecito comunicarme con un representante","5. nesecito comunicarme con un representante"]
}


user_state ={} #id del usuario en telegram : un estado en codificacion numerica

list_env_var=["db_sql_database","db_sql_host", "db_sql_user","on_dev","db_sql_password","db_sql_port", "TELEGRAM_TOKEN","AWS_SECRET_ACCESS_KEY","AWS_ACCESS_KEY_ID"]

DATABASE = os.getenv("db_sql_database")

AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID")

AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")

def check_environment_variables(required_vars: list):
    """
    Verifica si las variables de entorno requeridas están definidas.
    :param required_vars: Lista de nombres de las variables de entorno requeridas.
    """
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise EnvironmentError(
            f"Faltan las siguientes variables de entorno: {', '.join(missing_vars)}"
        )
    print("*---Todas las variables de entorno están definidas correctamente.---*")

def is_connected():
    try:
        connection = get_sql_connection()
        print("Conexión exitosa a la base de datos.")
        connection.close()
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")


# Diccionario para almacenar los datos y la URL del PDF
pdf_cache = {
    "data": None,  # Datos más recientes de los productos
    "url": "https://s3.us-east-2.amazonaws.com/test.bot.telegram/productos.pdf"    # URL pública del PDF más reciente
}