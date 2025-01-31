#!/usr/bin/env python
#

"""
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn


# You have to improve this tree or create an entire new one that is capable
# of winning against all the 5 opponent bots
def setup_behavior_tree():

    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')

    enemy_seq_1 = Sequence(name='Attack Enemy Strategy')
    enemy_check = Check(if_enemy_planet_available)
    enemy_general_action = Action(attack_weakest_enemy_planet_with_my_strongest)
    enemy_seq_1.child_nodes[enemy_check, enemy_general_action]

    neutral_seq_1 = Sequence(name='Attack Neutral Strategy')
    neutral_check = Check(if_neutral_planet_available)
    neutral_general_action = Action(attack_weakest_neutral_planet_with_my_strongest)
    neutral_seq_1.child_nodes[neutral_check, neutral_general_action]

    root.child_nodes = [enemy_seq_1, neutral_seq_1, Action(attack_weakest_enemy_planet_with_my_strongest)]


    # losing_plan = Sequence(name='Losing Strategy')
    # losing_check = Check(if_close_to_losing)
    # losing_action = Action()
    # losing_plan.child_nodes(losing_check, losing_action)

    # winning_plan = Sequence(name='Winning Strategy')
    # winning_check = Check(if_close_to_winning)
    # winning_action = Action()
    # winning_plan.child_nodes(winning_check, winning_action)

    # enemy_seq_1 = Sequence(name='Attack Enemy Strategy')
    # enemy_check = Check(if_enemy_planet_available)
    # enemy_seq_2 = Sequence(name='Attack Enemy with Nearby Ships Strategy')
    # enemy_nearby_ships_check = Check(if_my_planet_has_more_ships_than_weakest_enemy)
    # enemy_nearby_ships_action = Action(attack_weakest_enemy_planet_with_my_closest)
    # enemy_general_action = Action(attack_weakest_enemy_planet_with_my_strongest)
    # enemy_seq_2.child_nodes = [enemy_nearby_ships_check, enemy_nearby_ships_action]
    # enemy_seq_1.child_nodes[enemy_check, enemy_seq_2.copy(), enemy_general_action]

    # neutral_seq_1 = Sequence(name='Attack Neutral Strategy')
    # neutral_check = Check(if_neutral_planet_available)
    # neutral_seq_2 = Sequence(name='Attack Neutral with Nearby Ships Strategy')
    # neutral_nearby_ships_check = Check(if_my_planet_has_more_ships_than_weakest_neutral)
    # neutral_nearby_ships_action = Action(attack_weakest_neutral_planet_with_my_closest)
    # neutral_general_action = Action(attack_weakest_neutral_planet_with_my_strongest)
    # neutral_seq_2.child_nodes = [neutral_nearby_ships_check, neutral_nearby_ships_action]
    # neutral_seq_1.child_nodes[neutral_check, neutral_seq_2.copy(), neutral_general_action]

    # root.child_nodes = [losing_plan, winning_plan, enemy_seq_1, neutral_seq_1, Action(attack_weakest_enemy_planet_with_my_strongest)]

    logging.info('\n' + root.tree_to_string())
    return root

# You don't need to change this function
def do_turn(state):
    behavior_tree.execute(planet_wars)

if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
