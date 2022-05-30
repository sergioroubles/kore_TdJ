def box_miner(turn):
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
    return action