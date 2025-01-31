def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())


def if_enemy_planet_near(planet_wars):
    for planet in planet_wars.my_planets():
        for neighbor in planet_wars.planets_within_distance(planet, 2):
            if neighbor.owner() != planet_wars.my_player():
                return True
    return False

def if_weak_planet(planet_wars):
    for planet in planet_wars.my_planets():
        if planet.num_ships() < 10:
            return True
    return False

def defend_against_enemy_planet(planet_wars):
    for planet in planet_wars.my_planets():
        for neighbor in planet_wars.planets_within_distance(planet, 2):
            if neighbor.owner() != planet_wars.my_player():
                planet_wars.issue_order(planet, neighbor)
                return

def reinforce_weak_planet(planet_wars):
    weakest_planet = None
    for planet in planet_wars.my_planets():
        if planet.num_ships() < 10:
            if weakest_planet is None or planet.num_ships() < weakest_planet.num_ships():
                weakest_planet = planet
    if weakest_planet:
        for planet in planet_wars.my_planets():
            if planet != weakest_planet:
                planet_wars.issue_order(planet, weakest_planet)
                return
