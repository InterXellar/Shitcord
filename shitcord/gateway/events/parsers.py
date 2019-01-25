# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class Parser(ABC):
    @abstractmethod
    def parse(self, data, http):
        pass


class ModelParser(Parser):
    def __init__(self, model):
        self.model = model

    def parse(self, data, http):
        return self.model(data, http)


class NullParser(Parser):
    def parse(self, data, http):
        return data
