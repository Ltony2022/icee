from abc import ABCMeta, abstractmethod


class ApplicationBlock(metaclass=ABCMeta):
    """
    ApplicationBlock abstract class
    """

    @abstractmethod
    def add_block_application(self, application_name: str) -> tuple[bool, list[dict]]:
        pass

    @abstractmethod
    def remove_block_application(self, application_name: str) -> list[dict]:
        pass

    @abstractmethod
    def list_blocked_application(self) -> list[dict]:
        pass

    @abstractmethod
    def enforce_block(self) -> list[dict]:
        pass

    @abstractmethod
    def disable_block(self) -> list[dict]:
        pass
