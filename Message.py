"""Message Passing (Inter Task Communication)."""
import enum
from queue import Queue
from typing import List


class CameraChannel:
    queue = Queue(maxsize=60)
    listeners: List[Queue[bytes]] = []

    def add_listener(self, q: Queue[bytes]) -> int:
        index = len(self.listeners)
        self.listeners.append(q)
        return index

    def broadcast(self, jpeg: bytes) -> bool:
        for q in self.listeners:
            q.put(jpeg)
        return True
    
    def send(self, id:int, x):
        self.listeners[id].put(x)


Command = enum.Enum("Command", "UP RIGHT DOWN LEFT", module=__name__)


class ControlsChannel:
    queue: Queue[Command] = Queue(maxsize=10)

    def send(self, cmd: Command) -> bool:
        return True

    def subscribe(self) -> bool:
        return True


Camera = CameraChannel()
Controls = ControlsChannel()
