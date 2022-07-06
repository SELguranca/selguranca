"""Message Passing (Inter Task Communication)."""
from enum import Enum
from hashlib import sha256
from uuid import uuid4
from queue import Queue

empty_queue = Queue()


class CameraChannel:
    listeners: dict[str, Queue[bytes]] = {}

    def valid_listener(self, stream_id: str) -> bool:
        if stream_id not in self.listeners:
            return False
        return True

    def generate(self) -> str:
        stream_id = str(uuid4())
        self.listeners[stream_id] = empty_queue
        return stream_id

    def remove(self, stream_id: str) -> bool:
        if stream_id not in self.listeners:
            return False
        del self.listeners[stream_id]
        return True

    def register(self, stream_id: str, queue: Queue[bytes]) -> bool:
        if stream_id not in self.listeners:
            return False
        if self.listeners[stream_id] is not empty_queue:
            return False

        self.listeners[stream_id] = queue
        return True

    def broadcast(self, jpeg: bytes) -> bool:
        for queue in self.listeners.values():
            queue.put(jpeg)
        return True

    def send(self, stream_id: str, x):
        self.listeners[stream_id].put(x)


Command = Enum("Command", "UP RIGHT DOWN LEFT SWEEP_H SWEEP_V",
               module=__name__)


class ControlsChannel:
    queue: Queue[Command] = Queue(maxsize=10)
    current_key: str = ''

    def generate(self) -> str:
        uuid = str(uuid4())
        hash_code = sha256(uuid.encode('utf-8'))
        key = str(hash_code.hexdigest())
        self.current_key = key
        return key

    def check(self, key: str) -> bool:
        if self.current_key == '':
            return False
        if key == self.current_key:
            return True
        return False

    def reset(self) -> None:
        self.current_key = ''

    def send(self, cmd: Command) -> bool:
        return True

    def subscribe(self) -> bool:
        return True


Camera = CameraChannel()
Controls = ControlsChannel()
