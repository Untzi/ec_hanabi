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


game1 = Game(2, None)


def if_then_else(condition, out1, out2):
    out1() if condition() else out2()


def if_play(condition, out1, out2):
    ans, card = condition()
    if ans:
        out1(card, )
    else:
        out2()


def can_tell_about_ones1(out1, out2):
    return partial(game1.can_tell_about_ones, out1, out2)


def has_playable_card1(out1, out2):
    return partial(game1.has_playable_card, out1, out2)


pset = gp.PrimitiveSet("MAIN", 0)
pset.addPrimitive(can_tell_about_ones1, 2)
pset.addPrimitive(has_playable_card1, 2)
pset.addTerminal(game1.play_playable_card)
pset.addTerminal(game1.tell_about_ones)
pset.addTerminal(game1.play_random_card)

creator.create("FitnessMax", base.Fitness, weights=(1.0, ))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr_init", gp.genFull, pset=pset, min_=6, max_=10)

toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr_init)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def run_game(individual):
    player_action_tree = gp.compile(individual, pset)
    # run the game
    if player_action_tree == None:
        return 0
    generate_game = partial(game1.__init__, players_num = 2, player_action_tree=player_action_tree)
    generate_game()
    game1.run_game()
    # if game1.endgame() == 0:
    #     return float(1)
    return game1.endgame(),


# here we call the game
toolbox.register("evaluate", run_game)
toolbox.register("select", tools.selTournament, tournsize=7)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

pop = toolbox.population(n=30)
hof = tools.HallOfFame(1)
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean)
stats.register("std", numpy.std)
stats.register("min", numpy.min)
stats.register("max", numpy.max)

algorithms.eaSimple(pop, toolbox, 0.7, 0.3, 100, stats, halloffame=hof)

print("end")
# return pop, hof, stats