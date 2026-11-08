"""
Oefening 1: Word Generator (Genetisch Algoritme)
==================================================
Evolueer een populatie van willekeurige zinnen naar een doelzin.
"""

import random
import string


class WordPuzzle:
    def __init__(
        self,
        target_phrase,
        population_size=100,
        mutation_rate=0.05,
        num_generations=10000,
    ):
        self.target_phrase = target_phrase
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.num_generations = num_generations

    def generate_phrase(self, length):
        phrase = ""
        for i in range(length):
            r_idx = random.randint(0, len(string.printable) - 1)
            phrase += string.printable[r_idx]

        return str(phrase)

    def calculate_fitness(self, phrase):
        score = 0
        for c, t in zip(phrase, self.target_phrase):
            if c == t:
                score += 1

        return score / len(phrase)

    def generate_population(self, size, phrase_length):
        population = [self.generate_phrase(phrase_length) for i in range(size)]
        return population

    def crossover(self, phrase1, phrase2):
        r_idx = random.randint(0, len(phrase1))
        new_phrase = phrase1[:r_idx] + phrase2[r_idx:]
        return new_phrase

    def mutate(self, phrase, rate):
        new_phrase = ""
        for i in phrase:
            if random.random() <= rate:
                r_idx = random.randint(0, len(string.printable) - 1)
                new_phrase += string.printable[r_idx]
            else:
                new_phrase += i

        return new_phrase

    def select_best(self, population):
        pass

    def genetic_algorithm(self):
        population = self.generate_population(
            self.population_size, len(self.target_phrase)
        )

        best = ""
        for g in range(self.num_generations):
            pop_w_score = [
                {"instance": i, "score": self.calculate_fitness(i)} for i in population
            ]
            pop_w_score = sorted(pop_w_score, key=lambda pop: pop["score"])
            top2 = pop_w_score[-4:]
            best = pop_w_score[-1]["instance"]

            new_gen = [t["instance"] for t in top2]
            new_gen.append(
                self.crossover(new_gen[0], new_gen[1]),
            )
            new_gen.extend([self.mutate(j, self.mutation_rate) for j in new_gen])

            population = new_gen
            if g % 10 == 0:
                print(top2[0])

        return best


def main():
    target_phrase = "De basiswetten van de robotica werden ontwikkeld door Asimov"
    puzzle = WordPuzzle(target_phrase)
    # print(puzzle.generate_phrase(len(target_phrase)))
    # print(puzzle.crossover(puzzle.generate_phrase(len(target_phrase)), target_phrase))
    best_phrase = puzzle.genetic_algorithm()
    print(f"Beste zin: {best_phrase}")


if __name__ == "__main__":
    main()
