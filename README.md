# Índice

**Nota**: Este documento está disponible en español (ES) e inglés (EN). Usa el índice para navegar entre las versiones.

## ES (Español)

1. [Descripción](#descripción)
2. [Tecnologías](#tecnologías)
3. [Bases de Datos](#bases-de-datos)
   - 3.1. [Esquema](#esquema)
   - 3.2. [Tabla `codigos`](#tabla-codigos)
   - 3.3. [Tabla `clientes`](#tabla-clientes)
   - 3.4. [Tabla `pedidos`](#tabla-pedidos)
   - 3.5. [Tabla `hoja`](#tabla-hoja)
   - 3.6. [Tabla `pagos`](#tabla-pagos)
4. [Documentación Específica](#documentación-específica)
5. [Endpoints](#endpoints)
   - 5.1. [`/telegram-webhook` (POST)](#telegram-webhook-post)
6. [Posibles Estados](#posibles-estados)
7. [Posibles Saludos](#posibles-saludos)
8. [Estados](#estados)
   - 8.1. [Start](#start)
   - 8.2. [Progress](#progress)
      - 8.2.1. [Lista de Productos](#1-lista-de-productos)
      - 8.2.2. [Hacer un Pedido](#2-hacer-un-pedido)
      - 8.2.3. [Consultar Mis Pedidos Adeudados](#3-Consultar-mis-pedidos-adeudados)
      - 8.2.4. [Reclamos](#4-Reclamos)
      - 8.2.5. [Necesito Comunicarme con un Representante](#5-nesecito-comunicarme-con-un-representante)
   - 8.3. [Orders](#orders)
   - 8.4. [Debts](#debts)
9. [Variables de Entorno](#variables-de-entorno)
10. [Ejecución](#ejecución)
    - 10.1. [Entorno Local](#entorno-local)
    - 10.2. [Bot](#bot)
    - 10.3. [Comandos por Path](#comandos-por-path)
    - 10.4. [Bucle Infinito](#bucle-infinito)
11. [Archivo Procfile](#archivo-procfile)
12. [Licencias](#licencias)

---

## EN (English)

1. [Description](#description)
2. [Technologies](#technologies)
3. [Databases](#databases)
   - 3.1. [Schema](#schema)
   - 3.2. [Table `codigos`](#table-codigos)
   - 3.3. [Table `clientes`](#table-clientes)
   - 3.4. [Table `pedidos`](#table-pedidos)
   - 3.5. [Table `hoja`](#table-hoja)
   - 3.6. [Table `pagos`](#table-pagos)
4. [Specific Documentation](#specific-documentation)
5. [Endpoints](#endpoints)
   - 5.1. [`/telegram-webhook` (POST)](#telegram-webhook-post)
6. [Possible States](#possible-states)
7. [Possible Greetings](#possible-greetings)
8. [States](#states)
   - 8.1. [Start](#start)
   - 8.2. [Progress](#progress)
      - 8.2.1. [Product List](#1-product-list)
      - 8.2.2. [Place an Order](#2-place-an-order)
      - 8.2.3. [Check My Outstanding Orders](#3-check-my-outstanding-orders)
      - 8.2.4. [Claims](#4-claims)
      - 8.2.5. [I Need to Contact a Representative](#5-i-need-to-contact-a-representative)
   - 8.3. [Orders](#orders)
   - 8.4. [Debts](#debts)
9. [Environment Variables](#environment-variables)
10. [Execution](#execution)
    - 10.1. [Local Environment](#local-environment)
    - 10.2. [Bot](#bot)
    - 10.3. [Commands by Path](#commands-by-path)
    - 10.4. [Infinite Loop](#infinite-loop)
11. [Procfile](#procfile)
12. [Licenses](#licenses)


# ES
---
## Descripción

API para gestionar un bot en telegram , que contesta preguntas frecuentes , asi como consultar estados de cuenta, contactos de la empresa, y lista de precios.

Para esto se trabajo en el lenguaje Python, con el framework Fastapi, se contaba con una base de datos MySQL construida para otro proyecto que se utilizo como datos para el testeo, y un servicio de almacenamiento de archivos en este caso PDF.

## Tecnologías

- Backend: FastAPI (Python)
- Base de Datos: MySQL
- Almacenamiento de Imágenes: AWS S3

## Bases de Datos

Se contaba con una base de datos de un proyecto anterior, por eso comparto las partes pertinentes, este fue confeccionado en MySQL.

Para el almacenaje de las imagenes y su despliegue se utilizo los servicios de AWS S3, debido a su popularidad y sobre todo a su costo (gratis).

#### SCHEMA

|Simbolo | exprecion                              |
|--------|----------------------------------------|
| (*)    | dato no relebante para las operaciones |
| PK     | Primary Key                            |
| NN     | Not Null                               |
| AI     | Auto Increment                         |
| UQ     | Unique                                 |
| FK     | Foreign Key                            |


#### Tabla `codigos`


| Columna        | Tipo         | Descripción / Description             |
|----------------|--------------|---------------------------------------|
| codigo         | INT          | PK, NN, AI                            |
| nombre         | VARCHAR(100) | NN                                    |
| descripcion    | VARCHAR(100) |(default: NULL)                        |
| peso           | INT          | NN                                    |
| precio         | INT          |(default: '0')                         |
| precio_publico | INT          |(default: '0')                         |



#### Tabla `clientes`


| Columna       | Tipo         | Descripción / Description             |
|---------------|--------------|---------------------------------------|
| id_cliente    | INT          | PK, NN, AI                            |
| saldo         | INT          | NN, (representa el saldo del cliente) |
| direccion     | VARCHAR(80)  | NN, UQ                                |


#### Tabla `pedidos`

| Columna     | Tipo         | Descripción / Description                                                |
|-------------|--------------|--------------------------------------------------------------------------|
| id_pedido   | INT          | PK, NN, AI, UQ                                                           |
| id_hoja     | INT          | FK (hoja.id_hoja)(default: NULL)                                         |
|id_cliente_p | INT          | NN FK (clientes.id_cliente)                                              |
| id_medios   | INT          | NN FK (pagos_medios.id_medios) (representa el medio de pago)(*)          |
| pago        | INT          | NN (representa si dicho pedido fue pagado en su totalidad o no)           |
| visitado    | INT          | (default: '0')(refleja si el cliente fue visitado por este pedido)(*)    |
| venta       | INT          | (default: '0')(representa si este pedido fue convertido en venta) (*)    |


#### Tabla `hoja` 


| Columna     | Tipo         | Descripción / Description               |
|-------------|--------------|-----------------------------------------|
| id_hoja     | INT          | PK, NN, AI                              |
| fecha       | DATE         | FK (products.id_product)                |
| id_user_fk  | INT          | NN FK (users.id_user)(*)                |
| id_vehiculo | INT          | NN FK (vehiculo.id_vehiculo)(*)         |

(tabla utilizada para organizar el dia de trabajo lo que nos otorga un dia al al que se adjunto el pedido)

#### Tabla `pagos` 


| Columna     | Tipo         | Descripción / Description               |
|-------------|--------------|-----------------------------------------|
| id_dato     | INT          | PK, NN, AI, UQ                          |
| id_pedido   | INT          | FK (pedidos.id_pedido) (default: NULL)  |
| monto_pagar | INT          | NN (monto a total que resta pagar)      |
| cant_pago   | INT          | NN (monto pagado en esta oportunidad)   |
| fecha       | DATE         | NN (cuando se realizo el mismo)         |
| pago        | INT          | NN (si esta pago o no el pedido)        |


### Documentación Específica

Fastapi en su uso y coperacion con la tecnologia de Swagger UI nos facilita una documentación resumida y ordenada en {url_de_despliegue}/docs
o la opccion de ReDoc {url_de_despliegue}/redoc

## Endpoint

### **/telegram-webhook** (POST)
- **Descripción:** Endpoint que resive los mensaje del bot de Telegram.
- **Responses:**
    - **200 OK:**

- **Errores:** {"status": "error", "message": error espesifico}
Todos los errores tambien dan 200 OK, y se mustra por print(), para evitar el bucle infinito del error.


## Posibles Estados

|numero  | Estados      |
|--------|--------------|
| 1      | start        |
| 2      | progress     |
| 3      | orders       |
| 4      | debts        |


## Posibles de Saludos

|posibilidades  | texto                                                                                                                    |
|---------------|--------------------------------------------------------------------------------------------------------------------------|
|      1        | Buenas, soy el asistente automatico de DiscoverIT, mi funcionalidad esencial, es servir de testeo de las distintas...    |
|      2        | Hola, soy el bot automatico de DiscoverIT, diseñado para probar las capasidades de esta tecnologia en tu empresa.        |  
|      3        | Saludos, soy el asistente automatico de DiscoverIT, soy un bot, pensado para testear las posiblidades de esta tecnologia |
|      4        | Buenas, soy el asistente automatico de DiscoverIT, diseñado para mostrar el alcanse de esta tecnologia                   |


### Inicio

- Se detecata si el mensaje es el primero del usuario.

- Se establese si es mensaje es valido (ya que solo se admiten los mensajes de texto o contacto)

## Estados

### Start

Se ejecuta una apertura con un saludo elegido al azar de entre 4 posibles de saludos, simandole las opcciones de navegacion para el usuario:


>{posibilidad de saludos}                           
>Te dejo la siguientes opcciones para que explores: 
>1. Lista de productos                              
>2. Hacer un pedido                                 
>3. Consultar mis pedidos adeudados                 
>4. Reclamos                                        
>5. Nesecito comunicarme con un representante       


Cambiando el estado a su condicion 2 (progress)

### progress

En este estado se presenta la getion inicial o total de las 5 posibilidades de navegacion del usuario.

#### 1. Lista de productos

Se capturan todos los productos desde la base de datos y se comparan con los datos previamente almacenados en el servidor. Si ambos conjuntos de datos son idénticos, el proceso continúa sin cambios. De lo contrario:

- Se genera un archivo PDF con los datos extraídos de la base de datos.
- El archivo PDF se sube al servicio de almacenamiento en la nube AWS S3.
- Se envía el siguiente mensaje al usuario:


>Descarga el archivo PDF aquí:                             
>https://{Region}.amazonaws.com/{Bucket-Name}/productos.pdf

Finalmente, el estado del usuario cambia a **1 (start)**.

##### Ejemplo de PDF generado:
Puedes descargar un ejemplo del archivo PDF generado haciendo clic en el siguiente enlace:

[Descargar PDF](productos.pdf)

#### 2. Hacer un pedido 

Se envia un error por incapasidad actual de resolver la consulta, temporalmente:


>Upss! Actualmente no estamos reciviendo pedidos por este medio,
>Por Favor comuniquese                                          
>Al: +59 9 223 X XXXXXX                                         
>De Lun a Vie de 09:00 hs a 17:00 hs                            
>y podremos resolver su pedido                                  
>Si nuevamente nesecitas infromacion aqui estare.               


Se mantiene el estado en su posicion 2 (progress)

#### 3. Consultar mis pedidos adeudados

Se envia un mensaje solicitando datos para proseguir con la consulta:


>Para la consulta de pedidos adeudados nesecitamos tu direccion valida(de la siguiente forma: calle altura).  
>Por Favor comuniquese                                                                                        
>Al: +59 9 223 X XXXXXX                                                                                       
>De Lun a Vie de 09:00 hs a 17:00 hs                                                                          
>y podremos resolver su pedido                                                                                
>Si nuevamente nesecitas infromacion aqui estare.                                                             


Cambiando el estado a 3 (orders)


#### 4. Reclamos

Se envia un mensaje:


>Desde esta unidad automatica solo podemos orientarlo en los Reclamos.                                        
>Estas se realizan por los siguientes medios: Telefono o Whatsapp.                                            
>Al: +59 9 223 X XXXXXX                                                                                       
>De Lun a Vie de 09:00 hs a 17:00 hs                                                                          
>Recuerde tener a mano los remitos (de preferencia en formato digital) asi como informacion personal.         
>Si nuevamente nesecitas infromacion aqui estare.                                                             



Cambiando el estado del usuario a 1 (start)

#### 5. Nesecito comunicarme con un representante


Mensaje de respuesta:


>Desde esta unidad no podemos redireccionar su solicitud de forma automatica.                                  
>Estas se realizan por los siguientes medios: Telefono o Whatsapp.                                            
>Al: +59 9 223 X XXXXXX                                                                                       
>De Lun a Vie de 09:00 hs a 17:00 hs                                                                          
>Si nuevamente nesecitas infromacion aqui estare.                                                             


Cambiando el estado del usuario a 1 (start)

#### Error en el Mensaje

Ante la incapasidad de lectura del mensaje ya sea por no contener textos, o no sea valido el contenido del mensaje:

Enviando:


>Por favor, envía un mensaje con un valor valido.  |


Manteniendo el estado.

### orders

- Atravez de la direcion proporcionada se individualiza el el cliente.

ante la incapasidad de individualizarlo envia el mensaje (cambiando su estado a 1 (start)):


>Se encontraron múltiples clientes con la misma dirección. Por favor, contacta a un representante para resolver este caso.  
>Al: +59 9 223 X XXXXXX                                                                                                     
>De Lun a Vie de 09:00 hs a 17:00 hs                                                                                        



Si no se obtuvo resultado en la consualta a base de datos ( manteniendo estado ):


>No hemos podido relacionar la direccion provista con un cliente activo.                                                    
>Intenta nuevamente, con todos los caracteres en minuscula, sin espacios previos.                                           
>De la siguiente forma: calle altura                                                                                        
>Si continuas con incombenientes comunicate via whatsapp al +54 9 223 X XXXXXX                                              



- Se prosede a consultar por los pedidos que no esten retulados como pago *consultar tabla: pedidos.

De no encontrarse pedidos adeudados se retorna el siguiente mesnaje (retornando al estado 1 (start)):


>No hemos podido encontrar los pedidos adeudados,                                      
>Si crees que se trata de un error comuniquese via whatsapp al +54 9 223 X XXXXXX,     
>Nuestros representantes le podran asistir en su inquietud                             


- Luego se solicitan los a traves de vincular los pedidos a la hoja de trabajo que fue asignada para poder particularizar la fecha en que se realizo cada uno de los pedidos.

si no se encontrase habia una inconsistencia en el almacenaje de los datos lo que llevaria a contestar el siguiente mensaje (cambiando el estado a 1 (start)):


>Ocurrio un error en la carga de datos                         
>Por Favor comuniquese via whatsapp al +54 9 223 X XXXXXX,     
>Nuestros representantes le podran asistir                     


- Se consultan los pagos reaizados por el cliente para cada uno de los pedidos; se esta en condiciones de emitir un mensaje con la informacion solicitada por el cliente.

    ```r

                        |---------------------------------------------------------------------------------|
                        |Para el cliente con id: {id cliente} con direccion en: {direccion proporcianada} |
                        |Se registran un total de {cantidad de pedidos} pedio/s                           |
                        |---------------------------------------------------------------------------------|

                        +                                  o                         +

    |--------------------------------------------------|               |----------------------------------------------------|
    |Pedido entregado el : {fecha del primer pedido}   |               |Pedido entregado el : {fecha del primer pedido}     |
    |Total: {valor total del pedido}                   |               |Total: {valor total del pedido}                     |
    |Pagos registrados:                                |               |No se encontraron pagos realizados                  |
    |fecha: {fecha del pago} monto: {cantidad pagada}  |               |----------------------------------------------------|
    |--------------------------------------------------|               

El mensaje se extendera en funcion de la cantaidad de pedidos y el estado del mismo.

Ante un error inesperado en el proseso final envia menaje:


>Ocurrió un error al procesar tu solicitud. Por favor, intenta nuevamente más tarde.  


### debts

Esta en desarroyo catualmente no posee funcionalidades, en el futuro se podra hacer un pedido por este medio.


### Variables de Entorno
Crea un archivo `.env` con:
    ```env

    TELEGRAM_TOKEN = "75678644:AAGNJrjjlj1w6PZjhG0AB9qmnjfkjrtyeas" (EJEMPLO)

    db_sql_database={NOMBRE_DE_LA_DATABASE}
    db_sql_host={HOST}
    db_sql_port={PUERTO}
    db_sql_password={CONTRASEÑA}
    db_sql_user={USUARIO}

    on_dev="Y" (O "N" EN CASO DE ESTAR EN PRODUCCION)

    AWS_ACCESS_KEY_ID ="HGTGTYSTYHJJDMNCVB" (EJEMPLO)
    AWS_SECRET_ACCESS_KEY="FEGUHIFEGUFAGMdfiufgJFDBFG564/AGFD" (EJEMPLO)


### Ejecucion

#### Entorno Local

1. Se recomienda ejecutar el proyecto en un entorno virtual para evitar conflictos con otras dependencias del sistema.

Si no tienes un entorno virtual configurado, puedes crearlo y activarlo con los siguientes comandos:
Crear un entorno virtual (si no lo tienes)
    python -m venv venv

Activar el entorno virtual
En Windows:
    venv\Scripts\activate

En Linux/Mac:
    source venv/bin/activate

elemplo en termial:
{ubicado en raiz del proyecto}>python -m venv venv
{ubicado en raiz del proyecto}>venv\Scripts\activate
(venv) {ubicado en raiz del proyecto}>

2. Instalación de dependencias:
    pip install -r requirements.txt

3. Inicio del servidor

comando de inicio del servidor:

{ubicado en raiz del proyecto}> uvicorn main:app --host 0.0.0.0 --port 8000 --reload


El archivo main.py contiene dos funciones importantes que verifican el entorno antes de iniciar el servidor:

4. Verificación del entorno
check_environment_variables()
    verifica que todas las variables de entorno esten correctamente definidas:
        - respuesta positiva: *---Todas las variables de entorno están definidas correctamente.---*
        - respuesta negativa: Faltan las siguientes variables de entorno: XXX, ZZZ, YYY

5. Verifica la conexión a la base de datos
is_connected()
    verifica la conexion a base de datos (en este caso mysql) 
        - respuesta positiva: Conexión exitosa a la base de datos
        - respuesta negativa: Error al conectar a la base de datos:{error espesifico} 


6. Ejemplo de salida en la terminal
ejemplo de vision en terminal:
INFO:     Will watch for changes in these directories: ['{ubicado en raiz del proyecto}']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [14632] using WatchFiles
*---Todas las variables de entorno están definidas correctamente.---* 
Conexión exitosa a la base de datos.
INFO:     Started server process [14040]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

Una vez que el servidor esté en funcionamiento, puedes acceder a la API en tu navegador o mediante herramientas como curl o Postman o Thunder Client:

URL base: http://localhost:8000

y si la variable de entorno 'on_dev' == "Y":

Documentación interactiva (Swagger UI): http://localhost:8000/docs 

Documentación alternativa (ReDoc): http://localhost:8000/redoc

De lo contrario, es decir: 'on_dev' != "Y"

no sera visible; esto es espacialmente util para el despliegue del proyecto.

7. Cierre

Para cerrar el servidor: presione CTRL+C

y el entorno virtual: en la terminal que este sindo ejecutado: (venv) {ubicado en raiz del proyecto}> deactivate

#### Bot

Utiliza BotFather para dar de alta un bot y que este proporciene un TELEGRAM_TOKEN

busca BotFather y sigue las instrucciones.


#### Comandos por Path


Usa el siguiente comando para configurar el Webhook de Telegram:

curl -F "url=https://{TU_DOMINIO}/telegram-webhook" https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook

- Reemplaza {TU_DOMINIO} con la URL pública de tu servidor (por ejemplo, https://miapi.com).
- Reemplaza {TELEGRAM_TOKEN} con el token que obtuviste de BotFather.

Para verificar que el Webhook está configurado correctamente, usa este comando:

curl https://api.telegram.org/bot{TELEGRAM_TOKEN}/getWebhookInfo

Esto te mostrará información sobre el estado del Webhook.




#### Bucle infinito

Durante el desarrollo, puede ocurrir un bucle infinito si Telegram no recibe una respuesta HTTP 200 OK después de enviar una actualización a tu servidor. Esto hace que Telegram reenvíe continuamente la misma actualización, causando un ciclo repetitivo.

para localizar la id del mensaje problematico o ver la lista de mensaje que todabia no han sido correcatamente prosesados puedes usar:

curl https://api.telegram.org/bot<TELEGRAM_TOKEN>/getUpdates

- Reemplaza <TELEGRAM_TOKEN> con el token de tu bot (el que obtuviste de BotFather).

retornando algo similar a esto:
    ```r
    {
        "ok": true,
        "result": [
            {
                "update_id": 123456789,
                "message": {
                    "message_id": 1,
                    "from": {
                        "id": 987654321,
                        "is_bot": false,
                        "first_name": "Usuario",
                        "username": "usuario_prueba",
                        "language_code": "es"
                    },
                    "chat": {
                        "id": 987654321,
                        "first_name": "Usuario",
                        "username": "usuario_prueba",
                        "type": "private"
                    },
                    "date": 1698765432,
                    "text": "Hola, soy un mensaje pendiente."
                }
            }
        ]
    }

Comando de path para ignorar mensajes problemáticos:

    Durante el desarrollo, si ya estás atrapado en un bucle infinito, puedes usar un comando de path para ignorar los mensajes duplicados y continuar con el siguiente mensaje enviado por Telegram.

    curl -X POST https://api.telegram.org/bot<TELEGRAM_TOKEN>/getUpdates -d '{"offset": <UPDATE_ID>}'

    - Reemplaza <TELEGRAM_TOKEN> con tu token de bot.
    - Reemplaza <UPDATE_ID> con el ID del último mensaje duplicado. Esto hará que Telegram ignore todos los mensajes con un ID menor o igual al especificado.


##### EJEMPLO:
Supongamos que recibes el siguiente JSON al ejecutar getUpdates:
    ```r
    {
        "ok": true,
        "result": [
            {
                "update_id": 123456789,
                "message": {
                    "message_id": 1,
                    "from": { ... },
                    "chat": { ... },
                    "date": 1698765432,
                    "text": "Mensaje duplicado"
                }
            },
            {
                "update_id": 123456790,
                "message": {
                    "message_id": 2,
                    "from": { ... },
                    "chat": { ... },
                    "date": 1698765433,
                    "text": "Otro mensaje duplicado"
                }
            }
        ]
    }

Para ignorar estos mensajes duplicados, usa el siguiente comando:

curl -X POST https://api.telegram.org/bot<TELEGRAM_TOKEN>/getUpdates -d '{"offset": 123456791}'

Esto hará que Telegram ignore todos los mensajes con update_id menor o igual a 123456790.



#### Archivo Procfile
web: uvicorn main:app --host 0.0.0.0 --port $PORT

### Licencias
- **Este proyecto**: MIT License (ver [LICENSE](LICENSE)).
- **Dependencias**: Ver [LICENSES.md](LICENSES.md).
- **Nota**: `mysql-connector-python` está bajo GPL. Si usas este código en producción, considera migrar a `pymysql` (MIT License).




# EN
---


## Description

API for managing a Telegram bot that answers frequently asked questions, as well as checking account statements, company contacts, and price lists.

This work was done in Python, using the FastAPI framework. There was a MySQL database built for another project that was used as testing data, and a file storage service, in this case PDF.

## Technologies

- Backend: FastAPI (Python)
- Database: MySQL
- Image Storage: AWS S3

## Databases

There was a database from a previous project, so I'm sharing the relevant parts. This one was built in MySQL.

For image storage and deployment, AWS S3 services were used, due to its popularity and, above all, its cost (free).

#### SCHEMA

|Symbol | expression                     |
|-------|--------------------------------|
|  (*)  | data not relevant to operations|
|  PK   | Primary Key                    |
|  NN   | Not Null                       |
|  AI   | Auto Increment                 |
|  UQ   | Unique                         |
|  FK   | Foreign Key                    |


#### Table `codigos`


| Columna        | Tipo         | Descripción / Description             |
|----------------|--------------|---------------------------------------|
| codigo         | INT          | PK, NN, AI                            |
| nombre         | VARCHAR(100) | NN                                    |
| descripcion    | VARCHAR(100) |(default: NULL)                        |
| peso           | INT          | NN                                    |
| precio         | INT          |(default: '0')                         |
| precio_publico | INT          |(default: '0')                         |



#### Table `clientes`


| Columna       | Tipo         | Descripción / Description               |
|---------------|--------------|-----------------------------------------|
| id_cliente    | INT          | PK, NN, AI                              |
| saldo         | INT          | NN, (represents the customer's balance) |
| direccion     | VARCHAR(80)  | NN, UQ                                  |


#### Table  `pedidos`

| Columna     | Tipo  | Descripción / Description                                                   |
|-------------|-------|-----------------------------------------------------------------------------|
| id_pedido   | INT   | PK, NN, AI, UQ                                                              |
| id_hoja     | INT   | FK (hoja.id_hoja)(default: NULL)                                            |
|id_cliente_p | INT   | NN FK (clientes.id_cliente)                                                 |
| id_medios   | INT   | NN FK (pagos_medios.id_medios) (represents the means of payment)(*)         |
| pago        | INT   | NN (represents whether the order was paid in full or not)                   |
| visitado    | INT   | (default: '0')(reflects whether the customer was visited by this order)(*)  |
| venta       | INT   | (default: '0')(represents whether this order was converted into a sale) (*) |


#### Table `hoja` 


| Columna     | Tipo         | Descripción / Description               |
|-------------|--------------|-----------------------------------------|
| id_hoja     | INT          | PK, NN, AI                              |
| fecha       | DATE         | FK (products.id_product)                |
| id_user_fk  | INT          | NN FK (users.id_user)(*)                |
| id_vehiculo | INT          | NN FK (vehiculo.id_vehiculo)(*)         |

(table used to organize the work day which gives us a day to which the order is attached)

#### Table `pagos` 


| Columna     | Tipo         | Descripción / Description               |
|-------------|--------------|-----------------------------------------|
| id_dato     | INT          | PK, NN, AI, UQ                          |
| id_pedido   | INT          | FK (pedidos.id_pedido) (default: NULL)  |
| monto_pagar | INT          | NN (total amount remaining to be paid)  |
| cant_pago   | INT          | NN (amount paid on this occasion)       |
| fecha       | DATE         | NN (when it was done)                   |
| pago        | INT          | NN (whether the order is paid or not)   |


### Specific Documentation

Fastapi, in its use and cooperation with Swagger UI technology, provides summarized and organized documentation in {deployment_url}/docs
or the ReDoc option {deployment_url}/redoc

## Endpoint

### **/telegram-webhook** (POST)
- **Description:** Endpoint that receives messages from the Telegram bot.
- **Responses:**
- **200 OK:**

- **Errors:** {"status": "error", "message": specific error}
All errors also return 200 OK and are displayed via print() to avoid the infinite error loop.

## Possible States

|number | States   |
|-------|----------|
|   1   | start    |
|   2   | progress |
|   3   | orders   |
|   4   | debts    |

## Possibilities for Greetings



|Possibilities | Text                                                                                                                |
|--------------|---------------------------------------------------------------------------------------------------------------------|
|       1      | Hello, I'm the DiscoverIT auto-attendant. My main function is to test the different...                              |
|       2      | Hello, I'm the DiscoverIT auto-attendant bot, designed to test the capabilities of this technology in your company. |
|       3      | Greetings, I'm the DiscoverIT auto-attendant. I'm a bot designed to test the capabilities of this technology        |
|       4      | Hello, I'm the DiscoverIT auto-attendant, designed to show the scope of this technology                             |

(Guideline translation)

### Start

- Detects if the message is the user's first.

- Determines if the message is valid (as only text or contact messages are allowed).

## Statuses

### Start

An opening is executed with a greeting randomly chosen from 4 possible greetings, providing the user with navigation options:



>{possible greetings}                                  
> I'll leave the following options for you to explore: 
>1. Product list                                       
>2. Place an order                                     
>3. Check my outstanding orders                        
>4. Claims                                             
>5. I need to contact a representative                 


(Guideline translation)

Changing the status to condition 2 (progress)

### progress

This state presents the initial or complete management of the user's 5 navigation options.

#### 1. Product List

All products are captured from the database and compared with the data previously stored on the server. If both data sets are identical, the process continues unchanged. Otherwise:

- A PDF file is generated with the data extracted from the database.
- The PDF file is uploaded to the AWS S3 cloud storage service.
- The following message is sent to the user:


>Download the PDF file here:                               
>https://{Region}.amazonaws.com/{Bucket-Name}/products.pdf 


Finally, the user's status changes to **1 (start)**.

##### Example of generated PDF:
You can download an example of the generated PDF file by clicking the following link:

[Download PDF](products.pdf)

#### 2. Place an order

An error has been sent due to the current inability to resolve the query, temporarily:


>Oops! We are currently not accepting orders through this channel. 
>Please contact us                                                 
>At: +59 9 223 X XXXXXX                                            
>Mon to Fri from 9:00 AM to 5:00 PM                                
>and we can resolve your request                                   
>If you need information again, I'll be here.                      


(Guideline translation)

The status remains at position 2 (progress)

#### 3. Check my outstanding orders

A message is sent requesting information to continue with the query:


>To inquire about outstanding orders, we need your valid address (as follows: street address).  
>Please contact us                                                                              
>At: +59 9 223 X XXXXXX                                                                         
>Mon to Fri from 9:00 AM to 5:00 PM                                                             
>and we can resolve your request                                                                
>If you need more information, I'll be here.                                                    

(Guideline translation)

Changing the status to 3 (orders)

#### 4. Claims

A message is sent:


>From this automated unit, we can only assist you with claims.                                                  
>These can be made by the following means: Phone or WhatsApp.                                                   
>At: +59 9 223 X XXXXXX                                                                                         
>Mon to Fri from 9:00 AM to 5:00 PM                                                                             
>Remember to have your shipping receipts (preferably in digital format) as well as personal information on hand.
>If you need information again, I'll be here.                                                                   


(Guideline translation)

Changing user status to 1 (start)

#### 5. I need to contact a representative

Reply message:


>We cannot automatically redirect your request from this unit.                                               
>These can be done by the following means: Phone or WhatsApp.                                                
>To: +59 9 223 X XXXXXX                                                                                      
>Mon to Fri from 9:00 AM to 5:00 PM                                                                          
>If you need information again, I'll be here.                                                                


(Guideline translation)

Changing user status to 1 (start)

#### Message Error

If the message cannot be read, either because it contains no text or because the message content is invalid:

Sending:


>Please send a message with a valid value.   


(Guideline translation)

Maintaining status.


### orders

- The customer is identified using the provided address.

If the customer cannot be identified, send the following message (changing its status to 1 (start)):


>Multiple customers were found with the same address. Please contact a representative to resolve this case.   
>At: +59 9 223 X XXXXXX                                                                                       
>Mon to Fri from 9:00 AM to 5:00 PM                                                                           


(Guideline translation)

If the database query did not return a result (maintaining status):


>We were unable to match the address provided with an active customer.                  
>Please try again, using all lowercase characters and no spaces.                        
>As follows: street height                                                              
>If you continue to have problems, please contact us via WhatsApp at +54 9 223 X XXXXXX 


(Guideline translation)

- We will proceed to inquire about orders that are not labeled as paid *see table: orders.

If no outstanding orders are found, the following message will be returned (returning to status 1 (start)):


>We were unable to find the outstanding orders,                                         
>If you believe this is an error, please contact us via WhatsApp at +54 9 223 X XXXXXX, 
>Our representatives can assist you with your concern                                   


(Guideline translation)

- Then, the orders are requested by linking them to the assigned worksheet in order to specify the date each order was placed.

If it is not found, there is an inconsistency in the data storage, which would lead to the following message (changing the status to 1 (start)):


>An error occurred while loading data                           
>Please contact us via WhatsApp at +54 9 223 X XXXXXX,          
>Our representatives can assist you                             


(Guideline translation)

- Payments made by the customer for each order are reviewed; a message can be sent with the information requested by the customer.

    ```

                                |-------------------------------------------------------------------------|
                                |For customer with ID: {customer id} with address at: {address provided}  |
                                |A total of {number of orders} order(s) are recorded                      |
                                |-------------------------------------------------------------------------|

                    +                                              or                                           +


    |----------------------------------------------|                                        |------------------------------------------|
    |Order delivered on: {date of first order}     |                                        |Order delivered on: {date of first order} |
    |Total: {total order value}                    |                                        |Total: {total order value}                |
    |Payments recorded:                            |                                        |No payments found                         |
    |Date: {payment date} Amount: {amount paid}    |                                        |------------------------------------------|
    |----------------------------------------------|

(Guideline translation)

The message will be extended depending on the number of orders and their status.

In the event of an unexpected error in the final process, please send a message:


>An error occurred while processing your request. Please try again later.


(Guideline translation)

### debts

It is currently under development and has no functionalities. Orders may be placed through this method in the future.

### Variables de Entorno
Crea un archivo `.env` con:
    ```env

    TELEGRAM_TOKEN = "75678644:AAGNJrjjlj1w6PZjhG0AB9qmnjfkjrtyeas" (EJEMPLO)

    db_sql_database={NOMBRE_DE_LA_DATABASE}
    db_sql_host={HOST}
    db_sql_port={PUERTO}
    db_sql_password={CONTRASEÑA}
    db_sql_user={USUARIO}

    on_dev="Y" (O "N" EN CASO DE ESTAR EN PRODUCCION)

    AWS_ACCESS_KEY_ID ="HGTGTYSTYHJJDMNCVB" (EJEMPLO)
    AWS_SECRET_ACCESS_KEY="FEGUHIFEGUFAGMdfiufgJFDBFG564/AGFD" (EJEMPLO)

### Execution

#### Local Environment

1. It is recommended to run the project in a virtual environment to avoid conflicts with other system dependencies.

If you don't have a virtual environment configured, you can create and activate it with the following commands:
Create a virtual environment (if you don't have one)
python -m venv venv

Activate the virtual environment
On Windows:
venv\Scripts\activate

On Linux/Mac:
source venv /bin/activate

Terminal example:
{located in project root}> python -m venv venv
{located in project root}> venv\Scripts\activate
(venv) {located in project root}>

2. Installing dependencies:
pip install -r requirements.txt

3. Starting the server

Server startup command:

{located in project root}> uvicorn main:app --host 0.0.0.0 --port 8000 --reload

The main.py file contains two important functions that check the environment before starting the server:

4. Environment Check
check_environment_variables()
Verifies that all environment variables are correctly defined:
- Positive response: *---All environment variables are correctly defined.---*
- Negative response: The following environment variables are missing: XXX, ZZZ, YYY

5. Check the database connection
is_connected()
Verifies the database connection (in this case, MySQL)
- Positive response: Successful connection to the database
- Negative response: Error connecting to the database: {specific error}

6. Terminal output example
Terminal output example:
INFO:     Will watch for changes in these directories: ['{located at the root of the project}']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [14632] using WatchFiles
*---Todas las variables de entorno están definidas correctamente.---* 
Conexión exitosa a la base de datos.
INFO:     Started server process [14040]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

Once the server is up and running, you can access the API in your browser or using tools like curl, Postman, or Thunder Client:

Base URL: http://localhost:8000

And if the 'on_dev' environment variable == "Y":

Interactive documentation (Swagger UI): http://localhost:8000/docs

Alternative documentation (ReDoc): http://localhost:8000/redoc

Otherwise, i.e., 'on_dev' != "Y"

It will not be visible; this is especially useful for project deployment.

7. Shutdown

To shut down the server: press CTRL+C

and the virtual environment: in the terminal where it is running: (venv) {located in the project root} > deactivate

#### Bot

Use BotFather to register a bot and have it provide a TELEGRAM_TOKEN

Search for BotFather and follow the instructions.

#### Commands by Path

Use the following command to configure the Telegram Webhook:

curl -F "url=https://{YOUR_DOMAIN}/telegram-webhook" https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook

- Replace {YOUR_DOMAIN} with the public URL of your server (for example, https://mypi.com).
- Replace {TELEGRAM_TOKEN} with the token you obtained from BotFather.

To verify that the webhook is configured correctly, use this command:

curl https://api.telegram.org/bot{TELEGRAM_TOKEN}/getWebhookInfo

This will show you information about the webhook's status.


#### Infinite Loop

During development, an infinite loop may occur if Telegram doesn't receive an HTTP 200 OK response after sending an update to your server. This causes Telegram to continually resend the same update, causing a repetitive cycle.

To locate the ID of the problematic message or view the list of messages that haven't been successfully processed yet, you can use:

curl https://api.telegram.org/bot<TELEGRAM_TOKEN>/getUpdates

- Replace <TELEGRAM_TOKEN> with your bot's token (the one you obtained from BotFather).

returning something like this:
    ```r
    {
        "ok": true,
        "result": [
            {
                "update_id": 123456789,
                "message": {
                    "message_id": 1,
                    "from": {
                        "id": 987654321,
                        "is_bot": false,
                        "first_name": "Usuario",
                        "username": "usuario_prueba",
                        "language_code": "es"
                    },
                    "chat": {
                        "id": 987654321,
                        "first_name": "Usuario",
                        "username": "usuario_prueba",
                        "type": "private"
                    },
                    "date": 1698765432,
                    "text": "Hola, soy un mensaje pendiente."
                }
            }
        ]
    }

Path command to ignore problematic messages:

During development, if you're already stuck in an infinite loop, you can use a path command to ignore duplicate messages and continue with the next message sent by Telegram.

curl -X POST https://api.telegram.org/bot<TELEGRAM_TOKEN>/getUpdates -d '{"offset": <UPDATE_ID>}'

- Replace <TELEGRAM_TOKEN> with your bot token.
- Replace <UPDATE_ID> with the ID of the last duplicate message. This will cause Telegram to ignore all messages with an ID less than or equal to the specified one.

##### EXAMPLE:
Suppose you receive the following JSON when running getUpdates:
    ```r
    {
        "ok": true,
        "result": [
            {
                "update_id": 123456789,
                "message": {
                    "message_id": 1,
                    "from": { ... },
                    "chat": { ... },
                    "date": 1698765432,
                    "text": "Mensaje duplicado"
                }
            },
            {
                "update_id": 123456790,
                "message": {
                    "message_id": 2,
                    "from": { ... },
                    "chat": { ... },
                    "date": 1698765433,
                    "text": "Otro mensaje duplicado"
                }
            }
        ]
    }

To ignore these messages duplicates, use the following command:

curl -X POST https://api.telegram.org/bot<TELEGRAM_TOKEN>/getUpdates -d '{"offset": 123456791}'

This will cause Telegram to ignore all messages with an update_id less than or equal to 123456790.

#### Procfile
web: uvicorn main:app --host 0.0.0.0 --port $PORT

### Licenses
- **This project**: MIT License (see [LICENSE](LICENSE)).
- **Dependencies**: See [LICENSES.md](LICENSES.md).
- **Note**: `mysql-connector-python` is under the GPL. If you use this code in production, consider migrating to `pymysql` (MIT License).

































