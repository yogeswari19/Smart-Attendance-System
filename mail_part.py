import cv2
import time
import face_recognition
import numpy as np
from datetime import datetime
from threading import Thread
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from smtplib import SMTP
import csv
import os
import pickle
import try_pickle
import pandas as pd

email = ""

class Error(Exception):
    """Base class for other exceptions"""
    pass


class NameNotinList(Error):
    """Raised when the input value is too small"""
    pass


class EmailThread(Thread):

    def __init__(self, email_to):
        self.email_to = email_to
        Thread.__init__(self)

    def run(self):
        body = "your html body"
        text = "your plain body"
        message = MIMEMultipart("alternative")
        message["Subject"] = "subject"
        message["From"] = "yogeswari.mythology@gmail.com"
        message["To"] = self.email_to
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(body, "html")
        message.attach(part1)
        message.attach(part2)
        server = smtplib.SMTP_SSL("smtp.gmail.com",465)
        server.login("yogeswari.mythology@gmail.com", 'ogafeauurtukzogd')
        server.sendmail("yogeswari.mythology@gmail.com", self.email_to, message.as_string())
        print("mail sent")
        # df=pd.read_csv("face_recognition.csv")
        # df['mail details'] = "mail sent"
        return True

def writeintocsv(name):
    with open('face_recognition.csv', 'r+') as f:
        my_data_list = f.readlines()[1:]
        namelist = []
        for line in my_data_list:
            entry = line.split(',')
            namelist.append(entry[0])
        if name not in namelist:
            now = datetime.now()
            dt_string = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dt_string}')
            mail_dict = {'yogeswari': 'yogeswari.20ad@kct.ac.in', 'Mirudhula': 'mirudhula2864@gmail.com'}
            for i in mail_dict:
                if i == name:
                    email_to = str(mail_dict[i])
                    print(email_to)
                    obj = EmailThread(email_to)
                    obj.run()