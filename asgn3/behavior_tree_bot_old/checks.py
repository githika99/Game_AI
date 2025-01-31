
def if_neutral_planet_available(state):
    return any(state.neutral_planets())

# Only called if_neutral_planet_available True
def if_my_planet_has_more_ships_than_weakest_neutral(state):
    weakest_planet = min(state.neutral_planets(), key=lambda t: t.num_ships, default=None)
    bots_needed_from_p = weakest_planet.num_ships
    for p in state.my_planets():
        if p.num_ships * 2/3 >= bots_needed_from_p:
            return True
    return False

def if_enemy_planet_available(state):
    return any(state.enemy_planets())

# Only called if_neutral_planet_available True
def if_my_planet_has_more_ships_than_weakest_enemy(state):
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)
    for p in state.my_planets():
        bots_needed_from_p = weakest_planet.num_ships + (state.distance(p.ID, weakest_planet.ID) * weakest_planet.growth_rate)
        if p.num_ships * 2/3 >= bots_needed_from_p:
            return True
    return False

def if_close_to_winning(state):
    other_ships = sum(planet.num_ships for planet in state.enemy_planets() + state.neutral_planets())
    my_ships = sum(planet.num_ships for planet in state.my_ships())
    return (state.enemy_planets() + state.neutral_planets() <= 3) or (my_ships/(other_ships + my_ships) >= .90)

def if_close_to_losing(state):
    other_ships = sum(planet.num_ships for planet in state.my_planets() + state.neutral_planets())
    enemy_ships = sum(planet.num_ships for planet in state.enemy_ships())
    return (enemy_ships/(other_ships + enemy_ships) >= .90)

def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

"""
def if_my_planet_has_less_than_weakest_enemy_send_nearby_ships(state):
    if not if_enemy_planet_available(state):
        return False
    if if_my_planet_has_ships_than_weakest_enemy(state):
        return False
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)
    my_closest_planets = sorted(state.my_planets(), key=lambda p: state.distance(p.ID, weakest_planet.ID))[:5]  
    return weakest_planet.num_ships <= sum(planet.num_ships for planet in my_closest_planets)

def if_my_planet_has_less_than_weakest_enemy_send_strongest_ships(state):
    if not if_enemy_planet_available(state):
        return False
    if if_my_planet_has_ships_than_weakest_enemy(state):
        return False
    if if_my_planet_has_less_than_weakest_enemy_send_nearby_ships(state):
        return False
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)
    my_closest_planets = sorted(state.my_planets(), key=lambda p: state.distance(p.ID, weakest_planet.ID))[:5]  
    return weakest_planet.num_ships > sum(planet.num_ships for planet in my_closest_planets)
"""
