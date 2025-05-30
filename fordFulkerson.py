from collections import deque

# Run Ford-Fulkerson to find and allocate max satisfied students, returns a flow matrix which 
#tells how much flow is going through each edge
def space_efficient_ford_fulkerson():
    # Create residual graph - for each edge (u,v) we also add reverse edge (v,u)
    residual_graph = [[] for _ in range(n + m + 2)]
    
    # For each edge in original graph, add forward and reverse edges
    for u in range(n + m + 2):
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
    satisfied = 0
    while True:
        visited = [False] * (n + m + 2)
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
            
            # If this is student->class edge, record results 
            if u < n and v >= n and v < n + m:
                class_idx = v - n
                #these are what we are after
                phase1_assignments[u] = class_idx
                class_counts[class_idx] += 1
                satisfied += 1
    
    return satisfied
