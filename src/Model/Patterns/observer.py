from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange
from typing import List


class Observed(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    _state: int = None
    """
    For the sake of simplicity, the Subject's state, essential to all
    subscribers, is stored in this variable.
    """

    _observers: List[Observer] = []
    """
    List of subscribers. In real life, the list of subscribers can be stored
    more comprehensively (categorized by event type, etc.).
    """

    @classmethod
    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to the subject.
        """
        if observer is not None:
            self._observers.append(observer)

    @classmethod
    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from the subject.
        """
        self._observers.remove(observer)

    @abstractmethod
    def notify(self) -> None:
        """
        Notify all observers about an event.
        """
        for observer in self._observers:
            observer.update(self)



class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, subject: Observed) -> None:
        """
        Receive update from subject.
        """
        pass