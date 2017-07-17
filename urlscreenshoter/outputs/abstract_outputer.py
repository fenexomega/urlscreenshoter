#!/usr/bin/python3
# -*- coding: utf-8 -*-

from abc import ABCMeta

class AbstractOutputer:
    __metaclass__ = ABCMeta

    def openfile(self, file_name):
        raise NotImplementedError()

    def writerow(self, data):
        raise NotImplementedError()

    def closefile(self):
        raise NotImplementedError()
    
