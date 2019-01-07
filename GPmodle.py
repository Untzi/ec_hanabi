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
import os
try:
    os.remove('results.txt')
except:
    pass

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

def can_tell1(out1, out2):
    return partial(game1.can_tell, out1, out2)


pset = gp.PrimitiveSet("MAIN", 0)
pset.addPrimitive(can_tell_about_ones1, 2)
pset.addPrimitive(has_playable_card1, 2)
pset.addPrimitive(can_tell1, 2)
pset.addTerminal(game1.play_playable_card)
pset.addTerminal(game1.tell_about_ones)
pset.addTerminal(game1.play_random_card)
pset.addTerminal(game1.discard_oldest_with_least_info)

creator.create("FitnessMax", base.Fitness, weights=(1.0, ))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr_init", gp.genFull, pset=pset, min_=4, max_=10)

toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr_init)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def run_game(individual):
    player_action_tree = gp.compile(individual, pset)
    n = 2
    # run the game
    if player_action_tree == None:
        return 0
    ls = []
    for i in range(n):
        game1.reset(2, player_action_tree=player_action_tree)
        # generate_game = partial(game1.__init__, players_num = 2, player_action_tree=player_action_tree)
        # generate_game()
        ls.append(game1.run_game())
    # if game1.endgame() == 0:
    #     return float(1)
    avg = sum(ls) / float(len(ls))
    return avg,


# here we call the game
toolbox.register("evaluate", run_game)
toolbox.register("select", tools.selTournament, tournsize=7)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

pop = toolbox.population(n=30)
hof = tools.HallOfFame(3)
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean)
stats.register("std", numpy.std)
stats.register("min", numpy.min)
stats.register("max", numpy.max)

algorithms.eaSimple(population=pop, toolbox=toolbox, cxpb=0.9, mutpb=0.1, ngen=100,
                    stats=stats, halloffame=hof, verbose=True)

print("end")
# expr = toolbox.individual()
# nodes, edges, labels = gp.graph(expr)

# import matplotlib.pyplot as plt
# import networkx as nx
#
# g = nx.Graph()
# g.add_nodes_from(nodes)
# g.add_edges_from(edges)
# pos = nx.graphviz_layout(g, prog="dot")
#
# nx.draw_networkx_nodes(g, pos)
# nx.draw_networkx_edges(g, pos)
# nx.draw_networkx_labels(g, pos, labels)
# plt.show()