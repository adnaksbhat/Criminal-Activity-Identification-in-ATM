import smtplib
from email.message import EmailMessage

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
    -email_alert("🔴🔴🔴  ALERT! ALERT! ALERT!  🔴🔴🔴", "Crimnal Activities Identified","adnaks7bhat@gmail.com")