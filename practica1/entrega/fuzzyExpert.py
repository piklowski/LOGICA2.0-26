'''
 Sistema Experto Difuso para el guiado de un robot
 Esta clase contendrá el código creado por los alumnos de RyRDC para el control 
 y guiado de un robot móvil sobre un plano cartesiano para recorrer diferentes 
 objetivos utilizando un esquema de sistema experto difuso

 Creado por: Diego Viejo
 el 24/10/2024
 Modificado por: Diego Viejo. 

'''

import numpy as np
import math

from fuzzy_expert.variable import FuzzyVariable
from fuzzy_expert.rule import FuzzyRule
from fuzzy_expert.inference import DecompositionalInference

from objetivo import *

class FuzzySystem:
    def __init__(self) -> None:
        self.objetivoActual = None
        #Completar definiendo las variables difusas y las reglas difusas del sistema experto.
        #Construcción del modelo difuso

        #variables del sistema.
        variables={

            #variables de entrada. 

            "error_angulo": FuzzyVariable(
                universe_range=(-math.pi, math.pi),
                terms={
                    "muy_desviado_izquierda":('zmf', -math.pi, -0.8),
                    "desviado_izquierda":('trimf',-1.2, -0.4, 0),
                    "recto":('trimf',-0.15, 0, 0.15),
                    "desviado_derecha":('trimf', 0, 0.4, 1.2),
                    "muy_desviado_derecha":('smf', 0.8, math.pi)                 
                }
            ),

            'distancia_objetivo': FuzzyVariable(
                universe_range=(0,20),
                terms={
                    'muy_lejos':('smf', 12, 20),
                    'lejos': ('trimf', 7.0, 12.0, 15.0),
                    'media_distancia': ('trimf', 3.0, 6.0, 10.0),
                    'cerca': ('trimf', 1.0, 3.0, 5.0),
                    'muy_cerca': ('zmf', 0.5, 2.0)
                }
            ),


            #variables de salida.

            'velocidad_lineal': FuzzyVariable(
                universe_range=(0,3),
                terms={
                    'poca_velocidad':('zmf',0,0.5),
                    'velocidad_media':('gaussmf', 1.5,  0.6), #media, desviacion tipica.
                    'mucha_velocidad':('smf',1.5,3)
                }
            ),

            'velocidad_angular': FuzzyVariable(
                universe_range=(-1,1),
                terms={
                    'giro_fuerte_izquierda':('zmf', -0.8, -0.2),
                    'giro_flojo_izquierda':('gaussmf', -0.5, 0.2),
                    'recto':('trimf', -0.2, 0, 0.2),
                    'giro_flojo_derecha':('gaussmf', 0.5, 0.2),
                    'giro_fuerte_derecha':('smf', 0.2, 0.8)
                }
            ),
        }

        #reglas del sistema. 
        reglas={

            #reglas de alineacion con el objetivo.


            #reglas de avance.



            #reglas del frenado.
        }




    # función setObjetivo
    #   Especifica un objetivo que debe ser recorrido por el robot
    def setObjetivo(self, obj):
        self.objetivoActual = obj

    def tomarDecision(self, poseRobot):
        V = W = 0
        #uso del modelo difuso para objeter V y W
        return (V, W)
    
