
import smtplib
from email.message import EmailMessage

class notificacao():

    def __init__(self,destinatario,titulo):
        self.paraquem = destinatario
        self.titulo = titulo
        self.msg = EmailMessage()        
        self.dequem = "acesso.remoto@gsaladeaula.com.br"
        self.service = ""
        try:
            self.service = smtplib.SMTP('smtp.gmail.com')
            self.service.starttls()
            self.service.login(self.dequem,'getedu00')
            self.msg['Subject'] = self.titulo
            self.msg['From'] = self.dequem
            self.msg['To'] = [self.paraquem]
        except Exception as e:
            print(e)
    def enviar(self,msg):
        try:
            self.msg.set_content(msg)            
            self.service.send_message(self.msg)
            print("Mensagem enviada")
        except Exception as e:
            print("Falhou em enviar notificação: {}".format(e))

if __name__ == "__main__":
    email = notificacao('lucas@getedu.com.br','TESTE').enviar("TESTANDO ENVIO PELO PYTHON")