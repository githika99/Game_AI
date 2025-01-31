import sys
sys.path.insert(0, '../')
from planet_wars import issue_order
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


def attack_weakest_enemy_planet(state):
    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    
    logging.info(f'\n trying source {strongest_planet.ID} destination {weakest_planet.ID}')
    
    str1 = ''
    count = 0
    sent_so_far = 0
    for fleet in state.my_fleets():
        str1 += f'\nfleet {count} source {fleet.source_planet} destination {fleet.destination_planet}'
        count += 1
        if fleet.source_planet == strongest_planet.ID and fleet.destination_planet == weakest_planet.ID:
            logging.info('\n Match')
            return False
        elif fleet.destination_planet == weakest_planet.ID:
            # Check if this fleet will convert the planet 
            bots_needed_for_this_fleet = weakest_planet.num_ships + (state.distance(fleet.source_planet, weakest_planet.ID) * weakest_planet.growth_rate)
            if fleet.num_ships >= bots_needed_for_this_fleet:
                return False
            sent_so_far += fleet.num_ships
    logging.info('\n' + str1)

    # (5) Calculate the necessary amount of ships to send
    bots = strongest_planet.num_ships/2
    bots_needed_from_p = weakest_planet.num_ships + (state.distance(strongest_planet.ID, weakest_planet.ID) * weakest_planet.growth_rate) + 5 - sent_so_far
    if strongest_planet.num_ships * 2/3 > bots_needed_from_p:
        bots = bots_needed_from_p

    #(4) Send half the ships from my strongest planet to the weakest enemy planet.
    return issue_order(state, strongest_planet.ID, weakest_planet.ID, bots)


def spread_to_weakest_neutral_planet(state):
    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)


    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    
    logging.info(f'\n trying source {strongest_planet.ID} destination {weakest_planet.ID}')
    
    str1 = ''
    count = 0
    sent_so_far = 0
    for fleet in state.my_fleets():
        str1 += f'\nfleet {count} source {fleet.source_planet} destination {fleet.destination_planet}'
        count += 1
        if fleet.source_planet == strongest_planet.ID and fleet.destination_planet == weakest_planet.ID:
            logging.info('\n Match')
            return False
        elif fleet.destination_planet == weakest_planet.ID:
            # Check if this fleet will convert the planet 
            sent_so_far += fleet.num_ships
            if sent_so_far >= weakest_planet.num_ships:
                return False
    logging.info('\n' + str1)
    
    # (5) Calculate the necessary amount of ships to send
    bots = strongest_planet.num_ships/2
    bots_needed_from_p = weakest_planet.num_ships + 5 - sent_so_far
    if strongest_planet.num_ships * 2/3 > bots_needed_from_p:
        bots = bots_needed_from_p

    #(4) Send half the ships from my strongest planet to the weakest enemy planet.
    return issue_order(state, strongest_planet.ID, weakest_planet.ID, bots)

# def close_to_winning(state):
