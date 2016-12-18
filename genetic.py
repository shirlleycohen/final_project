import sys, random
from math import sqrt
from pickle import *

PIL_SUPPORT = None
try:
    from PIL import Image, ImageDraw, ImageFont

    PIL_SUPPORT = True
except:
    PIL_SUPPORT = False


def cartesian_matrix(coords):
    """ A distance matrix """
    matrix = {}
    for i, (x1, y1) in enumerate(coords):
        for j, (x2, y2) in enumerate(coords):
            dx, dy = x1 - x2, y1 - y2
            dist = sqrt(dx * dx + dy * dy)
            matrix[i, j] = dist
    return matrix


def tour_length(matrix, tour):
    """ Returns the total length of the tour """
    total = 0
    num_cities = len(tour)
    for i in range(num_cities):
        j = (i + 1) % num_cities
        city_i = tour[i]
        city_j = tour[j]
        total += matrix[city_i, city_j]
    return total

cm = []
coords = []


def eval_func(chromosome):
    """ The evaluation function """
    global cm
    return tour_length(cm, chromosome)


def cities_random(cities, xmax=800, ymax=600):
    """ get random cities/positions """
    coords = []
    for i in xrange(cities):
        x = random.randint(0, xmax)
        y = random.randint(0, ymax)
        coords.append((float(x), float(y)))
    return coords


# Individuals
class Individual:
    score = 0
    length = 30
    seperator = ' '

    def __init__(self, chromosome=None, length=30):
        self.chromosome = chromosome or self._makechromosome()
        self.length = length
        self.score = 0  # set during evaluation

    def _makechromosome(self):
        "makes a chromosome from randomly selected alleles."
        chromosome = []
        lst = [i for i in xrange(self.length)]
        for i in xrange(self.length):
            choice = random.choice(lst)
            lst.remove(choice)
            chromosome.append(choice)
        return chromosome

    def evaluate(self, optimum=None):
        self.score = eval_func(self.chromosome)

    def crossover(self, other):
        left, right = self._pickpivots()
        p1 = Individual()
        p2 = Individual()
        c1 = [c for c in self.chromosome \
              if c not in other.chromosome[left:right + 1]]
        p1.chromosome = c1[:left] + other.chromosome[left:right + 1] \
                        + c1[left:]
        c2 = [c for c in other.chromosome \
              if c not in self.chromosome[left:right + 1]]
        p2.chromosome = c2[:left] + self.chromosome[left:right + 1] \
                        + c2[left:]
        return p1, p2

    def mutate(self):
        "swap two element"
        left, right = self._pickpivots()
        temp = self.chromosome[left]
        self.chromosome[left] = self.chromosome[right]
        self.chromosome[right] = temp

    def _pickpivots(self):
        left = random.randint(0, self.length - 2)
        right = random.randint(left, self.length - 1)
        return left, right

    def __repr__(self):
        "returns string representation of self"
        return '<%s chromosome="%s" score=%s>' % \
               (self.__class__.__name__,
                self.seperator.join(map(str, self.chromosome)), self.score)

    def copy(self):
        twin = self.__class__(self.chromosome[:])
        twin.score = self.score
        return twin

    def __cmp__(self, other):
        return cmp(self.score, other.score)


class Environment:
    size = 0

    def __init__(self, population=None, size=100, maxgenerations=1000, \
                 newindividualrate=0.6, crossover_rate=0.9, \
                 mutation_rate=0.1):
        self.size = size
        self.population = self._makepopulation()
        self.maxgenerations = maxgenerations
        self.newindividualrate = newindividualrate
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        for individual in self.population:
            individual.evaluate()
        self.generation = 0
        self.minscore = sys.maxint
        self.minindividual = None
        # self._printpopulation()

    def _makepopulation(self):
        return [Individual() for i in range(0, self.size)]

    def run(self):
        for i in range(1, self.maxgenerations + 1):
            print "Generation no:" + str(i)
            for j in range(0, self.size):
                self.population[j].evaluate()
                curscore = self.population[j].score
                if curscore < self.minscore:
                    self.minscore = curscore
                    self.minindividual = self.population[j]
            print "Best individual:", self.minindividual
            if random.random() < self.crossover_rate:
                children = []
                newindividual = int(self.newindividualrate * self.size / 2)
                for i in range(0, newindividual):
                    selected1 = self._selectrank()
                    selected2 = self._selectrank()
                    parent1 = self.population[selected1]
                    parent2 = self.population[selected2]
                    child1, child2 = parent1.crossover(parent2)
                    child1.evaluate()
                    child2.evaluate()
                    children.append(child1)
                    children.append(child2)
                for i in range(0, newindividual):
                    # replce with child
                    totalscore = 0
                    for k in range(0, self.size):
                        totalscore += self.population[k].score
                    randscore = random.random()
                    addscore = 0
                    for j in range(0, self.size):
                        addscore += (self.population[j].score / totalscore)
                        if addscore >= randscore:
                            self.population[j] = children[i]
                            break
            if random.random() < self.mutation_rate:
                selected = self._select()
                self.population[selected].mutate()
        # end loop
        for i in range(0, self.size):
            self.population[i].evaluate()
            curscore = self.population[i].score
            if curscore < self.minscore:
                self.minscore = curscore
                self.minindividual = self.population[i]
        print "..................Result........................."
        print self.minindividual
        # self._printpopulation()

    def _select(self):
        totalscore = 0
        for i in range(0, self.size):
            totalscore += self.population[i].score
        randscore = random.random() * (self.size - 1)
        addscore = 0
        selected = 0
        for i in range(0, self.size):
            addscore += (1 - self.population[i].score / totalscore)
            if addscore >= randscore:
                selected = i
                break
        return selected

    def _selectrank(self, choosebest=0.9):
        self.population.sort()
        if random.random() < choosebest:
            return random.randint(0, self.size * self.newindividualrate)
        else:
            return random.randint(self.size * self.newindividualrate, \
                                  self.size - 1)

    def _printpopulation(self):
        for i in range(0, self.size):
            print "Individual ", i, self.population[i]


def main_run():
    global cm, coords
    # get cities's coords
    coords = cities_random(30)
    #coords=[(0,0),(20000,0),(40000,0),(60000,0),(80000,2),(100000,4),(100000,7),(80000,6),(80000,4),(60000,4),
            #(-200,0),(600,8),(600,10),(60000,12),(60000,14),(60000,16),(60000,19),(60000,22),(60000,25),(60000,28),
            #(60000,33),(60000,38),(60000,42),(60000,46),(60000,50),(60000,55),(60000,60),(60000,66),(60000,72),(60000,80)]
    cm = cartesian_matrix(coords)
    ev = Environment()
    ev.run()



if __name__ == "__main__":
    main_run()