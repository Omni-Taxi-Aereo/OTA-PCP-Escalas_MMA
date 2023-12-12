import yagmail

login = 'ti.digital@omnibrasil.com.br'
senha = 'ictrxbjknbignywd'
destinatarios = ['alan.chagas@omnibrasil.com.br', 'nathan.carvalho@omnibrasil.com.br', 'eduardo.succo@omnibrasil.com.br', 'daniel.fumian@omnibrasil.com.br' ]
assunto = 'Script Escalas MMA ERRROR'

def send_email(corpo, anexos=[], Cco=[]):
    try:
        print('-> Enviando o e-mail...')
        yag = yagmail.SMTP(login, senha)
        yag.send(
            to=destinatarios,
            subject=assunto,
            contents=corpo,
            attachments=anexos,
            bcc=Cco  
        )
        print(f'E-mail enviado para {", ".join(destinatarios)} com sucesso!')
    except Exception as e:
        raise e

def send_email_assunto(assunto,corpo, anexos=[], Cco=[]):
    try:
        print('-> Enviando o e-mail...')
        yag = yagmail.SMTP(login, senha)
        yag.send(
            to=destinatarios,
            subject=assunto,
            contents=corpo,
            attachments=anexos,
            bcc=Cco  
        )
        print(f'E-mail enviado para {", ".join(destinatarios)} com sucesso!')
    except Exception as e:
        raise e

def send_email_assunto_destinatarios(assunto,destinatarios, corpo, anexos=[], Cco=[]):
    try:
        print('-> Enviando o e-mail...')
        yag = yagmail.SMTP(login, senha)
        yag.send(
            to=destinatarios,
            subject=assunto,
            contents=corpo,
            attachments=anexos,
            bcc=Cco  
        )
        print(f'E-mail enviado para {", ".join(destinatarios)} com sucesso!')
    except Exception as e:
        raise e
    
