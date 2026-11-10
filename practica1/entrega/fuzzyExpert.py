'''
 Sistema Experto Difuso para el guiado de un robot
 Esta clase contendrá el código creado por los alumnos de RyRDC para el control
 y guiado de un robot móvil sobre un plano cartesiano para recorrer diferentes
 objetivos utilizando un esquema de sistema experto difuso

 Creado por: Diego Viejo
 el 24/10/2024
 Modificado por: Diego Viejo.

'''

#================================
#KACPER PIKLOWSKI - Y8458068Q
#================================

import numpy as np
import matplotlib.pyplot as plt
import math

from fuzzy_expert.variable import FuzzyVariable
from fuzzy_expert.rule import FuzzyRule
from fuzzy_expert.inference import DecompositionalInference

from objetivo import *

class FuzzySystem:
    def __init__(self) -> None:
        self.objetivoActual = None
        self.umbral = 0.28
        self.lista_puntos=[]


        #variables del sistema.
        self.variables={

            #variables de entrada.
            "error_angulo": FuzzyVariable(
                universe_range=(-math.pi, math.pi),
                terms={
                    "muy_derecha":('zmf', -1.0, -0.4),
                    "derecha":('trimf', -1.0, -0.4, 0.0),
                    "recto":('trimf', -0.4, 0.0, 0.4),
                    "izquierda":('trimf', 0.0, 0.4, 1.0),
                    "muy_izquierda":('smf', 0.4, 1.0),
                }
            ),


            'distancia': FuzzyVariable(
                universe_range=(0,100),
                terms={
                    'muy_cerca':('zmf', 0.6, 1.7),
                    'cerca':('zmf', 1.3, 3.33),
                    'media':('trimf', 2.64, 20.8, 26),
                    'lejos':('smf', 11.9, 33.0)
                }
            ),

            #variables de salida
            'velocidad_lineal': FuzzyVariable(
                universe_range=(0,3),
                terms={
                    'poca':('zmf', 0.09, 2.35),
                    'media':('trimf', 1.34, 2.2, 2.9),
                    'mucha':('smf', 2.95, 3.0)
                }
            ),

            'velocidad_angular': FuzzyVariable(
                universe_range=(-1,1),
                terms={
                    'giro_fuerte_derecha':('zmf', -0.8, -0.28),
                    'giro_flojo_derecha':('trimf', -1.0, -0.8, 0.0),
                    'recto':('trimf', -0.09, 0.0, 0.09),
                    'giro_flojo_izquierda':('trimf', 0.0, 0.8, 1.0),
                    'giro_fuerte_izquierda':('smf', 0.28, 0.8)
                }
            ),
        }

        #reglas del sistema.
        self.reglas=[

            #reglas de velocidad angular.
            FuzzyRule(
                premise=[('error_angulo', 'muy_derecha')],
                consequence=[('velocidad_angular', 'giro_fuerte_derecha')]),

            FuzzyRule(
                premise=[('error_angulo', 'derecha')],
                consequence=[('velocidad_angular', 'giro_flojo_derecha')]),

            FuzzyRule(
                premise=[('error_angulo', 'recto')],
                consequence=[('velocidad_angular', 'recto')]),

            FuzzyRule(
                premise=[('error_angulo', 'izquierda')],
                consequence=[('velocidad_angular', 'giro_flojo_izquierda')]),

            FuzzyRule(
                premise=[('error_angulo', 'muy_izquierda')],
                consequence=[('velocidad_angular', 'giro_fuerte_izquierda')]),


            #mucha velocidad lineal.
            FuzzyRule(
                premise=[('error_angulo', 'recto'), ('AND', 'distancia', 'lejos')],
                consequence=[('velocidad_lineal', 'mucha')]),

            FuzzyRule(
                premise=[('error_angulo', 'recto'), ('AND', 'distancia', 'media')],
                consequence=[('velocidad_lineal', 'mucha')]),

            FuzzyRule(
                premise=[('error_angulo', 'recto'), ('AND', 'distancia', 'cerca')],
                consequence=[('velocidad_lineal', 'media')]),

            FuzzyRule(
                premise=[('error_angulo', 'recto'), ('AND', 'distancia', 'muy_cerca')],
                consequence=[('velocidad_lineal', 'poca')]),


            #poca velocidad lineal
            FuzzyRule(
                premise=[('error_angulo', 'muy_derecha')],
                consequence=[('velocidad_lineal', 'poca')]),

            FuzzyRule(
                premise=[('error_angulo', 'derecha')],
                consequence=[('velocidad_lineal', 'poca')]),

            FuzzyRule(
                premise=[('error_angulo', 'izquierda')],
                consequence=[('velocidad_lineal', 'poca')]),

            FuzzyRule(
                premise=[('error_angulo', 'muy_izquierda')],
                consequence=[('velocidad_lineal', 'poca')]),
        ]

        #motor de inferencia.
        self.motor_inferencia = DecompositionalInference(
            and_operator="min",
            or_operator="max",
            implication_operator="Rc",
            composition_operator="max-min",
            production_link="max",
            defuzzification_operator="cog",
        )


#====================================================================


    #funcion set objetivo.
    def setObjetivo(self, obj):
        self.objetivoActual = obj
        self.lista_puntos = []

        if self.objetivoActual.getType()==1:
            self.lista_puntos.append(obj.getInicio())
            self.lista_puntos.append(obj.getFin())

        else:
            inicio=obj.getInicio()
            medio=obj.getMedio()
            fin= obj.getFin()

            punto_medio= ((inicio[0] + fin[0]) /2.0, (inicio[1] + fin[1]) /2.0)
            vector_medio= (medio[0]-punto_medio[0], medio[1]-punto_medio[1])
            distancia_medio = math.sqrt(vector_medio[0]**2 + vector_medio[1]**2)

            margen_seguridad = 0.6

            punto_rodear = (medio[0]+(vector_medio[0]/distancia_medio)*margen_seguridad, medio[1]+(vector_medio[1]/distancia_medio)* margen_seguridad)

            self.lista_puntos.append(inicio)
            self.lista_puntos.append(punto_rodear)
            self.lista_puntos.append(fin)


#====================================================================


    def tomarDecision(self, poseRobot):
        V = W = 0

        if not hasattr(self, 'lista_puntos') or not self.lista_puntos:
            return (0.0, 0.0)

        x_robot = poseRobot[0]
        y_robot = poseRobot[1]
        angulo_robot = math.radians(poseRobot[2])


        x_objetivo, y_objetivo = self.lista_puntos[0]
        vector_distancia = (x_objetivo - x_robot,y_objetivo - y_robot)
        distancia = math.sqrt(vector_distancia[0]**2 + vector_distancia[1]**2)


        if distancia < self.umbral:
            self.lista_puntos.pop(0)

            if not self.lista_puntos:
                return (0.0, 0.0)

            x_objetivo, y_objetivo = self.lista_puntos[0]
            vector_distancia = (x_objetivo - x_robot, y_objetivo - y_robot)
            distancia = math.sqrt(vector_distancia[0]**2 + vector_distancia[1]**2)

        angulo_referencia = math.atan2(vector_distancia[1], vector_distancia[0])
        dif_angulo = angulo_referencia - angulo_robot
        error_angulo = math.atan2(math.sin(dif_angulo), math.cos(dif_angulo))


        #ejecutamos el sistema difuso:
        resultado, _ = self.motor_inferencia(
            variables=self.variables,
            rules=self.reglas,
            error_angulo=error_angulo,
            distancia=distancia
        )

        V=resultado.get('velocidad_lineal',0.0)
        W=resultado.get('velocidad_angular',0.0)

        return (V, W)

