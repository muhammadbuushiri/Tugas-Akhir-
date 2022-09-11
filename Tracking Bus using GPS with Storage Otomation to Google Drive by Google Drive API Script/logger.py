from dataclasses import field
import mimetypes
from multiprocessing.connection import Client
from googleapiclient.http import MediaFileUpload
from Google import Create_Service

import datetime
import board
import busio
import adafruit_gps

LOG_FILE = datetime.datetime.now().strftime("track-%y%m%d-%H%M%S.txt")
#suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S.txt")
#filename = "_".join([LOG_FILE, suffix])
LOG_MODE = "ab"

import serial
uart = serial.Serial("/dev/serial0", baudrate=9600, timeout=10)
running = True

gps = adafruit_gps.GPS(uart)
with open(LOG_FILE, LOG_MODE) as outfile:
    while running:
        try:
            sentence = gps.readline()
            if not sentence:
                continue
            print(str(sentence, "ascii").strip())
            outfile.write(sentence)
            outfile.flush()

        except KeyboardInterrupt:
#           print("Program Stopped")
            CLIENT_SECRET_FILE = 'client_secrets.json'
            API_NAME = 'drive'
            API_VERSION = 'v3'
            SCOPES = ['https://www.googleapis.com/auth/drive']

            service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

            folder_id = '1wPmQCnFOIpB7qApcJfMZ0pOCnA03ldhK'
            file_names = [LOG_FILE]
            mime_types = ['text/plain']
            for file_name,mime_type in zip(file_names,mime_types):
                file_metadata = {
                    'name' : file_name,
                    'parents' : [folder_id]
                }

                media = MediaFileUpload('./{0}'.format(file_name), mimetype=mime_type)

                service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id'
                ).execute()
            running = False
            outfile.close()


        except Exception as e:
            retVal = {'status' : 'False', 'msg' : 'Python3 Exception : {}'.format(e)}
        else:
            retVal = {'status' : 'True', 'msg' : 'download'}
