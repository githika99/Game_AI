import sys
sys.path.insert(0, '../')
from planet_wars import issue_order
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import random

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
    bots_needed_from_p = weakest_planet.num_ships + (state.distance(strongest_planet.ID, weakest_planet.ID) * weakest_planet.growth_rate) + 5
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
    bots_needed_from_p = weakest_planet.num_ships + 5
    if strongest_planet.num_ships * 2/3 > bots_needed_from_p:
        bots = bots_needed_from_p

    #(4) Send half the ships from my strongest planet to the weakest enemy planet.
    return issue_order(state, strongest_planet.ID, weakest_planet.ID, bots)

def spread_to_many_neutral_planets(state):
    # (2) Find my strongest planets.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet:
        return False

    # (3) Find the 10 closest neutral/enemy planets.
    weakest_planets = sorted(state.neutral_planets() + state.enemy_planets(), key=lambda p: state.distance(strongest_planet.ID, p.ID))

    if not weakest_planets:
    # No legal source or destination
        return False

    # Find a neutral planet that we are not travelling to
    all_dest_planets = []
    for fleet in state.my_fleets():
        all_dest_planets.append(fleet.destination_planet)
    
    weakest_planet = weakest_planets[0]
    for p in weakest_planets:
        if p.ID not in all_dest_planets:
            weakest_planet = p
            break
    
    bots = strongest_planet.num_ships/2
    
    # (4) Send half the ships from my strongest planet to the weakest enemy planet.
    return issue_order(state, strongest_planet.ID, weakest_planet.ID, bots)

# At the halfway point we need to become more aggressive
def spread_more_aggressively(state):
    # select one of my planets: pick a random planet
    # strongest_planet = random.choice(state.my_planets())

    strongest_planet = None
    for planet in state.my_planets():
        if all(fleet.source_planet != planet.ID for fleet in state.my_fleets()):
            strongest_planet = planet

    if strongest_planet is None:
        strongest_planet = state.my_planets()[0]

    logging.info('\n randomly picked planet with id {strongest_planet.ID}')

    # select a enemy/neutral planet that is near it
    cloest_planets = sorted(state.enemy_planets() + state.neutral_planets(), key=lambda p: state.distance(strongest_planet.ID, p.ID))
    closest_planet = None
    for planet in cloest_planets:
        if not any(fleet.source_planet == strongest_planet.ID and fleet.destination_planet == planet.ID for fleet in state.my_fleets()):
            closest_planet = planet
            break  # Stop at the first valid planet

    
    if closest_planet is None:
    # No legal source or destination
        return False
    
    # send half of your ships
    bots = strongest_planet.num_ships/2
        
    # (4) Send half the ships from my strongest planet to the weakest enemy planet.
    return issue_order(state, strongest_planet.ID, closest_planet.ID, bots)

# def save_my_planets(state):
    # see all enemy fleets, and for ones that will beat my planets, save them if possible


def send_something(state):
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    
    weakest_planet = random.choice(state.enemy_planets() + state.neutral_planets())

    if not strongest_planet or not weakest_planet:
        return False
    
    bots = strongest_planet.num_ships/2
    if weakest_planet.owner == 0:
        bots_needed_from_p = weakest_planet.num_ships + 5
    else: #it is enemy
        bots_needed_from_p = weakest_planet.num_ships + (state.distance(strongest_planet.ID, weakest_planet.ID) * weakest_planet.growth_rate)

    if strongest_planet.num_ships * 2/3 > bots_needed_from_p:
        bots = bots_needed_from_p

    return issue_order(state, strongest_planet.ID, weakest_planet.ID, bots)

    



# reinforce our weakest planets
