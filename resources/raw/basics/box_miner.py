   
from kaggle_environments.envs.kore_fleets.helpers import *
from random import randint

def agent(obs, config):
    board = Board(obs, config)
    me=board.current_player

    me = board.current_player
    turn = board.step
    spawn_cost = board.configuration.spawn_cost
    kore_left = me.kore

    period = 40
    
    for shipyard in me.shipyards:
        action = None
        if turn < 40:
            action = ShipyardAction.spawn_ships(1)
        elif turn % period == 1:
            action = ShipyardAction.launch_fleet_with_flight_plan(21, "E9N9W9S")
        elif turn % period == 3: 
            action = ShipyardAction.launch_fleet_with_flight_plan(3, "E8N")
        elif turn % period == 5: 
            action = ShipyardAction.launch_fleet_with_flight_plan(3, "E7N")
        elif turn % period == 7: 
            action = ShipyardAction.launch_fleet_with_flight_plan(3, "E6N")
        elif turn % period == 9: 
            action = ShipyardAction.launch_fleet_with_flight_plan(3, "E5N")
        elif turn % period == 11: 
            action = ShipyardAction.launch_fleet_with_flight_plan(3, "E4N")
        elif turn % period == 13: 
            action = ShipyardAction.launch_fleet_with_flight_plan(3, "E3N")
        elif turn % period == 15: 
            action = ShipyardAction.launch_fleet_with_flight_plan(3, "E2N")
        elif turn % period == 17: 
            action = ShipyardAction.launch_fleet_with_flight_plan(3, "E1N")
        elif turn % period == 19: 
            action = ShipyardAction.launch_fleet_with_flight_plan(2, "EN")
        elif turn % period == 21: 
            action = ShipyardAction.launch_fleet_with_flight_plan(2, "N")
        elif kore_left >= spawn_cost:
            action = ShipyardAction.spawn_ships(1)
        shipyard.next_action = action

    return me.next_actions
