#Importacion Externa // External Import
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


#Importacion Interna // Internal Import
from Branches.start import opening
from Branches.progress import listenig
from Branches.ordes import searcher_debts
from Components.aux_function import which_state, change_state, send_message 

#variables de entorno
from Components.constants import check_environment_variables, list_env_var, is_connected
from dotenv import load_dotenv
import os

load_dotenv()
#acordarse de modificar los endpoint /dev para que solo se ejecuten en entorno de desarrollo

app = FastAPI(
    title= "Test_bot_telegram",
    version="0.1 BETA",
    description= "Api que gestiona bot en telegram",
    docs_url="/docs" if os.getenv("on_dev") == "Y" else None,
    redoc_url="/redoc" if os.getenv("on_dev") == "Y" else None,
    openapi_url="/openapi.json" if os.getenv("on_dev") == "Y" else None,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],  # Dominios permitidos (puedes usar "*" para permitir todos, aunque no es seguro en producción)
    allow_credentials=True,                  # Permitir credenciales como cookies
    allow_methods=["*"],                     # Métodos permitidos (GET, POST, etc.)
    allow_headers=["*"],                     # Encabezados permitidos
)

check_environment_variables(list_env_var)

is_connected()

@app.get("/")
async def root():
    return "Api para gestionar el bot de telegram"

# Endpoint para recibir mensajes de Telegram
@app.post("/telegram-webhook")
async def telegram_webhook(request: Request):
    """
    Endpoint que resive los mensaje del bot de Telegram.
    """
    try:
        # Obtener los datos del mensaje
        data = await request.json()

        # Extraer el chat_id
        chat_id = data["message"]["chat"]["id"]
        id_user_telegram = data["message"]["from"]["id"]
        state, first = which_state(id_user_telegram)

        # Verificar si el mensaje contiene texto
        if "text" in data["message"]:
            user_message = data["message"]["text"]
            # Mostrar el menú inicial si el usuario envía cualquier mensaje no reconocido

            if state == 1:
                opening(chat_id,first)
                change_state(chat_id,2)

            elif state == 2:
                listenig(chat_id,user_message,id_user_telegram)

            elif state == 3:
                searcher_debts(chat_id,user_message,id_user_telegram)

        elif "contact" in data["message"]:
            # Manejar mensajes de contacto
            contact = data["message"]["contact"]
            phone_number = contact.get("phone_number", "No disponible")
            first_name = contact.get("first_name", "No disponible")
            last_name = contact.get("last_name", "No disponible")
            send_message(chat_id, f"Gracias por compartir tu contacto, {first_name}!")

        else:
            # Mensaje no reconocido
            send_message(chat_id, "Por favor, envía un mensaje de texto o comparte un contacto.")

        return {"status": "ok"}

    except Exception as e:
        # Devolver una respuesta HTTP 200 OK para evitar que Telegram reenvíe la actualización
        return {"status": "error", "message": str(e)}, 200

