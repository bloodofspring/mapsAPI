from abc import ABC, abstractmethod


class AbstractScreen(ABC):
    def __init__(self, screen, runner, **kwargs):
        self.screen = screen
        self.runner = runner

    @abstractmethod
    def update(self, events, **kwargs):
        raise NotImplemented
