#ARCHIVO PARA TRABAJAR CON LA PRACTICA. 

from objetivo import *
import math

class ExpertSystem:
    def __init__(self) -> None:
        self.objetivoActual = None
        self.nombreAlumno = "Kacper Marcin Piklowski"

        #implementamos fase para saber en que fase del objetivo estamos y el umbral para saber si el objetivo esta alcanzado.
        self.umbral = 0.2
        self.cola_puntos=[]


    #============================================================================

    #============================================================================


    def setObjetivo(self, objetivo):
        self.objetivoActual = objetivo
        self.lista_puntos = []

        #para el tramo recto, calculamos el inicio y el final y lo anadimo a la lista del puntos. 
        if self.objetivoActual.getType()==1:
            self.lista_puntos.append(objetivo.getInicio())
            self.lista_puntos.append(objetivo.getFin())

        else:
            #para el tramo triangular, calculamos los puntos del inicio, final y del obstaculo para evitarlo. 
            inicio = objetivo.getInicio()
            medio = objetivo.getMedio()
            fin = objetivo.getFin()

            #calculo del punto medio de la recta que une el inicio y el final. 
            punto_medio= ((inicio[0] + fin[0]) /2.0, (inicio[1] + fin[1]) /2.0)

            #la linea que une el punto medio y el punto de obstaculo para saber donde esta situado. 
            vector_medio= (medio[0]-punto_medio[0], medio[1]-punto_medio[1])
            distancia_medio = math.sqrt(vector_medio[0]**2 + vector_medio[1]**2) #distancia euclidea.

            margen_seguridad = 0.8

            #obtenemos la direccion exacta del punto medio normalizando el vector, y al multiplicarlo por el margen, creamos un nuevo vector que mide exactamente lo que mide margen de seguridad.
            punto_rodear = (medio[0]+(vector_medio[0]/distancia_medio)*margen_seguridad, medio[1]+(vector_medio[1]/distancia_medio)* margen_seguridad)

            #guardamos todos los puntos en la lista de puntos. 
            self.lista_puntos.append(inicio)
            self.lista_puntos.append(punto_rodear)
            self.lista_puntos.append(fin)


    #============================================================================


    def tomarDecision(self, poseRobot):

        if not hasattr(self, 'lista_puntos') or not self.lista_puntos:
            return (0.0, 0.0)

        #obtenemos los datos del robot en el instante en el que vamos a tomar la decision. 
        x_robot = poseRobot[0]
        y_robot = poseRobot[1]
        angulo_robot = math.radians(poseRobot[2])


        #obtenemos las coordenadas del objetivo actual. 
        x_objetivo, y_objetivo = self.lista_puntos[0]


        #calculamos la distancia que le falta al robot para saber que direccion debe tomar el robot.
        vector_distancia = (x_objetivo - x_robot,y_objetivo - y_robot)
        distancia = math.sqrt(vector_distancia[0]**2 + vector_distancia[1]**2)


        #calculamos el angulo de referencia porque es angulo deseado que debe tomar el robot para alcanzar el objetivo. Es la direccion de la linea recta que conecta el robot y su objetivo.
        angulo_referencia = math.atan2(vector_distancia[1], vector_distancia[0])
            #usamos atan2 porque es una funcion matematica equivalente a arcotangente, pero calcula automaticamente en que cuadrante esta situado el objetivo y facilita situar el robot en la direccion correcta.


        #calculamos el la diferencia de angulos para que el robot sepa como girarse para alcanzar el objetivo.
        dif_angulo = angulo_referencia - angulo_robot
        error_angulo = math.atan2(math.sin(dif_angulo), math.cos(dif_angulo))


        #=========================
        #REGLAS DE ESTADO. 
        #=========================

        if distancia < self.umbral:
            self.lista_puntos.pop(0)
            return (0.0, 0.0) #POR AHORA RETURN PORQUE EL OBJETIVO ES QUE SE PARE. 


        #=========================
        #REGLAS DE CONTROL (VELOCIDADES). 
        #=========================
        
        if abs(error_angulo) < 0.05:
            v_lineal = 3.0
            v_angular=0.0
            

        elif abs(error_angulo) < 0.15:
            v_lineal = 2.5

            if error_angulo > 0:
                v_angular = 0.1
            else:
                v_angular = -0.1

        elif abs(error_angulo) < 0.20:
            v_lineal = 2.0

            if error_angulo > 0:
                v_angular = 0.15
            else:
                v_angular = -0.15

        elif abs(error_angulo) < 0.25:
            v_lineal = 0.5

            if error_angulo > 0:
                v_angular = 0.3
            else:
                v_angular = -0.3

        else:
            v_lineal = 0.0
            if error_angulo > 0:
                v_angular = 0.5
            else:
                v_angular = -0.5

        #=========================
        #FRENO CUANDO APROXIMADO   
        #=========================

        if distancia < self.umbral * 10:
            v_lineal = min(v_lineal, 1.8)

        if distancia < self.umbral * 7:
            v_lineal = min(v_lineal, 1.2)

        if distancia < self.umbral * 5:
            v_lineal = min(v_lineal, 0.9)

        if distancia < self.umbral * 2:
            v_lineal = min(v_lineal, 0.2)


        #tenemos que devolover la tupla con las velocidades que queremos que tome el robot. 
        return (v_lineal, v_angular)
        #return (1,0.5)