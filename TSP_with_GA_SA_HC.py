import random 
import math
from time import time
#-------------------Total Distance Calculating-------------------#

def total_distance(solution, distances):
    # Calculate the total distance of the route represented by the solution
    distance = 0
    for i in range(len(solution) - 1):
        distance += distances[solution[i]][solution[i + 1]]
    return distance

#-------------------Genetic Algorithm-------------------#

def tsp_genetic_algorithm(cities, distances, population_size, num_generations, mutation_rate):
    # Initialize the population with random routes
    population = [random_route(cities) for _ in range(population_size)]
    
    # Generate a random route as the best solution
    best_solution = random_route(cities)
    
    # Loop for the specified number of generations
    for _ in range(num_generations):
        # Calculate the fitness of each route
        fitness = [route_fitness(route, distances) for route in population]
        
        # Find the index of the fittest route in the population
        fittest_index = fitness.index(max(fitness))
    
        # Get the fittest route from the final population
        fittest_route = population[fittest_index]
        
        # Update the best solution if the fittest route is better
        if total_distance(fittest_route, distances) < total_distance(best_solution, distances) :
            best_solution = fittest_route
            print("İteration:", str(_) , "// Best Solution Changed:", str(best_solution))
            
            
        # Select the fittest routes for breeding
        breeding_pool = select_fittest(population, fitness, num_breeders=population_size)
        
        # Create the next generation of routes by breeding the fittest routes
        population = breed_routes(breeding_pool, mutation_rate)
        
        
    # Return the best solution and its total distance
    return best_solution, total_distance(best_solution, distances)


def random_route(cities):
    # Create a random route by shuffling the list of cities
    route = cities.copy()
    random.shuffle(route)
    return route

def select_fittest(population, fitness, num_breeders):
    # Select the fittest routes from the population for breeding
    breeders = []
    for _ in range(num_breeders):
        # Select the fittest route based on its fitness score
        fittest_index = fitness.index(max(fitness))
        breeders.append(population[fittest_index])
        # Remove the selected route from the population
        population.pop(fittest_index)
        fitness.pop(fittest_index)
    return breeders

def breed_routes(breeding_pool, mutation_rate):
    # Create the next generation of routes by breeding the fittest routes
    next_generation = []
    for i in range(len(breeding_pool)):
        # Select two routes for breeding
        parent1 = breeding_pool[i]
        parent2 = breeding_pool[(i + 1) % len(breeding_pool)]
        # Breed the routes to create a new route
        child = breed(parent1, parent2)
        # Add the new route to the next generation, with a chance of mutation
        next_generation.append(mutate(child, mutation_rate))
    return next_generation

def breed(route1, route2):
    # Breed two routes to create a new route by combining part of each route
    start = random.randint(0, len(route1) - 1)
    end = random.randint(start + 1, len(route1))
    child = route1[start:end]
    for city in route2:

        if city not in child:
            child.append(city)
    return child

def mutate(route, mutation_rate):
    # Mutate a route by swapping two cities in the route
    for i in range(len(route)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(route) - 1)
            route[i], route[j] = route[j], route[i]
    return route

def distance_between(city1, city2, distances):
    # Look up the distance between two cities in the distance matrix
    distance = distances[city1][city2]
    return distance

def route_fitness(route, distances):
    # Calculate the fitness of a route as the total distance of the route
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distance_between(route[i], route[i + 1], distances)
    return 1 / total_distance

#-------------------Hill Climbing Algorithm-------------------#


def tsp_hill_climbing(cities, distances, num_iterations):
    global counter
    # Initialize the list of cities
    city_list = cities.copy()
    # Generate a random starting solution
    current_solution = random.sample(city_list, len(city_list))
    # Set the best solution to be the starting solution
    best_solution = current_solution
    # Loop until there are no more iterations to be done
    for i in range(num_iterations):
        # Generate a list of all the possible neighbors of the current solution
        neighbors = []
        for j in range(len(current_solution)):
            # Generate a random current solution
            current_solution = random.sample(city_list, len(city_list))
            # Create a copy of the current solution
            temp = current_solution.copy()
            # Swap the jth element with the next element
            temp[j], temp[(j+1) % len(temp)] = temp[(j+1) % len(temp)], temp[j]
            # Add the modified solution to the list of neighbors
            neighbors.append(temp)
        # Calculate the total distance for each neighbor
        neighbor_distances = [total_distance(n, distances) for n in neighbors]
        # Find the index of the neighbor with the best distance
        best_index = neighbor_distances.index(min(neighbor_distances))
        # Set the current solution to be the best neighbor
        current_solution = neighbors[best_index]
        # If the current solution is better than the best solution, update the best solution
        if total_distance(current_solution, distances) < total_distance(best_solution, distances):  
            best_solution = current_solution
            print("Iteration: " + str(i)  + " // Best Solution Changed: " + str(best_solution))
        # Return the best solution
    print("")
    return best_solution, total_distance(best_solution, distances)


#-------------------Simulated Annealing Algorithm-------------------#

def tsp_simulated_annealing(cities, distances, num_iterations, temperature):
    # Set the initial solution to be a random permutation of the cities
    current_solution = random.sample(cities, len(cities))
    best_solution = current_solution.copy()

    # Loop for the specified number of iterations
    for i in range(num_iterations):
        # Generate a random new solution by swapping two cities in the current solution
        new_solution = current_solution.copy()
        a = random.randint(0, len(cities) - 1)
        b = random.randint(0, len(cities) - 1)
        new_solution[a], new_solution[b] = new_solution[b], new_solution[a]
        
        # Calculate the difference in distance between the current and new solutions
        current_distance = total_distance(current_solution, distances)
        new_distance = total_distance(new_solution, distances)
        diff = new_distance - current_distance
        
        # If the new solution is better, accept it
        if diff < 0:
            current_solution = new_solution
            if new_distance < total_distance(best_solution, distances):
                best_solution = new_solution
                print("Iteration: " + str(i)  + " // Best Solution Changed: " + str(best_solution) + " // Temperature: " + str(temperature))
        
        # If the new solution is worse, accept it with a certain probability
        else:
            probability = math.exp(-diff / temperature)
            if random.uniform(0, 1) < probability:
                current_solution = new_solution
        
        # Decrease the temperature
        temperature -= 1
    print("")
    # Return the best solution found
    return best_solution, total_distance(best_solution, distances)




#-------------------Main-------------------#


# Define the cities and their distances
        

cities = ["Bilecik", "Eskisehir", "Istanbul", "Bursa", "Kutahya", "Ankara", "Bolu", "Balikesir", "Muğla", "İzmir", "Antalya", "Trabzon"]
distances = {
    "Bilecik": {"Eskisehir": 80, "Istanbul": 200, "Bursa": 105, "Kutahya": 110, "Ankara": 317, "Bolu": 216, "Balikesir": 240, "Muğla": 512, "İzmir": 441, "Antalya": 477, "Trabzon": 1014},
    "Eskisehir": {"Bilecik": 80, "Istanbul": 306, "Bursa": 156, "Kutahya": 78, "Ankara": 235, "Bolu": 217, "Balikesir": 303, "Muğla": 478, "İzmir": 416, "Antalya": 417, "Trabzon": 978},
    "Istanbul": {"Bilecik": 200, "Eskisehir": 306, "Bursa": 154, "Kutahya": 331, "Ankara": 444, "Bolu": 258, "Balikesir": 281, "Muğla": 670, "İzmir": 480, "Antalya": 697, "Trabzon": 1058},
    "Bursa": {"Bilecik": 105, "Eskisehir": 156, "Istanbul": 154, "Kutahya": 182, "Ankara": 388, "Bolu": 273, "Balikesir": 144, "Muğla": 535, "İzmir": 345, "Antalya": 546, "Trabzon": 1091},
    "Kutahya": {"Bilecik": 110, "Eskisehir": 78, "Istanbul": 331, "Bursa": 182, "Ankara": 315, "Bolu": 304, "Balikesir": 225 , "Muğla": 402, "İzmir": 340, "Antalya": 367, "Trabzon": 1059},
    "Ankara": {"Bilecik": 317, "Eskisehir": 235, "Istanbul": 444, "Bursa": 388, "Kutahya": 315, "Bolu": 187, "Balikesir": 535, "Muğla": 623, "İzmir": 590, "Antalya": 477, "Trabzon": 729},
    "Bolu": {"Bilecik": 216, "Eskisehir": 217, "Istanbul": 258, "Bursa": 273, "Kutahya": 304, "Ankara": 187, "Balikesir": 416, "Muğla": 722, "İzmir": 617, "Antalya": 604, "Trabzon": 800},
    "Balikesir": {"Bilecik": 240, "Eskisehir": 303, "Istanbul": 281, "Bursa": 144, "Kutahya": 225, "Ankara": 535, "Bolu": 416, "Muğla": 394, "İzmir": 202, "Antalya": 527, "Trabzon": 1217},
    "Muğla": {"Bilecik": 512, "Eskisehir": 478, "Istanbul": 670, "Bursa": 535, "Kutahya": 402, "Ankara": 623, "Bolu": 722, "Balikesir": 394, "İzmir": 211, "Antalya": 314, "Trabzon": 1363},
    "İzmir": {"Bilecik": 441, "Eskisehir": 416, "Istanbul": 480, "Bursa": 345, "Kutahya": 340, "Ankara": 590, "Bolu": 617, "Balikesir": 202, "Muğla": 211, "Antalya": 457, "Trabzon": 1330},
    "Antalya": {"Bilecik": 477, "Eskisehir": 417, "Istanbul": 697, "Bursa": 546, "Kutahya": 367, "Ankara": 477, "Bolu": 604, "Balikesir": 527, "Muğla": 312, "İzmir": 459, "Trabzon": 1218},
    "Trabzon": {"Bilecik": 1014, "Eskisehir": 978, "Istanbul": 1058, "Bursa": 1091, "Kutahya": 1059, "Ankara": 729, "Bolu": 800, "Balikesir": 1217, "Muğla": 1362, "İzmir": 1330, "Antalya": 1218}
}




print("------------------------------------------------------------------")
print("Genetic Algorithm")
print("------------------------------------------------------------------\n")
tiempo_inicial = time()
# Test the genetic algorithm with the fixed distances
solution_genetic, total_distance_genetic = tsp_genetic_algorithm(cities, distances=distances, population_size=400, num_generations=250, mutation_rate=0.01)

print(f"Final Solution for GA: {solution_genetic}")
print(f"Total distance: {total_distance_genetic} \n")
tiempo_final_gen = time()
print("") 
print("Total time: ",(tiempo_final_gen - tiempo_inicial)," secs.\n")


print("------------------------------------------------------------------")
print("Hill Climbing")
print("------------------------------------------------------------------\n")
# Test the hill climbing algorithm with the fixed distances
solution_HC, total_distance_HC = tsp_hill_climbing(cities, distances, num_iterations=8400)

print(f"Final Solution for HC: {solution_HC}")
print(f"Total distance: {total_distance_HC} \n")
tiempo_final_HC = time()
print("")
print("Total time: ",(tiempo_final_HC - tiempo_final_gen)," secs.\n")


print("------------------------------------------------------------------")
print("Simulated Annealing")
print("------------------------------------------------------------------\n")
# Test the simulated annealing algorithm with the fixed distances
solution_SA, total_distance_SA = tsp_simulated_annealing(cities, distances, num_iterations=100000, temperature=100000)

print("Final Solution for SA: " + str(solution_SA))
print("Total Distance: " + str(total_distance_SA))
print("")
print("Total time: ",(time() - tiempo_final_HC)," secs.\n")






