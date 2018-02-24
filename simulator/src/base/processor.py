# -*- coding: utf-8 -*-


class Processor(object):
    def __init__(self, name):
        self.name = name
        self.inputs = []
        self.outputs = []

        return

    def set_values(self, values):
        for k in values:
            key = 'lab_' + k
            if key in self.__dict__:
                self.__setattr__(key, values[k])

        return

    def dump_values(self):
        values = {}

        for k in self.__dict__:
            keys = k.split('_', 1)
            if keys[0] == 'lab':
                values[keys[1]] = round(self.__getattribute__(k), 2)

        return values

    def calc_inputs(self):
        return

    def calc_outputs(self, interval):
        return
