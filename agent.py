import json
from kaggle_environments.envs.kore_fleets.helpers import *
from core.kore_utils import get_kore_grid_by_turn, get_opposite_way, get_max_kore_coordinates, \
    get_optimum_path_to_kore_coordinates
from kaggle_environments.helpers import Point, Direction, Configuration, Observation


def agent(obs, config):
    board = Board(obs, config)
    me = board.current_player

    turn = board.step
    spawn_cost = board.configuration.spawn_cost
    shipyards = me.shipyards
    kore_left = me.kore
    kore_grid = get_kore_grid_by_turn(board=board)

    for shipyard in shipyards:

        max_kore_coordinates = get_max_kore_coordinates(kore_grid)
        path = get_optimum_path_to_kore_coordinates(kore_grid=kore_grid, shipyard_coordinates=shipyard.position,
                                                    kore_coordinates=max_kore_coordinates)

        k = kore_left - (spawn_cost * shipyard.max_spawn)
        action = None
        if shipyard.ship_count > 20:
            direction = Direction.from_index(turn % 4)
            action = ShipyardAction.launch_fleet_with_flight_plan(21, "S4E4W4N")

        elif k != 0 and kore_left > spawn_cost * shipyard.max_spawn:
            action = ShipyardAction.spawn_ships(shipyard.max_spawn)
            kore_left -= spawn_cost * shipyard.max_spawn

        elif kore_left > spawn_cost:
            action = ShipyardAction.spawn_ships(1)
            kore_left -= spawn_cost

        shipyard.next_action = action

    return me.next_actions


