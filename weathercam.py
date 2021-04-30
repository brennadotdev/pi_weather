import argparse
from time import sleep
from picamera import PiCamera
from ftplib import FTP

parser = argparse.ArgumentParser(description='Use the attached camera to take a photo and upload it to wunderground')
parser.add_argument('--flipvertical', action='store_true', dest='vflip', help='Flip the image vertically')
parser.add_argument('--fliphorizontal', action='store_true', dest='hflip', help='Flip the image horizontally')
parser.add_argument('--deviceid', type=str, help='Your wunderground camera device id')
parser.add_argument('--uploadkey', type=str, help='Your wunderground upload key')

args = parser.parse_args()
fileName = 'still.jpg'

with PiCamera() as camera:
    camera.vflip = args.vflip
    camera.hflip = args.hflip
    camera.resolution = (1024, 768)
    sleep(2)
    camera.capture(fileName)
    pass

with open(fileName, 'rb') as file:
    with FTP("webcam.wunderground.com", user=args.deviceid, passwd=args.uploadkey) as ftp:
        ftp.cwd('/')
        ftp.storbinary('STOR image.jpg', file)
