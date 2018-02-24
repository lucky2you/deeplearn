# -*- coding: utf-8 -*-


class Simulator:

    def __init__(self):
        self.processors = {}

        return

    def add(self, processor):
        if processor.name in self.processors:
            raise RuntimeError('Porcessor %s already exist' % processor.name)

        self.processors[processor.name] = processor

    def remove(self, name):
        processor = {}
        if name in self.processors:
            processor = self.processors.pop(name)

        return processor

    def connect(self, up, down):
        if up.name not in self.processors:
            raise RuntimeError('Processor %s dose not exist' % up.name)
        if down.name not in self.processors:
            raise RuntimeError('Processor %s dose not exist' % down.name)

        up.outputs.append(down)
        down.inputs.append(up)

    def set_values(self, values):
        processors = {}
        for k in values:
            keys = k.split('_', 1)
            if keys[0] not in processors:
                processors[keys[0]] = {}

            processors[keys[0]][keys[1]] = values[k]

        for k in processors:
            if k in self.processors:
                self.processors[k].set_values(processors[k])

        return

    def dump_values(self):
        values = {}

        for name in self.processors:
            v = self.processors[name].dump_values()
            for k in v:
                values[name + '_' + k] = v[k]

        return values

    def step(self, interval):
        for name in self.processors:
            self.processors[name].calc_inputs()

        for name in self.processors:
            self.processors[name].calc_outputs(interval)

        return
