from Message import Command
from ServoMotor import Servomotor
from enum import Enum

# phi:      Horizontal Motion Motor
# theta:    Vertical Motion Motor
Angles = Enum("MotorIndex", "PHI THETA", module=__name__)


class Controller:

    motors: dict[Angles, Servomotor]

    def __init__(self, vertical: Servomotor, horizontal: Servomotor) -> None:
        self.motors[Angles.THETA] = vertical
        self.motors[Angles.PHI] = horizontal

    def consume(self, command: Command) -> bool:
        return False

    def reset(self) -> bool:
        return False
