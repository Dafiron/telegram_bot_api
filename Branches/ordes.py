from DB.client import get_sql_connection
import mysql.connector
from Components.constants import DATABASE
from Components.aux_function import send_message, change_state

def searcher_debts(chat_id:int,user_message:str, id_user_telegram):
    """
    Funcion que busca los pedidos adeudados de un cliente por direccion.
    """
    user_message = user_message.lower()
    try:
        with get_sql_connection() as connection:
            with connection.cursor() as cursor:
                # Solicito id_cliente para particularizar direccion. 
                query=f"""
                SELECT id_cliente
                FROM {DATABASE}.clientes
                WHERE direccion = %s;
                """
                cursor.execute(query,(user_message,))
                result = cursor.fetchall()
                if len(result) > 1:
                    send_message(chat_id, "Se encontraron múltiples clientes con la misma dirección. Por favor, contacta a un representante para resolver este caso.")
                    change_state(id_user_telegram,1)
                    return
                if not result:
                    menssage = (
                        "No hemos podido relacionar la direccion provista con un cliente activo.\n"
                        "Intenta nuevamente, con todos los caracteres en minuscula, sin espacios previos.\n"
                        "De la siguiente forma: calle altura\n"
                        "ejemplo :la madrid 157814\n"
                        "Si continuas con incombenientes comunicate via whatsapp al +54 9 223 X XXXXXX\n"
                    )
                    send_message(chat_id,menssage)
                else:
                    # solicita todos los pedidos adeudados.
                    id_cliente=[r[0]for r in result]
                    query2=f"""
                    SELECT id_pedido, id_hoja, id_medios
                    FROM {DATABASE}.pedidos
                    WHERE id_cliente_p = %s AND pago = 0;
                    """
                    cursor.execute(query2,(id_cliente))
                    result2 = cursor.fetchall()
                    if not result2:
                        menssage = (
                            "No hemos podido encontrar los pedidos adeudados,\n"
                            "Si crees que se trata de un error comuniquese via whatsapp al +54 9 223 X XXXXXX,\n"
                            "Nuestros representantes le podran asistir en su inquietud\n"
                        )
                        send_message(chat_id,menssage)
                        change_state(id_user_telegram,1) 
                    else:
                        pedidos_list = [p[0] for p in result2] 
                        # Se solicita cuando fueron entregados estos pedidos.
                        hojas = [h[1] for h in result2]
                        placeholders = ', '.join(['%s'] * len(hojas))
                        query4 = f"""
                        SELECT 
                            id_hoja,
                            fecha
                        FROM {DATABASE}.hoja
                        WHERE id_hoja IN ({placeholders})
                        """
                        print(f"Consulta generada para hoja: {query4}")  # Debugging
                        print(f"Valores para IN de hoja: {hojas}") 
                        cursor.execute(query4, hojas)
                        result4 = cursor.fetchall()
                        if not result4:
                            menssage = (
                                "Ocurrio un error en la carga de datos\n"
                                "Por Favor comuniquese via whatsapp al +54 9 223 X XXXXXX,\n"
                                "Nuestros representantes le podran asistir\n"
                            )
                            send_message(chat_id,menssage)
                            change_state(id_user_telegram,1)
                        else:
                            #se solicita si existieron pagos anteriores.
                            hoja_dict = {}
                            for h in result4:
                                for p in result2:
                                    if p[1] == h[0]:
                                        hoja_dict[p[0]]= str(h[1])
                            placeholders = ', '.join(['%s'] * len(pedidos_list))
                            query5 = f"""
                            SELECT 
                                id_pedido,
                                monto_pagar,
                                cant_pago,
                                fecha
                            FROM {DATABASE}.pagos
                            WHERE id_pedido IN ({placeholders})
                            """
                            print(f"Consulta generada: {query5}")  # Debugging
                            print(f"Valores para IN de hoja: {pedidos_list}") 
                            cursor.execute(query5, pedidos_list)
                            result5 = cursor.fetchall()
                            print(f" valores de respuesta para consulta 5 : {result5}")
                            #inicia el ordenamiento de datos para debolucion.
                            pagos={}
                            if result5:
                                for p in result5:
                                    if not p[0] in pagos:
                                        pagos[p[0]]={"monto_pagar":p[1], "pagos_realizados":[]}
                                    pagos[p[0]]["pagos_realizados"].append((p[2],str(p[3])))
                            print(f"pagos realizados: {pagos}")
                            pedi_str = ""
                            print(f"resultado 2 :{result2}")
                            print(f"hoja: {hoja_dict}")
                            for p in result2:
                                pedi_str += f"Pedido entregado el : {hoja_dict[p[0]]}\n"
                                print(f"construllendo mensaje: {pedi_str}")
                                if pagos[p[0]]["pagos_realizados"]:
                                    pedi_str += f"Total: {pagos[p[0]]['monto_pagar']}\n"
                                    pedi_str += f"Pagos registrados:\n"
                                    for pr in pagos[p[0]]["pagos_realizados"]:
                                        pedi_str += f"fecha: {pr[1]} monto: {pr[0]}\n"
                                elif  pagos[p[0]]["monto_pagar"]:
                                    pedi_str += f"Total: {pagos[p[0]]['monto_pagar']}\n"
                                    pedi_str += f"No se encontraron pagos realizados\n"
                                else:
                                    send_message(chat_id, "Ocurrió un error al procesar tu solicitud. Por favor, intenta nuevamente más tarde.")
                            print(f"preparando mensaje: {pedi_str}")
                            menssage=(
                                f"Para el cliente con id: {id_cliente} con direccion en: {user_message}\n"
                                f"Se registran un total de {len(pedidos_list)} pedio/s\n"
                            )
                            menssage += pedi_str
                            send_message(chat_id,menssage)
                            change_state(id_user_telegram,1)
    except mysql.connector.Error as e:
        print(f"Error en la consulta a la base de datos: {e}")
        send_message(chat_id, "Ocurrió un error al procesar tu solicitud. Por favor, intenta nuevamente más tarde.")
    except Exception as e:
        # Imprimir el error en la terminal
        print(f"Error en el endpoint /telegram-webhook: {e}")
        # Devolver una respuesta HTTP 200 OK para evitar que Telegram reenvíe la actualización
        return {"status": "error", "message": str(e)}, 200

