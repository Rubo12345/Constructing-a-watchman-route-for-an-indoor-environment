from random import randint
import math
import time

def genes(len_paths):
	global GENES
	GENES = ""

	for i in range(len_paths):
		GENES += chr(65+i)

# starting point
START = 0

# Initial population size for the algorithm
POP_SIZE = 10


class Individual:
	def __init__(self) -> None:
		self.gnome = ""
		self.fitness = 0

	def __lt__(self, other):
		return self.fitness < other.fitness

	def __gt__(self, other):
		return self.fitness > other.fitness


def rand_num(start, end):
	return randint(start, end-1)


# Function to check if the character
# has already occurred in the string
def repeat(gnome, ch):
	'''

	Args:
		gnome: The current gene
		ch: The character being added to the new gene

	Return: Boolean True or False

	'''
	for i in range(len(gnome)):
		if gnome[i] == ch:
			return True
	return False


def crossover(gnome, path_length):
	'''

	Args:
		gnome: GNOME is a string
		path_length: Length of paths 2 adjacency matrix that you get from A* or Dijkstra

	Returns:
			mutated GNOME
	'''
	gnome = list(gnome)
	while True:
		r = rand_num(1, path_length)
		r1 = rand_num(1, path_length)
		if r1 != r:
			temp = gnome[r]
			gnome[r] = gnome[r1]
			gnome[r1] = temp
			break
	return ''.join(gnome)


# Function to return a valid GNOME string
# required to create the population
def create_gnome(path_length):
	'''

	Args:
		path_length: Length of paths 2 adjacency matrix that you get from A* or Dijkstra

	Returns:
			The created genome
	'''
	gnome = "0"
	while True:
		if len(gnome) == path_length:
			gnome += gnome[0]
			break

		temp = rand_num(1, path_length)
		if not repeat(gnome, chr(temp + 48)):
			gnome += chr(temp + 48)

	return gnome


# Function to return the fitness value of a gnome.
# The fitness value is the path length
# of the path represented by the GNOME.
def cal_fitness(gnome, paths):
	'''

	Args:
		gnome: The gene, a string which represents the order of cities
		paths: Paths is a 2 adjacency matrix that you get from A* or Dijkstra

	Returns: Fitness value for that gene

	'''
	fitness = 0
	for i in range(len(gnome) - 1):
		fitness += paths[ord(gnome[i]) - 48][ord(gnome[i + 1]) - 48]

	return fitness


# This function is a stopping condition for the genetic algorithm
# Otherwise the genetic algorithm will keep on running
def cooldown(temp):
	'''

	Args:
		temp: Current temperature

	Returns: Cooldown Temperature

	'''
	return (99 * temp) / 100



def genetic_search(paths):
	'''

	Args:
		paths: The 2d adj matrix which contains all the path lengths

	Returns: None

	'''
	start_time = time.time()
	genes(len(paths))
	# To keep track of minimum path length
	min_path = math.inf
	track = 0
	# Generation Number
	gen = 1
	# Number of Gene Iterations
	gen_thres = 5000

	population = []
	temp = Individual()

	# Create initial pop and check their fitness
	for i in range(POP_SIZE):
		temp.gnome = create_gnome(len(paths))
		temp.fitness = cal_fitness(temp.gnome, paths)
		population.append(temp)

	# print("\nInitial population: \nGNOME	 FITNESS VALUE\n")
	# for i in range(POP_SIZE):
	# 	print(population[i].gnome, population[i].fitness)
	# print()

	# Initial temperature, hyperparameter can be tuned
	temperature = 10000000

	# Perform genetic mutation
	while temperature > 1000 and gen <= gen_thres:
		population.sort()
		# print("\nCurrent temp: ", temperature)
		new_population = []

		for i in range(POP_SIZE):
			p1 = population[i]

			while True:
				child = crossover(p1.gnome, len(paths))
				new_gnome = Individual()
				new_gnome.gnome = child
				new_gnome.fitness = cal_fitness(new_gnome.gnome, paths)

				if new_gnome.fitness <= population[i].fitness:
					new_population.append(new_gnome)
					break

				else:

					# allowing a worse child to get into the population for mutation
					prob = math.exp(-1*((new_gnome.fitness-population[i].fitness)/temperature))
					if prob > 0.5:
						new_population.append(new_gnome)
						break

		temperature = cooldown(temperature)
		population = new_population
		# print("Generation", gen)
		# print("GNOME	 FITNESS VALUE")

		for i in range(POP_SIZE):
			# print(population[i].gnome, population[i].fitness)
			if min_path > population[i].fitness:
				min_path = population[i].fitness
				track = gen
				f_time = time.time()-start_time
		gen += 1
		# print('--------------------------')

	print(f'Final path length, traversal order and corresponding generation it was found at are {min_path, track}')
	print(f'The time it took for genetic algorithm is {f_time}')
	print('----------------------------------')