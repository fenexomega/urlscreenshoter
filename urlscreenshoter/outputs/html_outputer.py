from urlscreenshoter.outputs.abstract_outputer import *
from htmldom import htmldom

class HtmlOutputer(AbstractOutputer):
    ext = '.html'
    
    def __init__(self, file_name):
        self.openfile(file_name)
    

    def openfile(self, file_name):
        self.file_name = file_name
        self.file = open(file_name + self.ext, 'w') 
        self.page = htmldom.HtmlDom().createDom( """<html>
        <head>
            <style>
            body{
                background-color: #212121    
            }
                div{
                    width: 256px;
                    float: left;
                    height: 192px;
                    padding: 4px;
                }   
            </style>
        </head>
        <body></body>
                </html>""")
        self.body = self.page.find('body')
        self.file.write(self.page.find('html').html())
        self.file.close()

    def writerow(self, data):
        self.file = open(self.file_name + self.ext, 'w') 
        self.body.append('<a target="_blank" href="{}"><div><img width="256" height="192" src="{}" /></a></div>'.format(data[0],data[1])) 
        self.file.write(self.page.find('html').html())
        self.file.close()


    def closefile(self):
        pass
