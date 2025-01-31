import sys
sys.path.insert(0, '../')
from planet_wars import issue_order
import logging


# Returns a list of [(my_planet_name, distance), ...] of my planets with the first one being closest to opp_planet
def my_planets_closest_to_and_stronger_than(state, target_planet, factor, buffer):
    res_planets = []
    res_bots = []
    for p in state.my_planets():
        if target_planet.owner == 2:
            bots_needed_from_p = target_planet.num_ships + (state.distance(p.ID, target_planet.ID) * target_planet.growth_rate)
        else: #opp_planet_is_neutral
            bots_needed_from_p = target_planet.num_ships
        
        # add buffer so we're not at 0 when we get there 
        bots_needed_from_p += buffer

        # if bots_needed_from_p is factor or less of p.num_ships()
        if p.num_ships * factor >= bots_needed_from_p:
            res_planets.append(p)
            res_bots.append(bots_needed_from_p) 

    return res_planets, res_bots 


def attack_weakest_enemy_planet_with_my_strongest(state):
    # (1) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    
    if len(state.my_fleets()) >= 1:
        for fleet in state.my_fleets():
            s = fleet.source_planet
            d = fleet.destination_planet
        logging.info('\n NEWWW I have an exisitng fleet with source ' + str(s) + ' and desitnation ' + str(d) + ' len of fleets '+ str(len(state.my_fleets()))
         + '\n I would have launched source ' + str(strongest_planet.ID), ' destination ' + str(weakest_planet.ID))
        return False
    
    # (3) If we currently have a fleet in flight from weakest_planet to strongest_planet stop
    elif any(fleet.destination_planet == weakest_planet.ID for fleet in state.my_fleets()):
        return False
    
    else:
        # (4) Send the num of ships needed from my strongest planet to the weakest enemy planet.
        bots_needed = weakest_planet.num_ships + (state.distance(strongest_planet.ID, weakest_planet.ID) * weakest_planet.growth_rate)
        bots_needed += 5
        if bots_needed > strongest_planet.num_ships:
            bots_needed =  strongest_planet.num_ships / 2
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, bots_needed)

def attack_weakest_enemy_planet_with_my_closest(state):

    # (1) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not weakest_planet:
        # No legal source or destination
        return False
    
    # (2) Find my closest planet to weakest_planet
    res_planets, res_bots = my_planets_closest_to_and_stronger_than(state, weakest_planet, 2/3, 5)
    bots = min(res_bots)
    my_planet = res_planets[res_bots.index(bots)]

    # if none of our planets are more powerful than weakest_planet, send half of ships from nearby planets

    if not my_planet or not weakest_planet:
        # No legal source or destination
        return False
    
    # if len(state.my_fleets()) >= 1:
    #     for fleet in state.my_fleets():
    #         s = fleet.source_planet
    #         d = fleet.destination_planet
    #     logging.info('\n I have an exisitng fleet with source ' + str(s) + ' and desitnation ' + str(d) + ' len of fleets '+ str(len(state.my_fleets())))
    #     logging.info('\n I would have launched source', str(my_planet.ID), 'destination', str(weakest_planet.ID))
    #     return False
    
    # (3) If we currently have a fleet in flight from weakest_planet to strongest_planet stop
    elif any(fleet.destination_planet == weakest_planet.ID for fleet in state.my_fleets()):
        return False
    
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, my_planet.ID, weakest_planet.ID, bots)

def attack_weakest_neutral_planet_with_my_strongest(state):
    # (1) Find the weakest enemy planet.
    weakest_planet = min(state.neutral_planets(), key=lambda t: t.num_ships, default=None)

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    
    if len(state.my_fleets()) >= 1:
        for fleet in state.my_fleets():
            s = fleet.source_planet
            d = fleet.destination_planet
        logging.info('\n NEWWW I have an exisitng fleet with source ' + str(s) + ' and desitnation ' + str(d) + ' len of fleets '+ str(len(state.my_fleets()))
         + '\n I would have launched source ' + str(strongest_planet.ID), ' destination ' + str(weakest_planet.ID))
        return False
    
    # (3) If we currently have a fleet in flight from weakest_planet to strongest_planet stop
    elif any(fleet.destination_planet == weakest_planet.ID for fleet in state.my_fleets()):
        return False
    
    else:
        # (4) Send the num of ships needed from my strongest planet to the weakest enemy planet.
        bots_needed = weakest_planet.num_ships
        bots_needed += 5
        if bots_needed > strongest_planet.num_ships:
            bots_needed =  strongest_planet.num_ships / 2
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, bots_needed)

def attack_weakest_neutral_planet_with_my_closest(state):
    if len(state.my_fleets()) >= 1:
        return False

    # (1) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not weakest_planet:
        # No legal source or destination
        return False
    
    # (2) Find my closest planet to weakest_planet
    res_planets, res_bots = my_planets_closest_to_and_stronger_than(state, weakest_planet, 2/3, 5)
    bots = min(res_bots)
    my_planet = res_planets[res_bots.index(bots)]

    if not my_planet or not weakest_planet:
        # No legal source or destination
        return False
    
    if len(state.my_fleets()) >= 1:
        for fleet in state.my_fleets():
            s = fleet.source_planet
            d = fleet.destination_planet
        logging.info('\n NEWWW I have an exisitng fleet with source ' + str(s) + ' and desitnation ' + str(d) + ' len of fleets '+ str(len(state.my_fleets()))
         + '\n I would have launched source ' + str(my_planet.ID), ' destination ' + str(weakest_planet.ID))
        return False
    
    # (3) If we currently have a fleet in flight from weakest_planet to strongest_planet stop
    elif any(fleet.destination_planet == weakest_planet.ID for fleet in state.my_fleets()):
        return False
    
    else:
        # (4) Send required num of ships from my strongest planet to the weakest enemy planet if my strongest planet has that many
        return issue_order(state, my_planet.ID, weakest_planet.ID, bots)

def close_to_winning(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False
    # Be more aggresive and attack all neutral or enemy planets

    # (1) Find the weakest neutral/enemy planet.
    weakest_planet = min(state.neutral_planets() and state.enemy_planets(), key=lambda p: p.num_ships, default=None)

    if not weakest_planet:
        return False
    
    # (2) Find my closest planet to weakest_planet
    res_planets, res_bots = my_planets_closest_to_and_stronger_than(state, weakest_planet, 1, 1)
    bots = min(res_bots)
    my_planet = res_planets[res_bots.index(bots)]

    if not my_planet or not weakest_planet:
        # No legal source or destination
        return False
    
    # (3) If we currently have a fleet in flight from weakest_planet to strongest_planet stop
    elif any(fleet.destination_planet == weakest_planet.ID for fleet in state.my_fleets()):
        return False
    
    else:
        # (4) Send required num of ships from my strongest planet to the weakest enemy planet if my strongest planet has that many
        return issue_order(state, my_planet.ID, weakest_planet.ID, bots)

# attack neutral planets that are near my strongest planet(s)

# if remianing enemy planet/neutral planets have more ships than we can account for, send half of nearby 
# ships to it
