from math import inf, sqrt
from heapq import heappop, heappush

def dijkstras_shortest_path(source_point, destination_point, source_box, dest_box, mesh):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        source_point: starting point of the pathfinder
        destination_point: the ultimate goal the pathfinder must reach
        mesh: pathway constraints the path adheres to

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """
    came_from = {source_point: None}          # maps cells to previous cells on path
    pathcosts = {source_point: 0}       # maps cells to their pathcosts (found so far)
    path = [source_point] #list of the actual point in each box that the path traverses 
    queue = []
    visited_boxes = set(source_box)
    heappush(queue, (0, source_point))  # maintain a priority queue of cells
    
    while queue:
        priority, box = heappop(queue) #pops the smallest number from the heap 
        if box == dest_box:
            return get_final_path(box, came_from), visited_boxes, list(came_from.keys())
        
        # investigate children
        for neighbor, new_point, cost in navigation_edges(mesh, box, point_in_box):
            visited_boxes.append(neighbor)
            # calculate cost along this path to child
            cost_to_child = priority + cost
            if neighbor not in pathcosts or cost_to_child < pathcosts[neighbor]:
                pathcosts[neighbor] = cost_to_child            # update the cost
                came_from[neighbor] = box                         # set the backpointer
                heappush(queue, (cost_to_child, neighbor))     # put the child on the priority queue
            
    return False

def get_final_path(box, came_from):
    if box == None:
        return []
    return get_final_path(came_from[box], came_from) + [box]


def navigation_edges(mesh, box, point_in_box):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        mesh: pathway constraints the path adheres to
        box:
        point_in_box: 

    Returns:
        A list of tuples containing an adjacent box's coordinates, the exact point we will travel to in the adjacent box, 
        and the cost of the distance to travel there from the point in the originating box.

        E.g. from (0,0, 0, 0):
            [((0,1, 0, 1), (0,1), 1),
             ((1,0, 9, 1), (1,0), 1),
             ((1,1, 8, 1), (6,1), 1.4142135623730951),
             ... ]
    """
    res = []
    for neighbor in mesh['adj'][box]:
        # find the point in neighbor box
        x1, x2, y1, y2 = box 
        Nx1, Nx2, Ny1, Ny2 = neighbor
        new_x = (min(x2,Nx2) - max(x1,Nx1))//2 + max(x1,Nx1)  # new_x is between the max of x1,Nx1 and the min of x2,Nx2
        new_y = (min(y2,Ny2) - max(y1,Ny1))//2 + max(y1,Ny1)
        
        #calculate euclidean distance between point_in_box and (new_x, new_y)
        euclidean_distance = sqrt((point_in_box[0] - new_x)**2 + (point_in_box[1] - new_y[1])**2)
        res.append(neighbor, (new_x, new_y), euclidean_distance)

    return res

# TODO: get source and destination box

def find_path (source_point, destination_point, mesh):

    """
    Searches for a path from source_point to destination_point through the mesh

    Args:
        source_point: starting point of the pathfinder
        destination_point: the ultimate goal the pathfinder must reach
        mesh: pathway constraints the path adheres to

    Returns:

        A path (list of points) from source_point to destination_point if exists
        A list of boxes explored by the algorithm
    """

    # Find box with starting point and box with ending point

    # bounds are in format (x1, x2, y1, y2)
    # (x1,y1) is the top left corner
    # (x2,y2) is the bottom right
    source_box = None
    dest_box = None
    for bounds in mesh['boxes']:
        x1, x2, y1, y2 = bounds
        if x1 <= source_point[0] and x2 >= source_point[0] and y1 <= source_point[1] and y2 >= source_point[1]:
            source_box = bounds
        if x1 <= destination_point[0] and x2 >= destination_point[0] and y1 <= destination_point[1] and y2 >= destination_point[1]:
            dest_box = bounds
        if source_box != None and dest_box != None:
            break
    
    if source_box == dest_box:
        return [source_point, destination_point], [source_box], []
    
    return dijkstras_shortest_path(source_point, destination_point, source_box, dest_box, mesh)
        
    # Implement a simple BFS (gives a complete solution)
    found_solution = False
    came_from = {}
    came_from[source_box] = None
    queue = [source_box]
    visited = [source_box]
    while (len(queue) > 0):
        box = queue[0]
        if box == dest_box:
            found_solution = True
            break
        queue.pop(0)
        # go through all neighbors of x
        for neighbor in mesh['adj'][box]:
            if neighbor not in visited:
                queue.append(neighbor)
                visited.append(neighbor)
                came_from[neighbor] = box
    
    if found_solution:
        print("solution exists")
    else:
        print("No path!")
        # TODO: What do we return if no path exists?
        return [], visited, []
        
    # Reconstruct Path that we explored
    traversed = [dest_box]
    path = [destination_point] #the point in the specific box that we are going to/from
    # k = list(came_from.keys())
    # v = list(came_from.values())

    curr = dest_box
    prev = came_from[curr]
    while prev != None:
        # find a new point in the neighbor box to go to
        print("curr is", curr)
        print("prev is", prev)
        x1, x2, y1, y2 = prev 
        Nx1, Nx2, Ny1, Ny2 = curr
        new_x = (min(x2,Nx2) - max(x1,Nx1))//2 + max(x1,Nx1)  # new_x is between the max of x1,Nx1 and the min of x2,Nx2
        new_y = (min(y2,Ny2) - max(y1,Ny1))//2 + max(y1,Ny1)  # new_y is between the max of y1,Ny1 and the min of y2,Ny2
        path.append((new_x,new_y))
        print("new point is", (new_x,new_y))

        traversed.append(prev)

        curr = prev
        prev = came_from[curr]
            

    print("source_box", source_box)
    print("dest_box", dest_box)
    print("source_point", source_point)
    print("destination_point", destination_point)
    print(came_from)

  
    print("\n\n\n")
    path.append(source_point)
    print(path)
    return path, visited, traversed


    # TODO: remove last parametrer from return 
