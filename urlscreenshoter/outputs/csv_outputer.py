import csv
from urlscreenshoter.outputs.abstract_outputer import * 


class CsvOutputer(AbstractOutputer):
    ext = '.csv'

    def __init__(self, file_name = None):
        if file_name != None:
            self.openfile(file_name)

    def openfile(self, file_name):
        self.output = open(file_name + self.ext,'w',newline='')
        self.csvwriter = csv.writer(self.output,delimiter=',')
        self.csvwriter.writerow(['URL','IMGUR LINK','Date Visited'])

    def writerow(self, data):
        self.csvwriter.writerow(data)

    def closefile(self):
        self.output.close()
    
