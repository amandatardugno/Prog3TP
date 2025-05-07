"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo. Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from time import time
from problem import OptProblem


class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)

        while True:

            # Buscamos la acción que genera el sucesor con mayor valor objetivo
            act, succ_val = problem.max_action(actual)

            # Retornar si estamos en un maximo local:
            # el valor objetivo del sucesor es menor o igual al del estado actual
            if succ_val <= value:

                self.tour = actual
                self.value = value
                end = time()
                self.time = end-start
                return

            # Sino, nos movemos al sucesor
            actual = problem.result(actual, act)
            value = succ_val
            self.niters += 1


class HillClimbingReset(LocalSearch):
    """Algoritmo de ascension de colinas con reinicio aleatorio."""

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas y reinicio aleatorio."""

        start = time()
        best_solution = None
        best_value = float('-inf')

        for _ in range(10):  #Aca indicamos la cantidad de reinicios
            actual = problem.random_reset()
            value = problem.obj_val(actual)

            while True:
                act, succ_val = problem.max_action(actual)

                if succ_val <= value:
                    break

                actual = problem.result(actual, act)
                value = succ_val
                self.niters += 1

            if value > best_value:
                best_solution = actual
                best_value = value

        self.tour = best_solution
        self.value = best_value
        self.time = time() - start


from collections import deque

class Tabu(LocalSearch):
    """Algoritmo de búsqueda tabú."""

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimización con búsqueda tabú."""

        start = time()
        actual = problem.init
        mejor = actual
        valor_mejor = problem.obj_val(mejor)

        tabu = deque([], maxlen=5)

        for _ in range(100):  #El criterio de parada es un nro fijo de iteraciones
            acciones = problem.actions(actual)
            mejor_accion = None
            mejor_valor = float('-inf')

            for accion in acciones:
                if accion not in tabu:
                    sucesor = problem.result(actual, accion)
                    val = problem.obj_val(sucesor)
                    if val > mejor_valor:
                        mejor_valor = val
                        mejor_accion = accion

            if mejor_accion is None:
                break

            sucesor = problem.result(actual, mejor_accion)
            tabu.append(mejor_accion)

            if problem.obj_val(sucesor) > valor_mejor:
                mejor = sucesor
                valor_mejor = problem.obj_val(sucesor)

            actual = sucesor
            self.niters += 1

        self.tour = mejor
        self.value = valor_mejor
        self.time = time() - start
