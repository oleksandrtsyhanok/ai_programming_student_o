from agent import EvoAgent
from evolution import evolve


if __name__ == "__main__":
    # initial population
    population = [EvoAgent() for _ in range(20)]

    # evolve
    population = evolve(population, generations=15)

    # best agent
    best = population[0]

    print("\nBest agent weights:")
    print(best.weights)