import random

from Operation.operation import calculate_route_distance


def tournament_selection(population, k):
    new_selection = []

    for i in range(len(population)):
        tournament = random.sample(population, k)
        sorted_tournament = sort_population(tournament)
        winner = sorted_tournament[0]
        new_selection.append(winner)

    return new_selection


def sort_population(population):
    for pop in population:
        pop.distance = calculate_route_distance(pop)
    return sorted(population, key=lambda x: x.distance, reverse=False)
