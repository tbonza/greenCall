#! /usr/bin/env python

descr = "Async API requests from CSV file"

from distutils.core import setup

setup(
    name='greenCall',
    version='0.2.0',
    maintainer='Tyler Brown',
    maintainer_email='tbrown@greenzoneinc.com',
    packages=['greencall'],
    scripts=['examples/okgo.py'],
    url='http://tbonza.github.io/',
    license='LICENSE.md',
    description= descr,
    long_description=open('README.md').read(),
    install_requires=[
        "cffi==1.1.2",
        "characteristic==14.3.0",
        "cryptography==0.9.1",
        "enum34==1.0.4",
        "idna==2.0",
        "ipaddress==1.0.7",
        "pyasn1==0.1.7",
        "pyasn1-modules==0.0.5",
        "pycparser==2.14",
        "pyOpenSSL==17.5.0",
        "service-identity==14.0.0",
        "six==1.9.0",
        "Twisted==15.2.1",
        "zope.interface==4.1.2",
        ],
)

    
