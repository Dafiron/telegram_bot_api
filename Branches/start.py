from Components.aux_function import send_message
import random

APERTURAS ={
    1: "Buenas, soy el asistente automatico de DiscoverIT, mi funcionalidad esencial, es servir de testeo de las distintas posibilidades en la implementacion de bot. \n",
    2: "Hola, soy el bot automatico de DiscoverIT, diseñado para probar las capasidades de esta tecnologia en tu empresa.\n",
    3: "Saludos, soy el asistente automatico de DiscoverIT, soy un bot, pensado para testear las posiblidades de esta tecnologia\n",
    4: "Buenas, soy el asistente automatico de DiscoverIT, diseñado para mostrar el alcanse de esta tecnologia. \n"
}


def opening(chat_id, first):
    if first:
        rand =random.choice(range(1,5))
        menu_text = (
            f"{APERTURAS[rand]}"
            "Te dejo la siguientes opcciones para que explores:\n"
            "1. Lista de productos\n"
            "2. Hacer un pedido\n"
            "3. Consultar mis pedidos adeudados\n"
            "4. Reclamos\n"
            "5. Nesecito comunicarme con un representante\n"
        )
        send_message(chat_id, menu_text)
    else:
        menu_text = (
            "Estas son las opcciones para que explores:\n"
            "1. Lista de productos\n"
            "2. Hacer un pedido\n"
            "3. Consultar mis pedidos adeudados\n"
            "4. Reclamos\n"
            "5. Nesecito comunicarme con un representante.\n"
        )
        send_message(chat_id, menu_text)
