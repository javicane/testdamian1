import imaplib
import email
from datetime import datetime
from binance_d.example_d.user.mail_scripts.mail_from_sierra import send_mail_now

# Credenciales de autenticación
username = 'sierramatic@gmail.com'
password = 'ybbffoywplpodtyd'

# Conexión al servidor de correo de Gmail
imap_server = imaplib.IMAP4_SSL('imap.gmail.com')

# Iniciar sesión en la cuenta de Gmail
imap_server.login(username, password)

# Seleccionar la carpeta "INBOX"
imap_server.select("INBOX")

# Activar el modo IDLE
response = imap_server.idle()

# Esperar a que lleguen nuevos correos
while True:
    # Leer la respuesta del servidor
    response = imap_server.readline()
    
    # Si la respuesta contiene la cadena "EXISTS", significa que ha llegado un nuevo correo
    if b"EXISTS" in response:
        print("¡Ha llegado un nuevo correo!")
    
    # Si la respuesta contiene la cadena "OK", significa que el servidor está listo para recibir otra solicitud
    if b"OK" in response:
        imap_server.idle()  # Volver a activar el modo IDLE