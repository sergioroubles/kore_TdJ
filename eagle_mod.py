
from random import random, sample, randint
import numpy as np

from kaggle_environments import utils
from kaggle_environments.helpers import Point, Direction
from kaggle_environments.envs.kore_fleets.helpers import Board, ShipyardAction

def get_kore_density(board, distance=2):
    # Find row and column window sizes
    size = board.configuration.size
    np_kore = np.array(board.observation["kore"]).reshape((size,size))
    x, y = np_kore.shape
    in_array = np_kore.copy().repeat(3, axis=0).repeat(3, axis=1)
    res = np_kore.copy()
    for i in range(x):
        xmin = x + (i-distance)
        xmax = x + (i+distance)
        for j in range(y):
            ymin = y + (j-distance)
            ymax = y + (j+distance)
            res[i, j] = in_array[xmin:xmax, ymin:ymax].sum() - np_kore[i, j]
    return res

def get_distance_to_closest_shipyards(board, me):
    size = board.configuration.size
    enemy_shipyards = np.full((size, size), size*100)
    allied_shipyards = np.full((size, size), size*100)
    for shipyard in board.shipyards.values():
        if shipyard.player_id == me.id:
            array = allied_shipyards
        else:
            array = enemy_shipyards
            
        for i in range(size):
            for j in range (size):
                dist = shipyard.position.distance_to(Point(i,j), size)
                array[i, j] = min(array[i, j], dist)
    return enemy_shipyards, allied_shipyards

def get_distances_to_position(position, size):
    distances = np.full((size, size), size*100)            
    for i in range(size):
        for j in range (size):
            dist = position.distance_to(Point(i,j), size)
            distances[i, j] = min(distances[i, j], dist)
    return distances

def get_shortest_flight_path_between(position_a, position_b, size, trailing_digits=False):
    mag_x = 1 if position_b.x > position_a.x else -1
    abs_x = abs(position_b.x - position_a.x)
    dir_x = mag_x if abs_x < size/2 else -mag_x
    mag_y = 1 if position_b.y > position_a.y else -1
    abs_y = abs(position_b.y - position_a.y)
    dir_y = mag_y if abs_y < size/2 else -mag_y
    flight_path_x = ""
    if abs_x > 0:
        flight_path_x += "E" if dir_x == 1 else "W"
        flight_path_x += str(abs_x - 1) if (abs_x - 1) > 0 else ""
    flight_path_y = ""
    if abs_y > 0:
        flight_path_y += "N" if dir_y == 1 else "S"
        flight_path_y += str(abs_y - 1) if (abs_y - 1) > 0 else ""
    if not len(flight_path_x) == len(flight_path_y):
        if len(flight_path_x) < len(flight_path_y):
            return flight_path_x + (flight_path_y if trailing_digits else flight_path_y[0])
        else:
            return flight_path_y + (flight_path_x if trailing_digits else flight_path_x[0])
    return flight_path_y + (flight_path_x if trailing_digits or not flight_path_x else flight_path_x[0]) if random() < .5 else flight_path_x + (flight_path_y if trailing_digits or not flight_path_y else flight_path_y[0])

def find_best_shipyard_location(shipyard, board, me):
    kore_density = get_kore_density(board)
    dist_enemy_shipyards, dist_allied_shipyards = get_distance_to_closest_shipyards(board, me)
    distance_to_shipyard = get_distances_to_position(shipyard.position, board.configuration.size)
    
    # We should explore near the current shipyard
    shipyard_is_close = distance_to_shipyard < dist_allied_shipyards*2

    # Allowed spots shoulb be safe and far from allied shipyards
    safe_locations = dist_enemy_shipyards + 1 >= dist_allied_shipyards
    not_next_locations = dist_allied_shipyards > 3
    spots = safe_locations & not_next_locations & shipyard_is_close

    # Some bonus should be granted based on distance to enforce expansion
    farthest_location = (spots * dist_allied_shipyards).max()
    richest_location = (spots * kore_density).max()
    distance_bonus = (richest_location * dist_allied_shipyards / farthest_location)

    value = spots * kore_density + distance_bonus
    best_location = np.unravel_index(np.argmax(value, axis=None), value.shape)
    return Point(*best_location)
    
def miner_agent(obs, config):
    board = Board(obs, config)
    me = board.current_player
    remaining_kore = me.kore
    shipyards = me.shipyards
    convert_cost = board.configuration.convert_cost
    spawn_cost = board.configuration.spawn_cost
    # randomize shipyard order
    shipyards = sample(shipyards, len(shipyards))
    for shipyard in shipyards:
        # if we have over 1k kore and our max spawn is > 5 (we've held this shipyard for a while)
        # create a fleet to build a new shipyard!
        if remaining_kore > 1000 and shipyard.max_spawn > 5:
            if shipyard.ship_count >= convert_cost + 10:
                best_location = find_best_shipyard_location(shipyard, board, me)
                flight_plan = get_shortest_flight_path_between(shipyard.position, best_location, board.configuration.size, trailing_digits=True)
                flight_plan += "C"
                shipyard.next_action = ShipyardAction.launch_fleet_with_flight_plan(max(convert_cost + 10, int(shipyard.ship_count/2)), flight_plan)
            elif remaining_kore >= spawn_cost:
                shipyard.next_action = ShipyardAction.spawn_ships(min(shipyard.max_spawn, int(remaining_kore/spawn_cost)))

        # launch a large fleet if able
        elif shipyard.ship_count >= 21:
            gap1 = str(randint(3, 9))
            gap2 = str(randint(3, 9))
            start_dir = randint(0, 3)
            flight_plan = Direction.list_directions()[start_dir].to_char() + gap1
            next_dir = (start_dir + 1) % 4
            flight_plan += Direction.list_directions()[next_dir].to_char() + gap2
            next_dir = (next_dir + 1) % 4
            flight_plan += Direction.list_directions()[next_dir].to_char() + gap1
            next_dir = (next_dir + 1) % 4
            flight_plan += Direction.list_directions()[next_dir].to_char()
            shipyard.next_action = ShipyardAction.launch_fleet_with_flight_plan(21, flight_plan)
    
        # else spawn if possible
        elif remaining_kore > board.configuration.spawn_cost * shipyard.max_spawn:
            remaining_kore -= board.configuration.spawn_cost
            if remaining_kore >= spawn_cost:
                shipyard.next_action = ShipyardAction.spawn_ships(min(shipyard.max_spawn, int(remaining_kore/spawn_cost)))
        # else launch a small fleet
        elif shipyard.ship_count >= 5:
            dir_str = Direction.random_direction().to_char()
            shipyard.next_action = ShipyardAction.launch_fleet_with_flight_plan(2, dir_str)
            
    return me.next_actions
