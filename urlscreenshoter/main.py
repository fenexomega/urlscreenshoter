#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import argparse
import csv
import configparser
from datetime import datetime
from urlscreenshoter.helper import Helper
from urlscreenshoter.imgur_helper import ImgurHelper
from urlscreenshoter.outputs.csv_outputer import CsvOutputer
from urlscreenshoter.outputs.html_outputer import HtmlOutputer

TMP_FILE = '/tmp/screenshot.png'
SEND_FILE = '/tmp/screenshot.jpg'

def get_config_values():
    parser = configparser.ConfigParser()
    parser.read('/etc/urlscreenshoter.conf')
    client_i = parser['DEFAULT']['client_id']
    client_s = parser['DEFAULT']['client_secret']
    return client_i, client_s

def parse_resolution(string):
    res = string.split('x')
    return [int(x) for x in res]
     
def get_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,description='YOU NEED A IMGUR ACCOUNT TO USE THIS PROGRAM. A program to visit a list of URLs, screenshot these and then upload these screens to Imgur.')
    parser.add_argument('input',help='The text file that stores the URLs, one per line')
    parser.add_argument('--output',default='result.csv',metavar='-o',help='The file to store the output')
    parser.add_argument('--resolution',default='1024x768',metavar='-r',help='Resolution of screenshots')
    return parser.parse_args()

def main():
    # Tratando o input
    args = get_args()
    INPUT_FILE  = args.input
    RESOLUTION  = parse_resolution(args.resolution)
    client_id, client_secret = get_config_values()
    imgur = ImgurHelper(client_id, client_secret)
    CROP = (0,0,RESOLUTION[0],RESOLUTION[1])
    FILENAME  = INPUT_FILE.split('.')[0]

    # Abrir arquivo com URLS
    links = None
    with open(INPUT_FILE,'r') as f:
        links = [x.replace('\n','') for x in f.readlines()]

    # initialize file
    csv = CsvOutputer(FILENAME)
    html = HtmlOutputer(FILENAME)
    # visitar URLS
    for url in links:
        try:
            url = Helper.fix_url(url)
            connect = requests.get(url,timeout=5)
            print('Connected to {}'.format(url))
            if not connect.status_code in [200,302,301,307,308]:
                print('Page at {} returned code {}'.format(url,connect.status_code) )
                date = datetime.strftime(datetime.now(),'%d/%m/%Y %H:%M')
                row = [url, connect.status_code,date]
                csv.writerow(row)
                continue
            Helper.takeScreenshotFromUrl(url,TMP_FILE,RESOLUTION) 
            Helper.convertImage(TMP_FILE,SEND_FILE,CROP)
            counter = 0
            # fazer upload das imagens
            while counter < 3:
                try:
                    print('Uploading image...')
                    image = imgur.upload(SEND_FILE)
                    break
                except:
                    print('Error uploading the image, trying again')
                    counter += 1
            if counter == 3:
                print('I couldn\'t upload your image. Skiping...')
                continue
            print('screenshot from {} uploaded at {}'.format(url,image['link'])) 
            date = datetime.strftime(datetime.now(),'%d/%m/%Y %H:%M')
            row = [url,image['link'],date]
            # exportar linhas
            csv.writerow(row)
            html.writerow(row)
        except requests.exceptions.Timeout:
            print('Page at {} timed out'.format(url) )
            date = datetime.strftime(datetime.now(),'%d/%m/%Y %H:%M')
            row = [url, 'timed out', date]
            csv.writerow(row)
        except ConnectionError as e:
            print('Page at {} not found'.format(url) )
            date = datetime.strftime(datetime.now(),'%d/%m/%Y %H:%M')
            row = [url, 'not found', date]
        except Exception as e:
            print('Page {} generated a unexpected error: {}'.format(url,e))
            date = datetime.strftime(datetime.now(),'%d/%m/%Y %H:%M')
            csv.writerow([url, 'error', date])
    csv.closefile()
    html.closefile()


if __name__ == "__main__":
    main()
