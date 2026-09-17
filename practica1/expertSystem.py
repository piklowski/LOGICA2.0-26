#ARCHIVO PARA TRABAJAR CON LA PRACTICA. 

from objetivo import *

class ExpertSystem:
    def __init__(self) -> None:
        self.objetivoActual = None
        self.nombreAlumno = "Kacper Marcin Piklowski"

    #=====================================================

    '''
    Este metodo se puede modificar incluyendo cualquier cambio que se considere conveniente.
    '''

    def setObjetivo(self, objetivo):
        self.objetivoActual = objetivo

    #=====================================================

    '''
    Este es el metodo que principalmente se tienen que crear las reglas. 
    '''

    def tomarDecision(self, poseRobot):

        '''
        Obtenemos las coordenadas actuales del robot a base de poseRobot que viene dada como parametro.
        '''

        x_robot = poseRobot[0]
        y_robot = poseRobot[1]
        angulo_robot = poseRobot[2]

        '''
        Tenemos que ver que tipo de objetivo es (segmento/triangulo). Segun el archivo objetivo.py, vemos que podemos saber que tipo es usando el metodo especifico para ello. 
        '''



        '''
        Se tiene que devolver una tupla que tenga (velocidad lineal, velocidad angular).
        '''

        return (3, 0.25)
    

