import queue
from Dataspace import Cell


class Bottom_clusters:
    def __init__(self, query_workload, dataspace):
        self.priority_queue = queue.PriorityQueue()
        self.query_workload = query_workload
        self.dataspace = dataspace

    def generate_bottom_clusters(self):
        """
        The Dataspace is partitioned into subspaces, each subspace is going into the queue
        Pop from queue we get the subspace with the most intersecting queries

        For each subspace we check if it is worthit to split further, by calculating its cost and comparing it to the best splitting costs

        The subspace have values:
            {Area , the queries intersecting , the objects in it, all the types of keywords}
        these are used mostly used to find the object checking cost |Os| of the spaces

        The Machine learning models are going to get rid of the values Objects and keywords
        """

        bottom_clusters = []

        subspace = {
            "area": self.dataspace.get_area(),
            "queries": None,
            "objects": self.dataspace.get_objects(),
            "keywords": self.dataspace.get_kws(),
        }
        subspace["queries"] = self.find_intersecting_queries(
            subspace["area"], self.dataspace.get_kws(), self.query_workload
        )
        # queue prioritizes min first. use "-" to reverce it
        priority = -len(subspace["queries"])
        count = 0  # i used to solve error of the priority queue
        # the problem is when priorities are equal that it compares dictionaries(it cant)
        self.enqueue(subspace, priority, count)

        while not self.priority_queue.empty():
            queries_num, c, sub = self.dequeue()
            queries_num *= -1

            cost = self.find_cost(sub["objects"], sub["queries"])

            # finding the optimal partition
            x_optimal = self.find_optimal_partition(sub, "x")
            y_optimal = self.find_optimal_partition(sub, "y")
            optimal_partition = (
                x_optimal if x_optimal["cost"] <= y_optimal["cost"] else y_optimal
            )

            # finding if split is worth it
            # Cs - w2*Best.cost > w1*|W|
            # w1*|W| = clusters times number of queries
            # w1 = time to check 1 bottom cluster FIXED
            # w2 = time to check 1 keyrord FIXED
            w2 = 1  # I do not know what to put
            w1 = 1  # I do not know what to put

            # If the decrease in Object checking cost is greater, > , than the increase in cluster checking cost
            if cost - w2 * optimal_partition["cost"] > queries_num * w1:
                # then make the split

                sub1, sub2 = self.split_space(sub, optimal_partition)
                prior1 = -len(sub1["queries"])
                prior2 = -len(sub2["queries"])

                count += 1
                self.enqueue(sub1, prior1, count)
                count += 1
                self.enqueue(sub2, prior2, count)

            else:
                # set it as a bottom cluster
                cell = Cell(sub["area"], sub["objects"])
                bottom_clusters.append(cell)

        return bottom_clusters

    def find_optimal_partition(self, sub, dimension):
        """
        Creates and returnes Dictionary with the optimal
        Dimension, Cost, Partition-> the place where the split happens
        """
        optimal = {"dimension": dimension}

        # aim to find the optimal split for Σ|Os|
        optimal["cost"], optimal["partition"] = self.brute_force_splitting(
            sub, dimension
        )

        return optimal

    def brute_force_splitting(self, sub, dimension):
        """

        Calculates for each possible partition of the subspace in the given dimension
        The Accurate cost and compares it with the best found

        """
        # find the Borders min max
        area = sub["area"]
        dim = 1
        if dimension == "x":
            dim = 0
        minimum = area[0][dim]
        maximum = area[1][dim]

        opt_cost = None
        opt_partition = None

        # Check the split cost for each possible partition
        for split in range(minimum, maximum):
            # find the objects and keywords in each subspace
            subspace1_objects = []
            subspace1_kws = []
            subspace2_objects = []
            subspace2_kws = []
            for j in sub["objects"]:
                object_kws = j.get_kws()
                location = j.get_location()
                if location[dim] <= split:
                    subspace1_objects.append(j)
                    for k in object_kws:
                        if k not in subspace1_kws:
                            subspace1_kws.append(k)
                else:
                    subspace2_objects.append(j)
                    for k in object_kws:
                        if k not in subspace2_kws:
                            subspace2_kws.append(k)

            # find the area of the 2 subspaces
            if dim == 0:
                subspace1_area = [[area[0][0], area[0][1]], [split, area[1][1]]]
                subspace2_area = [[split, area[0][1]], [area[1][0], area[1][1]]]
            else:
                subspace1_area = [[area[0][0], area[0][1]], [area[1][0], split]]
                subspace2_area = [[area[0][0], split], [area[1][0], area[1][1]]]

            # Find the queries intersecting with each subspace
            subspace1_queries = self.find_intersecting_queries(
                subspace1_area, subspace1_kws, sub["queries"]
            )
            subspace2_queries = self.find_intersecting_queries(
                subspace2_area, subspace2_kws, sub["queries"]
            )

            # calculating the Σ|Os|
            object_checking_cost = self.find_cost(subspace1_objects, subspace1_queries)
            object_checking_cost += self.find_cost(subspace2_objects, subspace2_queries)

            # Checking if the cost is better that the others before
            if (opt_cost == None) or (opt_cost > object_checking_cost):
                opt_cost = object_checking_cost
                opt_partition = split

        return opt_cost, opt_partition

    def enqueue(self, subspace, priority, count):
        # queue prioritises the smallest number's

        # Error occures if priorities are equal
        self.priority_queue.put((priority, count, subspace))

    def dequeue(self):
        if not queue:
            return None
        return self.priority_queue.get()

    def find_cost(self, subspace_objects, querie_workload):
        """

        Calculating object cost: Σ|Os|

        Find all objects that have at least 1 keyword incomon with each querie

        It goes through all the objects and finds with how many queries does it have 1 keyword incomon
        """

        object_checking_cost = 0
        for i in subspace_objects:
            obj_kws = i.get_kws()
            for j in querie_workload:
                q_kws = j.get_kws()
                for k in obj_kws:
                    if k in q_kws:
                        object_checking_cost += 1
                        break

        return object_checking_cost

    def intersection(self, a, b):
        """

        This compares the intersection only for one dimension
        2 matrices a,b with values [min, max]

        """
        if a[0] > b[1]:
            return False  # If min of one is biger than the max of the other than
        if b[0] > a[1]:
            return False

        return True  # they are intersecting

    def find_intersecting_queries(self, area, kws, queries):
        # returns array with all the querie objects that intersect
        queries_intersecting = []

        for i in queries:
            q_area = i.get_area()
            q_kws = i.get_kws()

            # checking intersection for dimension x and for y
            if self.intersection(
                [q_area[0][0], q_area[1][0]], [area[0][0], area[1][0]]
            ) & self.intersection(
                [q_area[0][1], q_area[1][1]], [area[0][1], area[1][1]]
            ):
                # checking keywords
                for j in q_kws:
                    if j in kws:
                        queries_intersecting.append(i)
                        break

        return queries_intersecting

    def split_space(self, space, best):
        sub1 = {"area": [], "queries": None, "objects": [], "keywords": []}
        sub2 = {"area": [], "queries": None, "objects": [], "keywords": []}

        # find the area of the subspaces
        split = best["partition"]
        if best["dimension"] == "x":
            sub1["area"] = [
                [space["area"][0][0], space["area"][0][1]],
                [split, space["area"][1][1]],
            ]
            sub2["area"] = [
                [split, space["area"][0][1]],
                [space["area"][1][0], space["area"][1][1]],
            ]
        else:
            sub1["area"] = [
                [space["area"][0][0], space["area"][0][1]],
                [space["area"][1][0], split],
            ]
            sub2["area"] = [
                [space["area"][0][0], split],
                [space["area"][1][0], space["area"][1][1]],
            ]

        dim = 1
        if best["dimension"] == "x":
            dim = 0

        # append the objects for each subspace
        for i in space["objects"]:
            obj_loc = i.get_location()
            obj_kws = i.get_kws()

            # if the object location is lower or higher than the split value
            if obj_loc[dim] - sub1["area"][1][dim] <= 0:
                sub1["objects"].append(i)
                # check if object added has a new keyword for the subspace
                for k in obj_kws:
                    if k not in sub1["keywords"]:
                        sub1["keywords"].append(k)
            else:
                sub2["objects"].append(i)
                for k in obj_kws:
                    if k not in sub2["keywords"]:
                        sub2["keywords"].append(k)

        # Find the queries intersecting
        sub1["queries"] = self.find_intersecting_queries(
            sub1["area"], sub1["keywords"], space["queries"]
        )
        sub2["queries"] = self.find_intersecting_queries(
            sub2["area"], sub2["keywords"], space["queries"]
        )

        return sub1, sub2
