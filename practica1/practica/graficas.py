'''
 Dibuja las variables del sistema experto difuso (FuzzySystem de fuzzyExpert.py)
 representando el grado de pertenencia de cada termino.

 Uso:
    python dibujarVariables.py               -> abre una ventana con todas las variables
    python dibujarVariables.py --guardar     -> ademas guarda variables_difusas.png
    python dibujarVariables.py --separadas   -> ademas guarda una imagen por variable (variable_<nombre>.png)

 Las variables se leen directamente de FuzzySystem().variables, asi que si se cambian
 los valores en fuzzyExpert.py, basta con volver a ejecutar este programa.
'''

import sys
import math
import numpy as np
import matplotlib.pyplot as plt

from fuzzyExpert import FuzzySystem

#numero de puntos con los que se dibuja cada curva (rejilla fina para que se vean suaves).
PUNTOS = 2000

#informacion para los titulos y los ejes: nombre de la variable -> (titulo, unidad, tipo).
INFORMACION = {
    'error_angulo':      ('Error de ángulo',      'rad',   'entrada'),
    'distancia':         ('Distancia al objetivo', 'm',     'entrada'),
    'velocidad_lineal':  ('Velocidad lineal',     'm/s',   'salida'),
    'velocidad_angular': ('Velocidad angular',    'rad/s', 'salida'),
}

#variables con terminos muy estrechos: ademas de la grafica completa se dibuja una ampliada.
AMPLIACIONES = {
    'error_angulo': (-1.5, 1.5),
    'distancia': (0, 20)
}

#colores de los terminos (apto para daltonismo), se asignan en el orden en que estan definidos.
COLORES = ['#0072B2', '#E69F00', '#009E73', '#D55E00', '#CC79A7', '#56B4E9', '#F0E442', '#444444']


#====================================================================
#funciones de pertenencia (mismas definiciones que usa fuzzy_expert).

def zmf(x, a, b):
    y = np.zeros_like(x)
    medio = (a + b) / 2.0
    y[x <= a] = 1.0
    tramo1 = (x > a) & (x <= medio)
    y[tramo1] = 1.0 - 2.0 * ((x[tramo1] - a) / (b - a)) ** 2
    tramo2 = (x > medio) & (x < b)
    y[tramo2] = 2.0 * ((x[tramo2] - b) / (b - a)) ** 2
    return y


def smf(x, a, b):
    return 1.0 - zmf(x, a, b)


def trimf(x, a, b, c):
    y = np.zeros_like(x)
    if b > a:
        subida = (x > a) & (x < b)
        y[subida] = (x[subida] - a) / (b - a)
    if c > b:
        bajada = (x > b) & (x < c)
        y[bajada] = (c - x[bajada]) / (c - b)
    y[x == b] = 1.0
    return y


FUNCIONES = {'zmf': zmf, 'smf': smf, 'trimf': trimf}


#====================================================================

#calcula el grado de pertenencia de un termino sobre el universo.
def pertenencia(definicion, universo):
    #si la libreria ya guarda los valores calculados, los usamos tal cual.
    if isinstance(definicion, np.ndarray):
        return definicion

    tipo = definicion[0]
    parametros = definicion[1:]
    return FUNCIONES[tipo](universo, *parametros)


#dibuja una variable en el eje que se le pasa. Si se indican limites, se dibuja ampliada.
def dibujarVariable(eje, nombre, variable, limites=None):
    #rango del universo (fuzzy_expert lo guarda en min_u y max_u).
    minimo, maximo = variable.min_u, variable.max_u
    universo = np.linspace(minimo, maximo, PUNTOS)

    titulo, unidad, tipo = INFORMACION.get(nombre, (nombre, '', ''))

    for i, (termino, definicion) in enumerate(variable.terms.items()):
        color = COLORES[i % len(COLORES)]
        mu = pertenencia(definicion, universo)
        eje.fill_between(universo, mu, color=color, alpha=0.12)
        eje.plot(universo, mu, color=color, linewidth=2.2, label=termino)

    if limites is not None:
        minimo, maximo = limites
        titulo = titulo + ' (ampliada)'

    eje.set_title(f'{titulo}  [{tipo}]' if tipo else titulo, fontsize=12, fontweight='bold')
    eje.set_xlabel(f'{nombre} ({unidad})' if unidad else nombre)
    eje.set_ylabel('grado de pertenencia')
    eje.set_xlim(minimo, maximo)
    eje.set_ylim(-0.02, 1.08)
    eje.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    eje.grid(True, alpha=0.3)
    eje.axhline(0.5, color='gray', linewidth=0.8, linestyle=':')

    #el angulo tambien se muestra en grados en un eje superior.
    if nombre == 'error_angulo':
        eje_grados = eje.secondary_xaxis('top', functions=(np.degrees, np.radians))
        eje_grados.set_xlabel('grados', fontsize=9)

    #la leyenda va debajo de la grafica para no tapar las curvas.
    eje.legend(loc='upper center', bbox_to_anchor=(0.5, -0.22),
               ncol=min(len(variable.terms), 3), fontsize=9, frameon=False)


#====================================================================

if __name__ == '__main__':
    sistema = FuzzySystem()
    variables = sistema.variables

    plt.rcParams.update({'axes.spines.top': False, 'axes.spines.right': False})

    #lista de graficas: cada variable completa y, si tiene ampliacion, la ampliada a continuacion.
    graficas = []
    for nombre, variable in variables.items():
        graficas.append((nombre, variable, None))
        if nombre in AMPLIACIONES:
            graficas.append((nombre, variable, AMPLIACIONES[nombre]))

    filas = math.ceil(len(graficas) / 2)
    figura, ejes = plt.subplots(filas, 2, figsize=(14, 5.2 * filas))
    ejes = ejes.flatten()

    for eje, (nombre, variable, limites) in zip(ejes, graficas):
        dibujarVariable(eje, nombre, variable, limites)

    #si sobra algun hueco en la cuadricula, se oculta.
    for eje in ejes[len(graficas):]:
        eje.axis('off')

    figura.suptitle('Variables del sistema experto difuso: grados de pertenencia', fontsize=15, fontweight='bold')
    figura.tight_layout(rect=(0, 0, 1, 0.97), h_pad=3.0)

    if '--guardar' in sys.argv:
        figura.savefig('variables_difusas.png', dpi=150, bbox_inches='tight')
        print('Imagen guardada en variables_difusas.png')

    #una imagen por variable (completa y ampliada si la tiene).
    if '--separadas' in sys.argv:
        for nombre, variable in variables.items():
            columnas = 2 if nombre in AMPLIACIONES else 1
            fig, ejes_var = plt.subplots(1, columnas, figsize=(7 * columnas, 5.2), squeeze=False)
            dibujarVariable(ejes_var[0][0], nombre, variable)
            if nombre in AMPLIACIONES:
                dibujarVariable(ejes_var[0][1], nombre, variable, AMPLIACIONES[nombre])
            fig.tight_layout()
            fig.savefig(f'variable_{nombre}.png', dpi=150, bbox_inches='tight')
            print(f'Imagen guardada en variable_{nombre}.png')
            plt.close(fig)

    plt.show()