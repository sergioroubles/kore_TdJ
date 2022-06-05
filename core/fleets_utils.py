import numpy as np
from kaggle_environments.helpers import Point, Direction
from kaggle_environments.envs.kore_fleets.helpers import Board

def get_fleets_grid_by_turn(board: Board, get_enemy_fleet: bool = False) -> np.ndarray:
    '''
    Devuelve una matriz 21x21 con el número de naves de una flota aliada o enemiga en cada celda

    TODO:
        - Podemos devolver una tupla con más info (dirección, plan, de vuelo, kore, ...)
    '''
    player_index = 0
    if get_enemy_fleet:
        player_index = 1
    fleets = board.observation["players"][player_index][2]

    grid_size = 21
    fleets_grid = np.zeros((grid_size, grid_size), dtype=np.int32)
    for fleet in fleets:
        fleet_id = fleet
        fleet_index = fleets[fleet_id][0]
        fleet_kore = fleets[fleet_id][1]
        fleet_count = fleets[fleet_id][2]
        fleet_direction = Direction.from_index(fleets[fleet_id][3])
        flight_plan = fleets[fleet_id][4]

        (x, y) = Point.from_index(fleet_index, 21)
        fleets_grid[y, x] = fleet_count

    return fleets_grid