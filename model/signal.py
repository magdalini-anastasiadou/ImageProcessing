from typing import Callable


class Signal:
    def __init__(self):
        self._callbacks = []

    def connect(self, callback: Callable) -> None:
        self._callbacks.append(callback)

    def disconnect(self, callback: Callable) -> None:
        self._callbacks.remove(callback)

    def emit(self, *args, **kwargs):
        for callback in self._callbacks:
            callback(*args, **kwargs)