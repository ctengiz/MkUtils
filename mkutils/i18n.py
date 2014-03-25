# -*- coding: utf-8 -*-

"""
Helper module for i18n translation functions.

Base source from : http://webpy.org/cookbook/runtime-language-switch

__author__ : Çağatay Tengiz
__date__   : 15.11.2013
"""

import gettext


class MkTranslate(object):
    def __init__(self, localedir):
        self.localedir = localedir
        self.lang = str('tr_TR')

        # Object used to store all translations.
        self.all_translations = {}

    def get_translations(self):
        """

        :param lang:
        :return: :rtype:
        """

        # Init translation.
        if self.lang in self.all_translations:
            translation = self.all_translations[self.lang]
        elif self.lang is None:
            translation = gettext.NullTranslations()
        else:
            try:
                translation = gettext.translation(
                    'messages',
                    self.localedir,
                    languages=[self.lang],
                    codeset="UTF8"
                )
            except IOError:
                translation = gettext.NullTranslations()
        return translation


    def load_translations(self):
        """

        :param lang:
        :return: :rtype:
        """
        #lang = str(lang)
        translation = self.all_translations.get(self.lang)
        if translation is None:
            translation = self.get_translations()
            self.all_translations[self.lang] = translation

            # Delete unused translations.
            for lk in self.all_translations.keys():
                if lk != self.lang:
                    del self.all_translations[lk]
        return translation


    def custom_gettext(self, string):
        """
        Get translated string for the given language

        :param string: Text to be translated
        :param lang: Target language code
        :return: :rtype:
        """

        translation = self.load_translations()
        if translation is None:
            return unicode(string)
        return translation.gettext(string)




