

def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def if_close_to_winning(state):
    enemy_ships = sum(planet.num_ships for planet in state.enemy_planets())
    my_ships = sum(planet.num_ships for planet in state.my_ships())
    return my_ships/(enemy_ships + my_ships) >= .90
