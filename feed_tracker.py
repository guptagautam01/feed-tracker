from abc import ABC, abstractmethod


class FeedTracker(ABC):
    @abstractmethod
    async def start(self, clear_backlog: bool = True):
        pass
