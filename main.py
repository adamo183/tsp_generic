import copy
import random

from Model.Config import read_config_file
from Operation.operation import open_tsp_file, generate_population, crossover, inversion_mutation, swap_mutation, \
    calculate_route_distance, print_result
from Operation.selection import tournament_selection, sort_population

distance_data = []

if __name__ == '__main__':
    config = read_config_file()
    distance_data = open_tsp_file(config.data_path)
    population = generate_population(config.population_size, len(distance_data[-1])-1)
    current_iteration = 0
    best_score = calculate_route_distance(population[0])
    while current_iteration <= config.iteration:
        parents = tournament_selection(population, config.selection_number_k)
        children = []

        for i in range(0, len(parents), 2):
            parent1 = copy.deepcopy(parents[i])
            parent2 = copy.deepcopy(parents[i + 1])

            do_crossover = random.random() < config.crossing_rate

            if do_crossover:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1 = copy.deepcopy(parent1)
                child2 = copy.deepcopy(parent2)

            if random.random() < config.inversion_rate:
                child1 = inversion_mutation(child1)
                child2 = inversion_mutation(child2)

            if random.random() < config.mutation_rate:
                child1 = swap_mutation(child1)
                child2 = swap_mutation(child2)

                children.append(child1)
                children.append(child2)
            else:
                children.append(parent1)
                children.append(parent2)

        candidates = parents + children
        parents = sort_population(candidates)
        population = parents[0:config.population_size]
        if (calculate_route_distance(population[0]) < best_score):
            best_score = calculate_route_distance(population[0]);
            print('New minimal route length: ' + str(best_score) + ' in iteration: ' + str(current_iteration))
        current_iteration += 1

    min_route = population[0]
    print("Minimum calculated route for " + str(config.data_path))
    print(min_route.route)
    print(calculate_route_distance(min_route))
    print_result(min_route)



