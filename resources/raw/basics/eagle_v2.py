# from https://github.com/Kaggle/kaggle-environments/blob/master/kaggle_environments/envs/kore_fleets/starter_bots/python/main.py
   
from kaggle_environments.envs.kore_fleets.helpers import *
from random import randint

def get_closest_enemy_shipyard(board, position, me):
    min_dist = 1000000
    enemy_shipyard = None
    for shipyard in board.shipyards.values():
        if shipyard.player_id == me.id:
            continue
        dist = position.distance_to(shipyard.position, board.configuration.size)
        if dist < min_dist:
            min_dist = dist
            enemy_shipyard = shipyard
    return enemy_shipyard

def build_flight_plan(dir_idx, size):
    flight_plan = ""
    for i in range(4):
        flight_plan += Direction.from_index((dir_idx + i) % 4).to_char()
        if not i == 3:
            flight_plan += str(size)
    return flight_plan

def agent(obs, config):
    board = Board(obs, config)
    me=board.current_player

    me = board.current_player
    turn = board.step
    spawn_cost = board.configuration.spawn_cost
    kore_left = me.kore
    spawn_cost = board.configuration.spawn_cost
    convert_cost = board.configuration.convert_cost

    for shipyard in me.shipyards:
        action = None
        if turn % 100 < 20 and shipyard.ship_count >= 100:
            closest_enemy_shipyard = get_closest_enemy_shipyard(board, shipyard.position, me)
            if not closest_enemy_shipyard:
                continue
            enemy_pos = closest_enemy_shipyard.position
            my_pos = shipyard.position
            flight_plan = "N" if enemy_pos.y > my_pos.y else "S"
            flight_plan += str(abs(enemy_pos.y - my_pos.y) - 1)
            flight_plan += "W" if enemy_pos.x < my_pos.x else "E"
            action = ShipyardAction.launch_fleet_with_flight_plan(shipyard.ship_count, flight_plan)  
        elif kore_left >= 200 & shipyard.ship_count > 100:
            flight_plan = build_flight_plan(randint(0, 3), randint(10, 15))
            flight_plan = flight_plan[:6] + "C"
            action = ShipyardAction.launch_fleet_with_flight_plan(convert_cost, flight_plan)
        elif  shipyard.ship_count > 40:
            flight_plan = build_flight_plan(randint(0, 3), randint(2, 8))
            action = ShipyardAction.launch_fleet_with_flight_plan(22, flight_plan)
        elif kore_left > spawn_cost * shipyard.max_spawn:
            action = ShipyardAction.spawn_ships(shipyard.max_spawn)
            kore_left -= spawn_cost * shipyard.max_spawn
        elif kore_left > spawn_cost:
            action = ShipyardAction.spawn_ships(1)
            kore_left -= spawn_cost

        shipyard.next_action = action

    return me.next_actions
