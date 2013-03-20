# -*- coding: UTF-8 -*-

from datetime import datetime
import time

from configobj import ConfigObj

class ConfigStore(object):
    
    configlist = []
    
    @classmethod
    def parse_date(cls, datestring):
        if datestring != None:
            datetime_obj = datetime(*time.strptime(datestring, "%d.%m.%Y")[0:6])
            return datetime_obj.date()
        return None
        
    @classmethod
    def _insert_into_configlist(cls, valid_from, section):
        config = Configuration(valid_from=valid_from, config=section)
        for i, data in enumerate(cls.configlist):
            date_from = data.valid_from
            if valid_from == None or \
                (date_from != None and valid_from < date_from):
                cls.configlist.insert(i, config)
                return
        cls.configlist.append(config)

    @classmethod
    def read_configuration(cls, filename):
        cls.reset()
        config = ConfigObj(filename)
        config.encoding = "UTF-8"
        for sectionname in config:
            section = config[sectionname]
            valid_from = cls.parse_date(section.get("valid_from", None))
            cls._insert_into_configlist(valid_from, section)
            
    @classmethod
    def get_configurations(cls):
        return cls.configlist

    @classmethod
    def get_configuration(cls, when=None):
        if when == None:
            last_index = len(cls.configlist) - 1
            return cls.configlist[last_index]
        
        found_config = None
        for config in cls.configlist:
            date_from = config.valid_from
            if date_from != None and date_from > when:
                break
            found_config = config
        return found_config
        
        
    @classmethod
    def get_predecessor(cls, configuration):
        pre = None
        for data in cls.configlist:
            if data == configuration:
                break
            pre = data
        return pre

    @classmethod
    def reset(cls):
        cls.configlist = []


class Configuration(object):

    def __init__(self, valid_from=None, config=None):
        self.valid_from = valid_from
        self.config = config

    def __getitem__(self, key):
        try:
            return self.config[key].decode("UTF-8")
        except KeyError, e:
            previous_configuration = ConfigStore.get_predecessor(self)
            if previous_configuration != None:
                return previous_configuration[key]
            else:
                raise e


