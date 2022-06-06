import numpy as np
from typing import Tuple, List
from kaggle_environments.envs.kore_fleets.helpers import Board
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


def get_kore_grid_by_turn(board: Board) -> np.ndarray:
    '''
    Devuelve una matriz 21x21 con la cantidad de core en cada celda
    '''
    kore_grid = np.flip(np.array(board.observation["kore"], dtype=np.float64).reshape(21, 21), axis=0)
    return kore_grid

def get_max_kore_coordinates(grid: np.ndarray) -> Tuple[int]:
    (x, y) = np.unravel_index(grid.argmax(), grid.shape)
    return (x, y)

def get_optimum_path_to_kore_coordinates(kore_grid: np.ndarray, shipyard_coordinates: Tuple[int], kore_coordinates: Tuple[int]) -> List[tuple]:
    """
    AStartFinder va del punto A al punto B por la ruta óptima que nosotros definiremos.
    Por defecto, irá por el camino con los valores >= 1 y nunca  pasará por celdas con
    valor < 1. Dará prioridad a aquellos valores más cercanos al 1: por eso se normalizan los valores
    del 1 al 10 y se invierten.

    EJEMPLO
    -------

    Para una matriz
        [1, 2, 2]
        [2, 0, 3]
        [1, 1, 1]

    Con nodos
        S = (0, 0)
        E = (2, 2)

    Hará el camino
        [S    ]
        [X #  ]
        [X X E]

    Donde
        S: punto de partida
        X: ruta tomada
        #: muro o bloqueo
        E: punto final

    Output
        [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]

    TODO:
        - Transformar el path de tuplas en una ruta de vuelo
    """
    lin_data = np.linalg.norm(kore_grid)
    norm_data = kore_grid / lin_data
    invertir = lambda t: 1 - t
    data_inverted = np.vectorize(invertir)(norm_data)
    weight = lambda n: n + 1
    data = np.vectorize(weight)(data_inverted).tolist()

    grid = Grid(matrix=data)

    sx, sy = shipyard_coordinates
    start = grid.node(sx, 20 - sy)

    ex, ey = kore_coordinates
    end = grid.node(ex, ey)

    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(start, end, grid)
    return path

def get_opposite_way(path: str) -> str:
    """
    Pensada para hacer un append al final del string del flight_plan para volver
    al shipyard.
    """
    opposite_path = ""
    for e, l in enumerate(path):
        if l == "N":
            digit = "S"
        elif l == "S":
            digit = "N"
        elif l == "W":
            digit = "E"
        elif l == "E":
            digit = "W"
        else:
            digit = l
        opposite_path += digit
    return opposite_path
