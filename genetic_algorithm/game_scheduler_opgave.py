import random
import itertools

class TournamentScheduler:
    def __init__(self, n=4, population_size=100, mutation_rate=0.02, num_generations=300):
        self.n = n
        self.num_teams = 2 * n
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.num_generations = num_generations
        self.fields = list(range(n))

    def generate_individual(self):
        teams = list(range(self.num_teams))
        ind = []
        for _ in range(self.n):
            random.shuffle(teams)
            slot = []
            for i in range(0, self.num_teams, 2):
                A, B = teams[i], teams[i+1]
                f = random.choice(self.fields)
                slot.append((A, B, f))
            ind.append(slot)
        return ind

    def fitness(self, individual):
        # Start met een score op nul

        # Maak een lege set om alle reeds gespeelde match-ups bij te houden

        # Maak een dictionary die per team de reeds gebruikte velden bijhoudt

        # Doorloop elke tijdslot in het individu
            # Maak een set om na te gaan welke teams al in dit tijdslot spelen

            # Doorloop elke wedstrijd (A, B, f) in dit tijdslot

                # Controle 1: team A of B speelt al in ditzelfde tijdslot?
                #   → ja: verlaag score
                #   → nee: verhoog score en markeer teams als gezien

                # Controle 2: match-up (A,B) is al eerder gespeeld?
                #   → ja: verlaag score
                #   → nee: verhoog score en voeg match-up toe

                # Controle 3: team A heeft dit veld al eerder gebruikt?
                #   → ja: verlaag score
                #   → nee: verhoog score en registreer veld

                # Controle 3b: idem voor team B

        # Geef de totale score terug
        pass


    def generate_population(self):
        return [self.generate_individual() for _ in range(self.population_size)]

    def crossover(self, p1, p2):
        point = random.randint(1, self.n - 1)
        return p1[:point] + p2[point:]

    def mutate(self, ind):
        if random.random() > self.mutation_rate:
            return ind
        return self.generate_individual()

    def print_schedule(self, ind):
        for i, slot in enumerate(ind):
            print(f"\nSlot {i+1}:")
            for A, B, f in slot:
                print(f"  {A} vs {B} op veld {f}")

    def genetic_algorithm(self):
        pop = self.generate_population()
        for gen in range(self.num_generations):
            pop.sort(key=self.fitness, reverse=True)
            elite = pop[:int(0.1 * self.population_size)]

            new = elite.copy()
            while len(new) < self.population_size:
                p1 = random.choice(pop[:50])
                p2 = random.choice(pop[:50])
                child = self.crossover(p1, p2)
                new.append(self.mutate(child))

            pop = new
        return pop[0]


# -------------------------------------------------------
# Voorbeeld
# -------------------------------------------------------
if __name__ == "__main__":
    scheduler = TournamentScheduler(n=4)
    solution = scheduler.genetic_algorithm()
    print("Fitness:", scheduler.fitness(solution))
    scheduler.print_schedule(solution)
