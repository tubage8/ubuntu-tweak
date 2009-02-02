#!/usr/bin/python

# Ubuntu Tweak - PyGTK based desktop configure tool
#
# Copyright (C) 2007-2008 TualatriX <tualatrix@gmail.com>
#
# Ubuntu Tweak is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Ubuntu Tweak is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ubuntu Tweak; if not, write to the Free Software Foundation, Inc.,

import os
import gtk
import gconf
from common.factory import GconfKeys

class Config:
    #FIXME The class should be generic config getter and setter
    __client = gconf.Client()

    def set_value(self, key, value):
        if not key.startswith("/"):
            key = GconfKeys.keys[key]

        if type(value) == int:
            self.__client.set_int(key, value)
        elif type(value) == float:
            self.__client.set_float(key, value)
        elif type(value) == str:
            self.__client.set_string(key, value)
        elif type(value) == bool:
            self.__client.set_bool(key, value)

    def get_value(self, key):
        if not key.startswith("/"):
            key = GconfKeys.keys[key]
		
        try:
            value = self.__client.get_value(key)
        except:
            return None
        else:
            return value

    def set_pair(self, key, type1, type2, value1, value2):
        if not key.startswith("/"):
            key = GconfKeys.keys[key]
		
        self.__client.set_pair(key, type1, type2, value1, value2)

    def get_pair(self, key):
        if not key.startswith("/"):
            key = GconfKeys.keys[key]

        value = self.__client.get(key)
        if value:
            return value.to_string().strip('()').split(',')
        else:
            return (0, 0)

    def get_string(self, key):
        if not key.startswith("/"):
            key = GconfKeys.keys[key]

        string = self.get_value(key)
        if string: 
            return string
        else: 
            return '0'

    def get_client(self):
        return self.__client

class TweakSettings:
    '''Manage the settings of ubuntu tweak'''
    url = 'tweak_url'
    version = 'tweak_version'
    toolbar_size = 'toolbar_size'
    toolbar_color = 'toolbar_color'
    window_size= 'window_size'
    window_height = 'window_height'
    window_width = 'window_width'
    show_donate_notify = 'show_donate_notify'
    default_launch = 'default_launch'
    check_update = 'check_update'
    need_save = True

    def __init__(self):
        self.__config = Config()

    def get_check_update(self):
        return self.__config.get_value(self.check_update)

    def set_check_update(self, bool):
        self.__config.set_value(self.check_update, bool)

    def get_toolbar_color(self, instance = False):
        color = self.__config.get_value(self.toolbar_color)
        if color == None:
            if instance:
                return gtk.gdk.Color(32767, 32767, 32767)
            return (0.5, 0.5, 0.5)
        else:
            try:
                color = gtk.gdk.color_parse(color)
                if instance:
                    return color
                red, green, blue = color.red/65535.0, color.green/65535.0, color.blue/65535.0
                return (red, green, blue)
            except:
                return (0.5, 0.5, 0.5)

    def set_toolbar_color(self, color):
        self.__config.set_value(self.toolbar_color, color)

    def set_default_launch(self, id):
        self.__config.set_value(self.default_launch, id)

    def get_default_launch(self):
        return self.__config.get_value(self.default_launch)

    def set_show_donate_notify(self, bool):
        return self.__config.set_value(self.show_donate_notify, bool)

    def get_show_donate_notify(self):
        value = self.__config.get_value(self.show_donate_notify)

        if value == None:
            return True
        return value

    def set_url(self, url):
        '''The new version's download url'''
        return self.__config.set_value(self.url, url)

    def get_url(self):
        return self.__config.get_string(self.url)

    def set_version(self, version):
        return self.__config.set_value(self.version, version)

    def get_version(self):
        return self.__config.get_string(self.version)

    def set_paned_size(self, size):
        self.__config.set_value(self.toolbar_size, size)

    def get_paned_size(self):
        position = self.__config.get_value(self.toolbar_size)

        if position:
            return position
        else:
            return 150

    def set_window_size(self, width, height):
        self.__config.set_value(self.window_width, width)
        self.__config.set_value(self.window_height, height)
#        self.__config.set_pair(self.window_size, gconf.VALUE_INT, gconf.VALUE_INT, height, width)

    def get_window_size(self):
        width = self.__config.get_value(self.window_width)
        height = self.__config.get_value(self.window_height)

#        height, width = self.__config.get_pair(self.window_size)

        if width and height:
            height, width = int(height), int(width)
            return (width, height)
        else:
            return (740, 480)

    def get_icon_theme(self):
        return self.__config.get_value('/desktop/gnome/interface/icon_theme')

tweak_settings = TweakSettings()

if __name__ == '__main__':
    print Config().get_value('show_donate_notify')
