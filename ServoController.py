# antes derodar o código : sudo pigiod
import pigpio #sudo apt-get install python3-pigpio
import time

#Portas para os PWM de cada Servo
servo_H = 18
servo_V = 17

ang1=90
ang2=90

# more info at http://abyz.me.uk/rpi/pigpio/python.html#set_servo_pulsewidth

pwm = pigpio.pi() #Inicia biblioteca

#Define os Servos com Output
pwm.set_mode(servo_H, pigpio.OUTPUT)
pwm.set_PWM_frequency( servo_H, 50 )
pwm.set_mode(servo_V, pigpio.OUTPUT)
pwm.set_PWM_frequency( servo_V, 50 )

#Retorna o valor em segundos da rotacao em graus desejada
def func(x): 
    return ((2500-500)/(180-0))*x+500 #Funcao de primeiro grau

# Posiciona os servos em um angulo fixo dado na entrada da função
def Angulo(angulo_H=0,angulo_V=0,slp=1):
       
       if (float(angulo_H)<0 or float(angulo_H)>180) or (float(angulo_V)<0 or float(angulo_V)>180):
           #Desliga os Servos
           pwm.set_PWM_dutycycle(servo_H, 0)
           pwm.set_PWM_frequency(servo_H, 0)
           pwm.set_PWM_dutycycle(servo_V, 0)
           pwm.set_PWM_frequency(servo_V, 0)
           return "ERROR: Angulo fora de faixa [0,180]"
       else:
           pwm.set_servo_pulsewidth( servo_H, func(float(angulo_H))) ;
           pwm.set_servo_pulsewidth( servo_V, func(float(angulo_V))) ;
           time.sleep( slp )


# Incrementa ou decrementa a posição do servo

def controle(x):
    global ang1, ang2
    ang1, ang2 = Controle_manua(x, ang1, ang2)

def Controle_manua(dir, ang1, ang2):
    step=10
    if (dir == "E"):
        ang1=ang1+step
        Angulo(ang1, ang2, 0.5)
    elif (dir == "D"):
        ang1=ang1-step
        Angulo(ang1, ang2, 0.5)
    elif (dir == "B"):
        ang2=ang2+step
        Angulo(ang1, ang2, 0.5)
    elif (dir == "C"):
        ang2=ang2-step
        Angulo(ang1, ang2, 0.5)
    elif (dir == "H"):
        for i in range(70,150):
            Angulo(i,90,0.05)
        for i in range(150,70,-1):
            Angulo(i,90,0.05)    
    elif(dir == "V"): # Servo Vertical
        for i in range(80,140):
            Angulo(90,i,0.05)
            ang2 = 90
            ang1 = 90
        for i in range(140,90,-1):
            Angulo(90,i,0.05)
            ang2 = 90
            ang1 = 90
    else:
        print("error")
    time.sleep(0.5)
    print(ang1, ang2)
    return(ang1, ang2)

# Varre de 0 a 180
def Varredura(servo): 
    if(servo == "H"): #Servo Horizontal
        for i in range(70,150):
            Angulo(i,90,0.05)
        for i in range(150,70,-1):
            Angulo(i,90,0.05)    
    elif(servo == "V"): # Servo Vertical
        for i in range(80,140):
            Angulo(90,i,0.05)
        for i in range(140,90,-1):
            Angulo(90,i,0.05)

# MAIN
#valores iniciais dos angulos:

#Varredura("H")
#Varredura("V")
#ang1, ang2= Controle_manua ("E", ang1, ang2)
#ang1, ang2= Controle_manua ("D", ang1, ang2)
#ang1, ang2= Controle_manua ("C", ang1, ang2)
#ang1, ang2= Controle_manua ("B", ang1, ang2)
print("ok")
