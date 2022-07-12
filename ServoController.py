from Message import Command
from ServoMotor import Servomotor
from enum import Enum

# phi:      Horizontal Motion Motor
# theta:    Vertical Motion Motor
Angles = Enum("MotorIndex", "PHI THETA", module=__name__)


class Controller:

    motors: dict[Angles, Servomotor] = {}

    def __init__(self, vertical: Servomotor, horizontal: Servomotor) -> None:
        self.motors[Angles.THETA] = vertical
        self.motors[Angles.PHI] = horizontal

    def consume(self, command: Command) -> tuple[bool, float, float]:
        if command == Command.SWEEP_V:
            self.motors[Angles.THETA].varredura()
        elif command == Command.SWEEP_H:
            self.motors[Angles.PHI].varredura()
        elif command == Command.UP:
            self.motors[Angles.THETA].controle("+")
        elif command == Command.DOWN:
            self.motors[Angles.THETA].controle("-")
        elif command == Command.LEFT:
            self.motors[Angles.PHI].controle("+")
        elif command == Command.RIGHT:
            self.motors[Angles.PHI].controle("-")
        else:
            print(f"Unknown Command: {str(command)}")
            return (False, -1, -1)
        x = self.motors[Angles.PHI].angle
        y = self.motors[Angles.THETA].angle
        return (True, x, y)

    def reset(self) -> bool:
        self.motors[Angles.THETA].angulo(0)
        self.motors[Angles.PHI].angulo(0)
        return True
