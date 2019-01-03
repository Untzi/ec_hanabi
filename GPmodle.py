import copy
import random
import numpy
from functools import partial
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

from card import *
from game import *
from player import *

import operator

def if_then_else(condition, out1, out2):
    out1() if condition() else out2()

def if_play(condition, out1, out2):
    ans, card =  condition()
    if ans:
        out1(card, )
    else:
        out2()

pset = gp.PrimitiveSetTyped("MAIN", 0)
pset.addPrimitive(if_then_else, [bool, function, function], function)
pset.addPrimitive(operator.or_, [bool, bool], bool)
pset.addPrimitive(operator.and_, [bool, bool], bool)
pset.addPrimitive(operator.not_, [bool], bool)
# pset.addTerminal(player.player_place_card)
# pset.addTerminal(player.discard_card)
# pset.addTerminal(player.tell_info)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr_init", gp.genFull, pset=pset, min_=6, max_=10)

toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr_init)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def run_game(individual):



# here we call the game
toolbox.register("evaluate", run_game)
toolbox.register("select", tools.selTournament, tournsize=7)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
