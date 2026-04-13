from abc import ABCMeta, abstractmethod


class cli():
    """
    Command-line interface for icee-utils.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def exit(self):
        pass
