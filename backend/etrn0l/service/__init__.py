from typing import Optional
from abc import ABC, abstractmethod, abstractproperty
from ..model import FlashLoop


class FlashFileService(ABC):
    """Meant to handle all file opperations.

    This makes it irrelevant where we actually store the files.
    They could really be anywhere.
    """
    @abstractmethod
    def set_file(self, loop_id):
        pass

    @abstractmethod
    def remove_file(self, loop_id):
        pass

    @abstractmethod
    def file_exists(self, loop_id):
        pass


class FlashLoopService(ABC):
    """Meant to handle all the database opperations."""
    @abstractmethod
    def add_loop(self, loop: FlashLoop) -> str:
        pass

    @abstractmethod
    def remove_loop(self, loop_id) -> bool:
        pass

    @abstractmethod
    def get_loop_by_id(self, loop_id) -> Optional[FlashLoop]:
        pass

    @abstractmethod
    def get_randomLoop(self) -> FlashLoop:
        pass
