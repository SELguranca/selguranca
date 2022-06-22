#Servomotor

# antes derodar o código : sudo pigpiod
# more info at http://abyz.me.uk/rpi/pigpio/python.html#set_servo_pulsewidth


from mailbox import MH
from statistics import mode
import pigpio #sudo apt-get install python3-pigpio
import time

#Definição das portas p/ Servomotores
servo_H = 18
servo_V = 17

pwm = pigpio.pi() #Inicia biblioteca

#Define os Servos com Output
pwm.set_mode(servo_H, pigpio.OUTPUT)
pwm.set_PWM_frequency( servo_H, 50 )
pwm.set_mode(servo_V, pigpio.OUTPUT)
pwm.set_PWM_frequency( servo_V, 50 )

#Retorna o valor em segundos da rotacao em graus desejada
def func(x): 
    return ((2500-500)/(180-0))*x+500 #Funcao de primeiro grau

class Servomotor:
    def __init__(self, pin, angle, lim_inf, lim_sup):
        self.pin = pin
        self.angle = angle
        self.lim_inf = lim_inf
        self.lim_sup = lim_sup

    # Mode Angulo: Posiciona os Servomotores em dado ângulo.
    def angulo(self, x):
        
        if (float(x)< self.lim_inf or float(x)> self.lim_sup):
            #Desliga os Servos
            pwm.set_PWM_dutycycle(self.pin, 0)
            pwm.set_PWM_frequency(self.pin, 0)
            return "ERROR: Angulo fora de faixa [0,180]"
        else:
            pwm.set_servo_pulsewidth(self.pin, func(float(x))) ;
            self.angle= x
            time.sleep(0.05)
        return self.angle

    def controle(self, dir):
        if (dir == "+"):
            self.angle = self.angle + 10
            self.angulo(self.angle)
        elif (dir == "-"):
            self.angle = self.angle - 10
            self.angulo(self.angle)
        time.sleep(0.5)
        return self.angle

    # Varre de 0 a 180
    def Varredura(self): 
        self.angulo(self.lim_inf) # varredurra no intervalo [70, 150]
        for i in range(self.lim_inf, self.lim_sup):
            self.angulo(i)
        for i in range(self.lim_sup, self.lim_inf, -1):
            self.angulo(i)  
        return self.angle 

# MAIN
#valores iniciais dos angulos:
# (pin, angle, lim_inf, lim_sup)
mH = Servomotor (18, 90, 70, 150)
mV = Servomotor (17, 90, 80, 140)

# Se posicionar no ângulo x=110
mV.angulo((mV.lim_sup - mV.lim_sup)/2)
mH.angulo((mH.lim_sup - mH.lim_sup)/2)

# Conrtrole manual (+/-)
# mV.controle("+")
# mV.controle("-")

# # Varredura Automática
# mV.Varredura()
# mH.Varredura()
print("ok")
