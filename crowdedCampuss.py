def crowdedCampus(n, m, timePreferences, proposedClasses, minimumSatisfaction):
    """
        Approach description :
        There are two problems we have to solve: 
        Classes that cant take in all the students who prefer it 
        Classes that don't get enough students 

        So there are two phases to solve each problem, 
        Phase 1 is for the first:
        Based on the proposed classes available we connect students to their top 5 classes and try to allocate as many as we can without breaking any max cap. We do this by running ford fulkerson to find max flow on a space efficient bipartite graph. It’ll tell us the max satisfied students possible. 

        check no. of satisfied >= min satisfied, since it'll only get lower from here

        After, we might have classes that didn’t reach their min cap being either:
        Classes that didnt get enough students
        And
        Students who werent allocated since none of the proposed classes were preferences, or their preferred classes were full

        This is solved in phase 2:
        From phase 1, we get the current allocation of students to their preferred classes, the satisfied count, and the class counts. We go through the class counts finding ones without enough students and first assign unallocated students (ones who didnt get their preferred class). If this isnt enough we start sacrificing students in preferred classes.

        At the end we'll have our final allocation, and based on how many students allocated to preferred classes we had to sacrifice, we may have a feasible solution. 

        Also prior checks: 
        Sum of max caps<= No of students <= sum of min caps,
        If these arent met from the start, then the supply and demand is off and there is no possible solution. 

        :Input:
        argv1: n - number of students
        argv2: m - number of classes
        argv3: timePreferences - list of lists, each sublist contains the preferred class times for each student
        argv4: proposedClasses - list of lists, each list contains (class time, min capacity, max capacity) for each class
        argv5: minimumSatisfaction - minimum number of students that must be satisfied with their class allocation
        :Output, return or postcondition: List of allocation for students based on index, or None
        :Time complexity: O(n^2)
        :Time complexity analysis: 
        For both complexities the most important thing to understand is the lowest min capacity for classes is 1, a class must have at least 1 student. 
        So if we check for this, the most number of classes is n, where we have to assign a single student to each class. 

        based on this, our main time complexity is from our ford fulkerson function, which is O(n^2), and 
        any loops where we check each student against each class would also be O(n^2)
        :Space complexity: O(n)
        :Space complexity analysis:
        The bipartite graph and the residual graph are the most space consuming. The bigger of the two the residual, in the worst case,
        holds n edges froms source to students, 
        5n edges from students to their 5 preferred classes and n reverse edges to source
        n edges from classes to sink. 
        Overall is boiled down to O(n) space used. 
    """


    # Check basic requirements
    total_min_capacity = sum(proposedClasses[j][1] for j in range(m))
    total_max_capacity = sum(proposedClasses[j][2] for j in range(m))
    if n < total_min_capacity:
        return None  # Not enough students
    if n > total_max_capacity:
        return None  # Too many students
    
    # PHASE 1: Find maximum satisfied students by matching to preferred classes
    
    # Create space-efficient graph representation
    # Format: For each node, store list of [neighbor, capacity] lists, space used: O(n)
    graph = [[] for _ in range(n + m + 2)]
    source = n + m
    sink = n + m + 1
    
    # Connect source to students with capacity 1, O(n)
    for i in range(n):
        graph[source].append((i, 1))
    
    # Connect students to preferred classes
    for i in range(n):
        top_five_slots = timePreferences[i][:5] # the list slice is constant O(5)
        for j in range(m):
            if proposedClasses[j][0] in top_five_slots:
                # Student i connects to class n+j
                graph[i].append((n + j, 1))
                break
        
    # Connect classes to sink
    for j in range(m):
        class_node = n + j
        max_capacity = proposedClasses[j][2]
        graph[class_node].append((sink, max_capacity))

    # Run Ford-Fulkerson to find and allocate max satisfied students
    phase1_assignments = [-1] * n  # allocation of students (to preferred classes)
    class_counts = [0] * m        # How many students in each class after
    satisfied_count = 0           # Count of satisfied students

    preferredMatches = space_efficient_ford_fulkerson(graph, source, sink)
    print(preferredMatches)
    #For every student, check which class they were assigned to
    for i in range(n):
        for edge in preferredMatches[i][:-1]:  # Skip the last edge, since thats the reverse edge to the source
            if edge[1] == 0:
                class_index = edge[0] - n 
                phase1_assignments[i] = class_index
                class_counts[class_index] += 1
                satisfied_count += 1
                break

    # IF max possible satisfied students is less than minimum satisfaction, return None
    if satisfied_count < minimumSatisfaction:
        return None
    
    #Phase 2 fix any classes with minimum capacity not met


    # Track students assigned to non-preferred classes
    nonPreferredAllocatedStudents = [0] * n
    
    # Handle minimum capacity constraints
    for j in range(m):
        if class_counts[j] < proposedClasses[j][1]:
            deficit = proposedClasses[j][1] - class_counts[j]
            
            # First use unassigned students
            for i in range(n):
                if phase1_assignments[i] == -1 and deficit > 0:
                    phase1_assignments[i] = j
                    nonPreferredAllocatedStudents[i] = 1
                    class_counts[j] += 1
                    deficit -= 1
            
            # If still deficit, sacrifice satisfied students
            if deficit > 0:
                for i in range(n):
                    if (nonPreferredAllocatedStudents[i] != 1 and 
                        deficit > 0 and 
                        phase1_assignments[i] != -1 and
                        (class_counts[phase1_assignments[i]] - 1) >= proposedClasses[phase1_assignments[i]][1]):
                        
                        original_class = phase1_assignments[i]
                        phase1_assignments[i] = j
                        class_counts[j] += 1
                        class_counts[original_class] -= 1
                        deficit -= 1
                        satisfied_count -= 1
    
    # Assign any remaining unassigned students to classes with available capacity
    for i in range(n):
        if phase1_assignments[i] == -1:
            for j in range(m):
                if class_counts[j] < proposedClasses[j][2]:
                    phase1_assignments[i] = j
                    class_counts[j] += 1
                    break
    
    # Final check
    if satisfied_count < minimumSatisfaction:
        return None
        
    return phase1_assignments


def space_efficient_ford_fulkerson(graph, source, sink):
    """
        Function description:
        We use ford-fulkerson with dfs to find the maximum matching in this bipartite graph, through 
        finding max flow. Its residual graph is space-efficient, it stores lists of lists to hold the
        outgoing edges for a node (v, capacity), not through indexes which would be a flow matrix requiring
        O(n^2) space.

        :Input:
        argv1:graph - adjacency list representation of the graph, where each node has a list of [neighbor, capacity]
        argv2: source - the source node index
        argv3: sink - the sink node index

        :Output, return or postcondition: residual_graph
        :Time complexity: O(n^2) worst case
        :Time complexity analysis: with dfs the worst time complex is O(E*max_flow). The max possible flow is n, number of students since we 
        only have n amount of students to assign once. The number of edges is : n (source to students) + 5n (if each student was connected to their 5 preferred classes) + n (classes to sink, the most classes we can have is equal to students since min capacity possible is 1 and sum of min caps =< n) = 7n = n
        therefore O(n^2) in the worst case.
        :Space complexity: O(n)
        :Space complexity analysis: The residual graph takes up the most space, in the worst case we hold edges from students to their 5 preferred classes thus: 5n, edges from source to students n, and edges from classes to sink n. Thus the total space used is O(n).
    """
    total_nodes = len(graph)

    # Create residual graph - for each edge (u,v) we also add reverse edge (v,u)
    residual_graph = [[] for _ in range(total_nodes)]
    # For each edge in original graph, add forward and reverse edges
    for u in range(total_nodes):
        for v, capacity in graph[u]:
            residual_graph[u].append((v, capacity))
            residual_graph[v].append((u, 0))
    
    # DFS to find augmenting path
    def dfs(u, visited, min_capacity_so_far):
        # If we reached the sink, we found a path
        if u == sink:
            return True, min_capacity_so_far, []
        
        visited[u] = True
        
        # Try all outgoing edges
        for idx, (v, capacity) in enumerate(residual_graph[u]):
            if not visited[v] and capacity > 0:
                # Calculate new minimum capacity along this path
                new_min_capacity = min(min_capacity_so_far, capacity)
                
                # Continue DFS from v
                found, path_capacity, path = dfs(v, visited, new_min_capacity)
                
                if found:
                    # Add this edge to the path
                    path.append((u, v, idx))
                    return True, path_capacity, path
        
        return False, 0, []
    
    # Find augmenting paths and update flow
    while True:
        visited = [False] * (total_nodes)
        found, path_capacity, path = dfs(source, visited, float('inf'))
        
        if not found:
            break
            
        # Reverse path to go from source to sink
        path.reverse()
        
        # Update residual capacities
        for u, v, idx in path:
            # Update forward edge
            residual_graph[u][idx] = (residual_graph[u][idx][0], residual_graph[u][idx][1] - path_capacity)
            
            # Find and update reverse edge
            for rev_idx, (rev_v, rev_cap) in enumerate(residual_graph[v]):
                if rev_v == u:
                    residual_graph[v][rev_idx] = (u, rev_cap + path_capacity)
                    break
        
    return residual_graph

