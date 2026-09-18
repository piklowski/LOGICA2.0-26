#ARCHIVO PARA TRABAJAR CON LA PRACTICA. 

from objetivo import *
import math

class ExpertSystem:
    def __init__(self) -> None:
        self.objetivoActual = None
        self.nombreAlumno = "Kacper Marcin Piklowski"

        #implementamos fase para saber en que fase del objetivo estamos y el umbral para saber si el objetivo esta alcanzado.
        self.umbral = 0.2
        self.fase = 1


    #============================================================================


    def setObjetivo(self, objetivo):
        self.objetivoActual = objetivo

    #============================================================================


    def tomarDecision(self, poseRobot):

        v_lineal=0.0
        v_angular=0.0
        
        '''
        obtenemos la posicion y el angulo actuales del robot.
        '''

        #obtenemos los datos del robot en el instante en el que vamos a tomar la decision. 
        x_robot = poseRobot[0]
        y_robot = poseRobot[1]
        angulo_robot = math.radians(poseRobot[2])

        #----------------------------------------------------------------------------------------

        '''
        obtenemos el tipo de objetivo con el que se enfrenta el robot. 
        '''

        if self.objetivoActual.getType() == 1 and self.fase==1:
            x_objetivo, y_objetivo = self.objetivoActual.getInicio()
        elif self.objetivoActual.getType() == 1 and self.fase==2:
            x_objetivo, y_objetivo = self.objetivoActual.getFin()

        #----------------------------------------------------------------------------------------

        '''
        calculamos la distancia que le falta al robot para saber que direccion debe tomar el robot.
        ''' 

        vector_distancia = (x_objetivo - x_robot,y_objetivo - y_robot)
        distancia = math.sqrt(vector_distancia[0]**2 + vector_distancia[1]**2)

        '''
        calculamos el angulo de referencia porque es angulo deseado que debe tomar el robot para alcanzar el objetivo. Es la direccion de la linea recta que conecta el robot y su objetivo.
        '''

        angulo_referencia = math.atan2(vector_distancia[1], vector_distancia[0])
            #usamos atan2 porque es una funcion matematica equivalente a arcotangente, pero calcula automaticamente en que cuadrante esta situado el objetivo y facilita situar el robot en la direccion correcta.

        '''
        calculamos el la diferencia de angulos para que el robot sepa como girarse para alcanzar el objetivo.
        '''

        dif_angulo = angulo_referencia - angulo_robot
        error_angulo = math.atan2(math.sin(dif_angulo), math.cos(dif_angulo))
        margen = 0.1

        #----------------------------------------------------------------------------------------

        #=========================
        #REGLAS DE ESTADO. 
        #=========================

        if distancia <= self.umbral:
            self.fase+=1

        if self.fase==2:
            return (0.0,0.0)


        #=========================
        #REGLAS DE CONTROL (VELOCIDADES). 
        #=========================
        
        if abs(error_angulo) < margen:
            v_lineal = 3.0
            v_angular = 0.0
            
        else:
            v_lineal = 0.0
            if error_angulo > 0:
                v_angular = 0.5
            else:
                v_angular = -0.5




        #tenemos que devolover la tupla con las velocidades que queremos que tome el robot. 
        return (v_lineal, v_angular)
        #return (1,0.5)