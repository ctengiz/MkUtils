# -*- coding: utf-8 -*-

"""
Modülün Açıklaması

__author__ : Çağatay Tengiz
__date__   : 25.12.2013
"""

from distutils.core import setup

setup(
    name='MkUtils',
    version='0.0.1alpha',
    author='Makki - Cagatay Tengiz',
    author_email='cagatay.tengiz@makki.com.tr',
    packages=['mkutils', ],
    license='MIT',
    description='Collection of helper functions used in various projects developed by Makki.',
    long_description=open('README.txt').read(),
)
