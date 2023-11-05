import random
import tsplib95
import pandas as pd
import matplotlib.pyplot as plt


import numpy as np

from Model.Config import read_config_file
from Model.Coords import Route
from Model.MapDisplay import MapDisplay

config = read_config_file()


def open_tsp_file(path: str):
    input = open(path, "r")
    var = []
    for line in input:
        var.append(line.strip().split(' '))
    return var


distance_data = open_tsp_file(config.data_path)


def generate_population(pop_number, route_length):
    population = []
    for i in range(pop_number):
        data_to_shuffle = list(range(1, route_length+1, 1))
        random.shuffle(data_to_shuffle)
        elem = Route()
        elem.route = data_to_shuffle
        population.append(elem)
    return population


def calculate_route_distance(route : Route) -> int:
        route_distance = 0
        for point in range(len(route.route)):
            if point + 1 < len(route.route):
                distance = get_distance_between_points(route.route[point],route.route[point + 1])
            else:
                distance = get_distance_between_points(route.route[point], route.route[0])
            route_distance += int(distance)
        return route_distance


def get_distance_between_points(point_1: int, point_2: int) -> int:
    min_p = min(point_1, point_2)
    max_p = max(point_1, point_2)
    return distance_data[int(max_p-1)][int(min_p-1)]


def crossover(parent1, parent2):
    size = len(parent1.route)
    point1, point2 = sorted(random.sample(range(size), 2))
    child1 = pmx_crossover(parent1, parent2, point1, point2)
    child2 = pmx_crossover(parent2, parent1, point1, point2)

    parent1Cross = Route()
    parent1Cross.route = child1.tolist()

    parent2Cross = Route()
    parent2Cross.route = child2.tolist()
    return parent1Cross, parent2Cross


def pmx_crossover(parent1, parent2, sequence_start, sequence_end):
    child = np.zeros(len(parent1.route))
    parent1_to_child1_genes = parent1.route[sequence_start:sequence_end]

    parent1_to_child1 = np.isin(parent1.route, parent1_to_child1_genes).nonzero()[0]

    for gene in parent1_to_child1:
        child[gene] = parent1.route[gene]

    genes_not_in_child = np.array(parent2.route)[np.isin(parent2.route, parent1_to_child1_genes, invert=True).nonzero()[0]]

    if genes_not_in_child.shape[0] >= 1:
        for gene in genes_not_in_child:
            if gene >= 1:
                lookup = gene
                not_in_sequence = True

                while not_in_sequence:
                    position_in_parent2 = parent2.route.index(lookup)

                    if position_in_parent2 in range(sequence_start, sequence_end):
                        lookup = np.array(parent1.route[position_in_parent2])

                    else:
                        child[position_in_parent2] = gene
                        not_in_sequence = False

    return child


def inversion_mutation(child):
    size = len(child.route)
    point1, point2 = sorted(random.sample(range(size), 2))
    child.route[point1:point2] = reversed(child.route[point1:point2])
    return child


def swap_mutation(child):
    size = len(child.route)
    point1, point2 = random.sample(range(size), 2)
    child.route[point1], child.route[point2] = child.route[point2], child.route[point1]
    return child


def print_result(population):
    raw_data = tsplib95.load('berlin52map.tsp')
    coords_array = []
    for node in raw_data.node_coords:
        coords_array.append({"id":node,"long": raw_data.node_coords[node][0],"lat":raw_data.node_coords[node][1]})

    data_to_print = []

    for coords in population.route:
        mapdata = [x for x in coords_array if x["id"] == int(coords)][0]
        data_to_add = [mapdata['long'], mapdata['lat']]
        data_to_print.append(data_to_add)

    data_to_print.append([data_to_print[0][0], data_to_print[0][1]])
    df = pd.DataFrame(data=data_to_print, columns=['x', 'y'])
    df.plot(x='x', y='y')
    plt.show()


