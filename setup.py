from setuptools import setup, find_packages

setup(
    name='ScottyInt',
    version='0.1.0',
    author='Toby Cortez',
    author_email='Tcortez@fullsail.edu',
    packages=find_packages(),
    url='http://atomicyetigaming.com',
    license='LICENSE.txt',
    description='Interactive 7DTD and Beam fun with ScottyBot',
    long_description=open('README.txt').read(),
    install_requires=[
        "websocket-client == 0.18.0"
    ],
)
