import setuptools

setuptools.setup(name='urlscreenshoter',
         version='0.2.0',
         description='URL Screenshots take screenshots from the URL and upload then to IMGUR',
         long_description=open('README.md').read().strip(),
         author='Jordy Ferreira',
         author_email='jordyfgomes@gmail.com',
         url='http://path-to-my-packagename',
         packages=['urlscreenshoter'],
         install_requires=['pillow','selenium','configparser','imgurpython',
             'requests','argparse'],
         entry_points={
             'console_scripts':[
                 'urlscreenshoter = urlscreenshoter.main:main'
                 ]
         },
         data_files = [
             ('/etc/', ['urlscreenshoter.conf'])
         ],
         license='GPLv2',
         keywords='url screenshot imgur phantomjs',
         classifiers=['web', 'screenshot', 'imgur'])
