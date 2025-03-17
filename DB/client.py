from dotenv import load_dotenv
import mysql.connector
from fastapi import HTTPException,status
import os

load_dotenv()

sql_pass = os.getenv("db_sql_password")
sql_user = os.getenv("db_sql_user")
sql_host = os.getenv("db_sql_host")
sql_port = os.getenv("db_sql_port")
sql_database =os.getenv("db_sql_database")

def get_sql_connection():
    try:
        config = {
            "host": sql_host,
            "port": int(sql_port),
            "database": sql_database,
            "user": sql_user,
            "password": sql_pass,
            "connect_timeout": 10,
            "use_pure": True  # Fuerza el uso del conector puro de Python
        }
        connection = mysql.connector.connect(**config)
        return connection
    except mysql.connector.errors.InterfaceError as ie:
        print(f"Error de interfaz al conectar a la base de datos: {ie}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error de interfaz al conectar a la base de datos: {ie}"
        )
    except mysql.connector.errors.DatabaseError as de:
        print(f"Error de base de datos al conectar: {de}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error de base de datos al conectar: {de}"
        )
    except Exception as e:
        print(f"Error inesperado al conectar a la base de datos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado al conectar a la base de datos: {e}"
        )