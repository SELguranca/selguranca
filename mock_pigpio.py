OUTPUT = 1
INPUT = 0


class PWM:

    def set_mode(self, pin, direction):
        pass

    def set_PWM_frequency(self, pin, freq):
        pass

    def set_PWM_dutycycle(self, pin, x):
        pass

    def set_servo_pulsewidth(self, pin, x):
        pass


def pi():
    return PWM()
