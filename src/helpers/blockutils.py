from abc import abstractmethod, ABCMeta


class BlockUtils:
    """
    Abstract class for blockutils.
    """

    # __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def add_block_site(self, site):
        pass

    @abstractmethod
    def list_block_sites(self):
        pass

    @abstractmethod
    def remove_block_site(self, site):
        pass

    @abstractmethod
    def enable_block_site(self):
        pass

    @abstractmethod
    def disable_block_site(self, site):
        pass
