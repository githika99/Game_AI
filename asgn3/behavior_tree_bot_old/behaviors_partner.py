import sys
sys.path.insert(0, '../')
from planet_wars import issue_order


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

def defend_against_enemy_planet(state):
    if len(state.my_fleets()) >= 1:
        return False
    nearest_enemy_planet = None
    min_dist = float('inf')
    for enemy_planet in state.enemy_planets():
        for my_planet in state.my_planets():
            distance = state.distance(my_planet, enemy_planet)
            if distance < min_dist: 
                min_dist = distance
                nearest_enemy_planet = enemy_planet

    strongest_planet = None
    max_ships = 0 
    for my_planet in state.my_planets():
        if state.distance(my_planet, nearest_enemy_planet) <= 2:
            if my_planet.num_ships > max_ships:
                max_ships = my_planet.num_ships
                strongest_planet = my_planet
        if not strongest_planet or not nearest_enemy_planet: 
            return False
        else:
            return issue_order(state, strongest_planet.ID, nearest_enemy_planet.ID, strongest_planet.num_ships)

def reinforce_weak_planet(state):
    if len(state.my_fleets()) >= 1:
        return False

    weakest_planet = min(state.my_planets(), key=lambda p: p.num_ships, default=None)
    strongest_planet = None
    max_ships = 0
    for my_planet in state.my_planets():
        if my_planet != weakest_planet and state.distance(my_planet, weakest_planet) <= 2:
            if my_planet.num_ships > max_ships:
                max_ships = my_planet.num_ships
                strongest_planet = my_planet
    
    if not strongest_planet or not weakest_planet:
        return False
    else: 
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)
