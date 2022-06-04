"""Message Passing (Inter Task Communication)."""
import enum
from queue import Queue
from typing import List


class CameraChannel:
    queue = Queue(maxsize=60)
    listeners: List[Queue] = []

    def add_listener(self, q: Queue) -> int:
        index = len(self.listeners)
        self.listeners.append(q)
        return index

    def send(self, jpeg: bytes) -> bool:
        for q in self.listeners:
            q.put(jpeg)
        return True


class AlarmChannel:
    queue = Queue(maxsize=1)

    def publish(self, frame: int) -> bool:
        return True

    def subscribe(self) -> bool:
        return True


Command = enum.Enum("Command", "UP RIGHT DOWN LEFT", module=__name__)


class ControlsChannel:
    queue = Queue(maxsize=10)

    def publish(self, frame: Command) -> bool:
        return True

    def subscribe(self) -> bool:
        return True


Camera = CameraChannel()
Alarm = AlarmChannel()
Controls = ControlsChannel()
