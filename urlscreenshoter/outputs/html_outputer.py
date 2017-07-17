from urlscreenshoter.outputs.abstract_outputer import *
from htmldom import htmldom

class HtmlOutputer(AbstractOutputer):
    ext = '.html'


    def openfile(self, file_name):
        self.file = open(file_name + self.ext, 'w') 
        self.dom = htmldom.HtmlDom().createDom( """<html>
        <head>
            <style>
                a{
                    width: 256px;
                    height: 192px;
                }   
            </style>
        </head>
        <body></body>
                </html>""")
        self.body = dom.find('body')

    def writerow(self, data):
        body.append('<a href="{}"><img src="{}" /></a>'.format(data[0],data[1])) 
        self.file.write(dom.html())
        self.file.flush()


    def closefile(self):
        self.file.close()
