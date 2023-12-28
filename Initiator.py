# from bottom_cluster_generation import Bottom_clusters
import matplotlib.pyplot as plt
from Object import Object
from Query import Skr_query
from Dataspace import Cell
from bottom_cluster_generation import Bottom_clusters
from matplotlib.patches import Rectangle

# Create all objects
objects = []
objects.append(Object([10, 5], ["coffee"]))  # , "breakfast"
objects.append(Object([5, 3], ["delivery"]))
objects.append(Object([7, 6], ["breakfast"]))
objects.append(Object([2, 2], ["dinner"]))  # , "delivery"
objects.append(Object([1, 6], ["dinner", "coffee"]))  # "coffe",
objects.append(Object([4, 8], ["dinner", "coffee"]))
objects.append(Object([0, 0], ["smoothies"]))
objects.append(Object([10, 10], ["coffee"]))

# Create all queries
queries = []
queries.append(Skr_query([[6, 6], [10, 10]], ["coffee"]))
queries.append(Skr_query([[0, 0], [5, 4]], ["dinner"]))

# create the dataspace
dataspace = Cell([[0, 0], [10, 10]], objects)

# visualize all the values
area = dataspace.get_area()
for j in range(1 + area[1][1]):
    plt.plot(0, j, "|", color="blue")
    plt.plot(area[1][0], j, "|", color="blue")

for i in range(1 + area[1][0]):
    plt.plot(i, 0, "_", color="blue")
    plt.plot(i, area[1][1], "_", color="blue")


for k in queries:
    area = k.get_area()
    for j in range(area[0][1], 1 + area[1][1]):
        plt.plot(area[0][0], j, "|", color="red")
        plt.plot(area[1][0], j, "|", color="red")
    for i in range(area[0][0], 1 + area[1][0]):
        plt.plot(i, area[0][1], "_", color="red")
        plt.plot(i, area[1][1], "_", color="red")


for i in objects:
    x, y = i.get_location()
    plt.plot(x, y, "*", color="green")
    plt.annotate(i.get_kws(), [x, y])

plt.title("2D dataspace with queries")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.show()

# Generate the bottom clusters
b_clusters_gen = Bottom_clusters(queries, dataspace)
bottom_clust = b_clusters_gen.generate_bottom_clusters()

# Visualize the bottom cluser dimensions
for i in bottom_clust:
    area = i.get_area()
    for j in range(area[0][1], 1 + area[1][1]):
        plt.plot(area[0][0], j, "|", color="orange")
        plt.plot(area[1][0], j, "|", color="orange")

    for i in range(area[0][0], 1 + area[1][0]):
        plt.plot(i, area[0][1], "_", color="orange")
        plt.plot(i, area[1][1], "_", color="orange")


plt.title("Area of the bottom clusters")
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.show()
