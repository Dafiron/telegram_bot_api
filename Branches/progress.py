from Components.aux_function import generate_pdf,upload_pdf_to_public_storage, send_message, change_state, fetch_codigos,is_data_changed
from Components.constants import POSSIBILITY, pdf_cache

def listenig(chat_id, user_message:str, id_user_telegram):
    user_message = user_message.lower()
    try:
        if user_message == "1" or user_message in POSSIBILITY[1]:
            
            call_data = fetch_codigos() #se extrae todos los productos
            is_changed=is_data_changed(call_data) # se verifica si hubo cambios en relacion a la ultima consulta
            if is_changed:
                pdf_path = generate_pdf(call_data) # genera un pdf con los datos
                url_public = upload_pdf_to_public_storage(pdf_path)  # se sube a aws
                pdf_cache ["data"] = call_data #se guarda el nuevo estado de productos
                pdf_cache ["url"] = url_public #se guarda la nueva url 
                send_message(chat_id, f"Descarga el archivo PDF aquí: {pdf_cache['url']}")
                change_state(id_user_telegram,1)
            else:
                pdf_url = "https://s3.us-east-2.amazonaws.com/test.bot.telegram/productos.pdf"
                send_message(chat_id, f"Descarga el archivo PDF aquí: {pdf_cache['url']}")
                change_state(id_user_telegram,1)

        elif user_message == "2"or user_message in POSSIBILITY[2]:
            menssage = (
                "Upss! Actualmente no estamos reciviendo pedidos por este medio,\n"
                "Por Favor comuniquese"
                "Al: +59 9 223 X XXXXXX\n"
                "De Lun a Vie de 09:00 hs a 17:00 hs \n"
                "y podremos resolver su pedido\n"
                "Si nuevamente nesecitas infromacion aqui estare."
            )
            send_message(chat_id,menssage)
            change_state(id_user_telegram,2)

        elif user_message == "3"or user_message in POSSIBILITY[3]:
            menssage=(
                "Para la consulta de pedidos adeudados nesecitamos tu direccion valida(de la siguiente forma: calle altura).\n"
                "Si nesecitas ayuda envia un '0'.\n"
                "Si deseas retornar al menu principal envia un '9'\n"
            )
            send_message(chat_id, menssage)
            change_state(id_user_telegram,3)

        elif user_message == "4" or user_message in POSSIBILITY[4]:
            menssage=(
                "Desde esta unidad automatica solo podemos orientarlo en los Reclamos.\n"
                "Estas se realizan por los siguientes medios: Telefono o Whatsapp.\n"
                "Al: +59 9 223 X XXXXXX\n"
                "Recuerde tener a mano los remitos (de preferencia en formato digital) asi como informacion personal.\n"
                "Si nuevamente nesecitas infromacion aqui estare."
            )
            send_message(chat_id,menssage)
            change_state(id_user_telegram,1)

        elif user_message == "5"or user_message in POSSIBILITY[5]:
            menssage=(
                "Desde esta unidad no podemos redireccionar su solicitud de forma automatica.\n"
                "La atencion al cliente personalizada se realiza por los siguientes medios: Telefono o Whatsapp.\n"
                "Al: +59 9 223 X XXXXXX\n"
                "De Lun a Vie de 09:00 hs a 17:00 hs \n"
                "Si nuevamente nesecitas infromacion aqui estare."
            )
            send_message(chat_id,menssage)
            change_state(id_user_telegram,1)
        
        else:
            send_message(chat_id, "Por favor, envía un mensaje con un valor valido.")
    except Exception as e:
        print(f"Error en el endpoint /telegram-webhook: {e}")
        return {"status": "error", "message": str(e)}, 200
