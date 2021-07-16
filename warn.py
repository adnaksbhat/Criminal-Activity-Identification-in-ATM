import smtplib
from email.message import EmailMessage



from datetime import datetime

 
# dd/mm/YY H:M:S
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

a="ABNORMAL ACTIVITIES DETECTED------------"
 
b=str(dt_string)

res=a+b

def email_alert(subject, body, to):
    msg=EmailMessage()
    msg.set_content(body)
    msg['subject']=subject
    msg['to']=to


    user="demoalertsystems@gmail.com"
    msg["from"]=user
    password="lbqrajggiuagykuk"


    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg)
    server.quit()



if __name__ == '__main__':
    -email_alert("🟠🟠🟠  WARNING! WARNING!  🟠🟠🟠", res,"adnaks7bhat@gmail.com")