
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email(data):
    try:
        message = MIMEMultipart()
        message['Subject'] = 'Price drop alert from python script.'
        mail_content=f'''
Hello, {data["website"]} product, named {data["productname"]} is available at price {data["price"]}
To buy, please click below link
{data["url"]}
For more details, please see the attached screenshot
        '''
        message['From'] = 'pyproj1212@gmail.com'
        message['To'] = data["receiver_mail"]


        message.attach(MIMEText(mail_content, 'plain'))
        attach_file_name = 'hello.png'
        attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
        payload = MIMEBase('application', 'octate-stream')
        payload.set_payload((attach_file).read())
        encoders.encode_base64(payload) #encode the attachment
        #add payload header with filename
        
        #payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
        payload.add_header(
            "Content-Disposition",
            f"attachment; filename= {attach_file_name}",
        )

        message.attach(payload)
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login('pyproj1212@gmail.com', 'pyproj1212@123') #login with mail_id and password
        text = message.as_string()
        session.sendmail('pyproj1212@gmail.com', data["receiver_mail"], text)
        session.quit()
        print(f'Alert email sent to {data["receiver_mail"]} from "pyproj1212@gmail.com", Thanks for using our script')

    except Exception as e:
        print ('Error occured while sending email' +str(e))
# data={}
# data["receiver_mail"]="tatanithin007@gmail.com"
# send_email(data)