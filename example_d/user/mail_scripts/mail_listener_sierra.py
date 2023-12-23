import imaplib
import email
from datetime import datetime
from binance_d.example_d.user.mail_scripts.mail_from_sierra import send_mail_now

# Credenciales de autenticación
username = 'sierramatic@gmail.com'
password = 'ybbffoywplpodtyd'
'''

# Conectar al servidor IMAP de Gmail
imap = imaplib.IMAP4_SSL('imap.gmail.com')
imap.login(username, password)
imap.select('inbox')

# Buscar todos los correos electrónicos en la bandeja de entrada
status, messages = imap.search(None, 'ALL')
messages = messages[0].split(b' ')

# Loop para procesar los correos electrónicos
for msg in messages:
    # Obtener el correo electrónico
    _, msg_data = imap.fetch(msg, '(RFC822)')
    email_data = msg_data[0][1]
    message = email.message_from_bytes(email_data)

    # Obtener el asunto y el cuerpo del correo electrónico
    subject = message['subject']
    print("subject", subject)
    print("type subject", type(subject))
    #body = message.get_payload(decode=True).decode()
    if 'sierra' in subject:
        print("ok found") 
    else:
        print("pass")
    #print("message", message)

    # Realizar una acción basada en el contenido del correo electrónico
    body = "" 
    if 'from sierra' in body and 'sierra' in subject:
        # Hacer algo
        print("body", body)
        #pass
    else:
        # Hacer algo más
        print("else")
        #pass

# Cerrar la conexión
imap.close()
imap.logout()
+++++++++++++++

import imaplib
import email

# Credenciales de Gmail
username = 'tu_correo@gmail.com'
password = 'tu_contraseña'

# Conexión al servidor de Gmail a través de IMAP
imap_server = imaplib.IMAP4_SSL('imap.gmail.com')
imap_server.login(username, password)
imap_server.select('INBOX')

# Ordenar los correos electrónicos por fecha descendente
status, messages = imap_server.sort('DATE', 'UTF-8', 'ALL')

# Obtener sólo los últimos N correos electrónicos
n = 10
latest_messages = messages[-n:]

# Obtención de los detalles de cada correo electrónico encontrado
for message_id in latest_messages:
    status, message_data = imap_server.fetch(message_id, '(RFC822)')
    email_message = email.message_from_bytes(message_data[0][1])
    subject = email_message['Subject']
    print(f'Asunto: {subject}')
    # Aquí puedes procesar el correo electrónico de acuerdo a tus necesidades

# Cierre de la conexión con el servidor de Gmail
imap_server.close()
imap_server.logout()

####
'''
import os
import time
import threading

filename = 'archivo.txt'
path = './'

def search_mail():
    print("in search_mail")
    exists_mail = False
    # Conexión al servidor de Gmail a través de IMAP
    imap_server = imaplib.IMAP4_SSL('imap.gmail.com')
    imap_server.login(username, password)
    imap_server.select('INBOX')

    # Búsqueda de correos electrónicos por asunto
    my_string = "sierra control"
    #my_string = "sierra status"
    #query = '(subject "' + my_string + '")'
    query = '(UNSEEN subject "' + my_string + '")'
    #ok status, messages = imap_server.search(None, query) # no es case sensitive en gmail
    # no es case sensitive en gmail
    #status, messages = imap_server.sort(status, 'DATE', 'UTF-8')

    # Busca correos con el subject "Ejemplo de Subject"
    result, data = imap_server.search(None, query) # no es case sensitive en gmail
   # result, data = imap_server.search(None, "SUBJECT 'sierra control'")
    print("result", result)
    print("data", data)
 # Obtener las capacidades del servidor
    #capabilities = imap_server.capability()
    #print(capabilities)
# gmail no tiene capability de sort:
#('OK', [b'IMAP4rev1 UNSELECT IDLE NAMESPACE QUOTA ID XLIST CHILDREN X-GM-EXT-1 UIDPLUS COMPRESS=DEFLATE ENABLE MOVE CONDSTORE ESEARCH UTF8=ACCEPT LIST-EXTENDED LIST-STATUS LITERAL- SPECIAL-USE APPENDLIMIT=35651584'])

    #typ, data = imap_server.search(None, 'SUBJECT', 'sierra control')
   # typ, data = imap_server.search(None, query)
    ids = data[0].split()
    #print("ids", ids)
    if ids:
        print("ids", ids)
        exists_mail = True
    else:
        print("ids empty")
# buscar correo electrónico específico por ID
    for num in ids:
# el fetch marca automaticamente el correo como leido/seen en gmail
        result, message_data = imap_server.fetch(num, '(RFC822)')
# convertir los datos en objeto email
        raw_email = message_data[0][1]
        email_message = email.message_from_bytes(raw_email)
        #print("email_message", email_message)
# mostrar información del correo electrónico
#        print('Subject:', email_message['Subject'])
        subject = email_message['Subject']
        sender = email_message['From']
        date = email_message['Date']
        #print('Body:', email_message.get_payload())
        print(f'Subject: {subject}, From: {sender}, Date: {date}') 
    
    # Hacer algo con la información extraída
    # Obtener la fecha del correo electrónico
        date_str = email_message['Date']
        date_tuple = email.utils.parsedate_tz(date_str)
        print("date_tuple", date_tuple)
            # Convertir la fecha a formato datetime
        if date_tuple:
            utc_time = datetime.utcfromtimestamp(email.utils.mktime_tz(date_tuple))
            print("Fecha del correo electrónico:", utc_time)
            epoch_timestamp = time.mktime(date_tuple[:9])
            print(epoch_timestamp)
    '''
        # para case sensitive
        if my_string in subject: 
            print(f'in search_mail , mail encontrado, subject: {subject}')
    '''    
    # Cierre de la conexión con el servidor de Gmail
    imap_server.close()
    imap_server.logout()
    return exists_mail
 
def monitor_file():
    while True:
        if os.path.exists(os.path.join(path, filename)):
            print("El archivo", filename, "ha sido encontrado.")
            # Ejecutar alguna acción aquí
            print("ejecutando send_mail_now")
            send_mail_now()
            print("ejecutado")
            
            #break
        else:
            print("Archivo no encontrado. Esperando 5 segundos...")
            time.sleep(5)

def monitor_mail():
    while True:
        if search_mail(): 
            print("El mail ha sido encontrado.")
            # Ejecutar alguna acción aquí
            print("ejecutando send_mail_now")
            send_mail_now()
            print("ejecutado")
           # break
            #time.sleep(5) 
        else:
            print("mail no encontrado. Esperando 5 segundos...")
        print("sleeping 30")
        time.sleep(30)


#monitor_thread = threading.Thread(target=monitor_file)
monitor_thread = threading.Thread(target=monitor_mail)
monitor_thread.start()

