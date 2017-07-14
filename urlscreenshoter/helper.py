import hashlib,os
from selenium import webdriver
from PIL import Image

class Helper:
    @staticmethod
    def fix_url(url):
        if not "http" in url:
            return "http://" + url
        return url

    @staticmethod
    def takeScreenshotFromUrl(url,file,res):
        url = Helper.fix_url(url)
        driver = webdriver.PhantomJS(service_log_path=os.path.devnull)
        driver.set_window_size(res[0],res[1])
        driver.get(url)
        driver.save_screenshot(file)
        
    @staticmethod
    def sha1FromFile(file):
        hash = hashlib.sha1()
        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash.update(chunk)
        return hash.hexdigest()
        
    @staticmethod
    def convertImage(old,new,crop):
        dir =  os.path.dirname(old)
        #save file
        try:
            img = Image.open(old)
            if crop != None:
                background = Image.new('RGB',(1024,768),(255,255,255,255))
                img = img.crop(crop)
            else:
                background = Image.new('RGB',(1024,768),(255,255,255,255))
            background.paste(img,mask=img.split()[3])
            background.save(new)
        except IOError as e:
            print("cannot convert {}".format(e))

