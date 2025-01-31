
def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def if_close_to_losing(state):
    enemy_ships = sum(planet.num_ships for planet in state.enemy_planets())
    neutral_ships = sum(planet.num_ships for planet in state.neutral_planets())
    my_ships = sum(planet.num_ships for planet in state.my_ships())
    return enemy_ships/(enemy_ships + my_ships + neutral_ships) >= .65

def if_at_beginning_of_game(state):
    return len(state.my_planets()) <= 3

def if_at_halfway_point(state):
    enemy_and_neutral_ships = sum(planet.num_ships for planet in state.enemy_planets() + state.neutral_planets())
    my_ships = sum(planet.num_ships for planet in state.my_planets())
    p = my_ships/(enemy_and_neutral_ships + my_ships)
    return .40 < p
