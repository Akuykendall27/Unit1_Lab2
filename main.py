# Abel D Kuykendall
# 9/5/24
# CPAPROG 2nd year
# Rat generation simulator

from rat import Rat
from random import triangular, uniform, choice, random, shuffle
from time import time

GOAL = 50000                # Target average weight (grams)
NUM_RATS = 20               # Max adult rats in the lab
INITIAL_MIN_WT = 200        # The smallest rat (grams)
INITIAL_MAX_WT = 600        # The chonkiest rat (grams)
INITIAL_MODE_WT = 300       # The most common weight (grams)
MUTATE_ODDS = 0.01          # Liklihood of a mutation
MUTATE_MIN = 0.5            # Scalar mutation - least beneficial
MUTATE_MAX = 1.2            # Scalar mutation - most beneficial
LITTER_SIZE = 8             # Pups per litter (1 mating pair)
GENERATIONS_PER_YEAR = 10   # How many generations are created each year
GENERATION_LIMIT = 500      # Generational cutoff - stop breeded no matter what

def calculate_weight(sex:str, mother:Rat, father:Rat):
    max = float(father.getWeight())
    min = float(mother.getWeight())

    if sex == "M":
      wt = int(triangular(min, max, max))
    else:
      wt = int(triangular(min, max, min))
    return wt

def mutate(pups):
  """Check for mutability, modify weight of affected pups"""
  for pup in pups:
      individual_check = MUTATE_ODDS >= random()
      if individual_check:
          pup.weight *= uniform(MUTATE_MIN, MUTATE_MAX)
  return pups

def calculate_mean(rats):
  '''Calculate the mean weight of a population'''
  sumWt = 0
  numRats = 0
  for r in rats:
    for rat in r:
        sumWt += rat.getWeight()
        numRats += 1
  return sumWt // numRats

def fitness(rats):
  """Determine if the target average matches the current population's average"""
  mean = calculate_mean(rats)
  return mean >= GOAL, mean

def initial_population():
  '''Create the initial set of rats based on constants'''
  rats = [[],[]]
  mother = Rat("F", INITIAL_MIN_WT)
  father = Rat("M", INITIAL_MAX_WT)

  for r in range(NUM_RATS):
    if r < 10:
      sex = "M"
      ind = 0
    else:
      sex = "F"
      ind = 1

    wt = calculate_weight(sex, mother, father)
    R = Rat(sex, wt)
    rats[ind].append(R)

  return rats

def breed(rats):
    children=[]
    shuffle(rats[1])

    for row in rats:
        for r in row:
            r.litters += 1

    for i in range(10):
        for a in range(8):
            sex = choice(["M", "F"])
            children.append(Rat(sex, calculate_weight(sex, rats[0][i], rats[1][i])))

    return children

def combine_population(rats, pups):
    male = []
    female = []
    male.extend(rats[0])
    female.extend(rats[1])

    for pup in pups:
        if pup.getSex() == "M":
            male.append(pup)
        else:
            female.append(pup)
    return [male, female]

def select(rats):
    rats[0].sort(reverse=True)
    rats[0][:] = rats[0][:10]
    rats[1].sort(reverse=True)
    rats[1][:] = rats[1][:10]
    largest = None
    if rats[1][0] < rats[0][0]:
        largest = rats[0][0]
    else:
        largest = rats[1][0]
    return rats, largest

def final_output(data):
    mean = data[0]
    gen = data[1]
    duration = data[2]
    simdur = data[3]
    largest = data[4]
    genaverages = data[5]

    print("RESULTS".center(20,"~"))
    print(f"Final Population Mean: {mean}")
    print(f"Experiment Duration: {duration}")
    print(f"Simulation Duration: {simdur}")
    print(f"\nThe Largest Rat: \n({largest.getSex()}) - {int(largest.getWeight())}")
    print(f"\nGeneration weight averages (GRAMS)")
    final = ""
    for i in genaverages:
        final += f"\t{i}"
    print(final)

def main():
    rats = mutate(initial_population())
    pop = []
    generations = 0
    mean = 0
    means = []
    flag = False
    largestRat = Rat("M", 0)
    start = time()
    while flag == False and generations < GENERATION_LIMIT:
        print(generations, "running")
        pups = mutate(breed(rats))
        rats = combine_population(rats, pups)
        rats, largest = select(rats)
        flag, mean = fitness(rats)
        if largestRat < largest:
            largestRat = largest
        means.append(int(mean))
        generations += 1
    end = time()

    final_output([mean, generations, generations / GENERATIONS_PER_YEAR, end - start, largestRat, means])

if __name__ == "__main__":
    main()
