import hashlib,os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from PIL import Image

class Helper:
    @staticmethod
    def fix_url(url):
        if not "http" in url:
            return "http://" + url
        return url

    @staticmethod
    def takeScreenshotFromUrl(url,file,res):
        #https://coderwall.com/p/9jgaeq/set-phantomjs-user-agent-string
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36"
            "(KHTML, like Gecko) Chrome/37.0.2062.$")
        driver = webdriver.PhantomJS(service_log_path=os.path.devnull,desired_capabilities=dcap)
        # driver = webdriver.PhantomJS(service_log_path=os.path.devnull)
        # driver = webdriver.PhantomJS()
        driver.set_window_size(res[0],res[1])
        url = Helper.fix_url(url)
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

