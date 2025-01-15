from heapq import *
from math import sqrt

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
        return [source_point, destination_point], [source_box]
    
    # If user picks an area that is not in the NavMesh
    if source_box == None or dest_box == None:
        print("No path!")
        return [], []

    print("source_box, type(source_box)", source_box, type(source_box))
    print("dest_box, type(dest_box)", dest_box, type(dest_box))

        
    # Implement a simple bidirectional A* (gives a complete solution)
    found_solution = False

    came_from_forward = {}
    came_from_forward[source_box] = None
    came_from_backward = {}
    came_from_backward[dest_box] = None

    cost_so_far_forward = {}
    cost_so_far_forward[source_box] = 0
    cost_so_far_backward = {}
    cost_so_far_backward[dest_box] = 0

    frontier = []
    heappush(frontier, (0, source_box, destination_point))
    heappush(frontier, (0, dest_box, source_point))

    traversed_forward = [dest_box]
    traversed_backward = [source_box]

    path_forward = [destination_point] #the point in the specific box that we are going to/from
    path_backward = [source_point]

    detail_points_forward = {} # map boxes to points within them
    detail_points_forward[source_box] = source_point
    detail_points_backward = {} # map boxes to points within them
    detail_points_backward[dest_box] = destination_point

    visited_forward = [source_box]
    visited_backward = [dest_box]

    meeting_box = (0, 0, 0, 0)

    while (len(frontier) > 0) and not found_solution:
        priority, box, goal_point = heappop(frontier)

        # go through all neighbors of x
        for neighbor in mesh['adj'][box]:

            if goal_point == destination_point:

                if neighbor == dest_box:
                    return [source_point, travel_box(detail_points_forward[box], source_box, dest_box), destination_point], [source_box, dest_box]

                if neighbor in visited_backward:
                    visited_forward.append(neighbor)
                    came_from_forward[neighbor] = box
                    meeting_box = neighbor
                    found_solution = True
                    break

                # traverse through boxes using next point instead of box logic
                next_point = travel_box(detail_points_forward[box], box, neighbor)
                new_cost = cost_so_far_forward[box] + point_distance(detail_points_forward[box], next_point)

                # same exact thing as original A*, except it's now the "forward" direction
                if neighbor not in cost_so_far_forward or new_cost < cost_so_far_forward[neighbor]:

                    cost_so_far_forward[neighbor] = new_cost
                    heappush(frontier, (cost_so_far_forward[box] + point_distance(next_point, destination_point), neighbor, destination_point))
                    visited_forward.append(neighbor)
                    came_from_forward[neighbor] = box
                    detail_points_forward[neighbor] = next_point

            elif goal_point == source_point:

                if neighbor == source_box:
                    return [destination_point, travel_box(detail_points_backward[box], source_box, dest_box), source_point], [source_box, dest_box]

                if neighbor in visited_forward:
                    visited_backward.append(neighbor)
                    came_from_backward[neighbor] = box
                    meeting_box = neighbor
                    found_solution = True
                    break

                # again same exact algorithm, except it's another A* going the other direction
                # traverse through boxes using next point instead of box logic
                next_point = travel_box(detail_points_backward[box], box, neighbor)
                new_cost = cost_so_far_backward[box] + point_distance(detail_points_backward[box], next_point)
                # same exact thing as original A*, except it's now the "forward" direction
                if neighbor not in cost_so_far_backward or new_cost < cost_so_far_backward[neighbor]:

                    cost_so_far_backward[neighbor] = new_cost
                    heappush(frontier, (cost_so_far_backward[box] + point_distance(next_point, source_point), neighbor, source_point))
                    visited_backward.append(neighbor)
                    came_from_backward[neighbor] = box
                    detail_points_backward[neighbor] = next_point
    
    if found_solution:
        # reconstruct path from the two halves of bidirectional A*
        box_path = []
        current_box = meeting_box

        # append the first half to the box path
        while current_box:
            box_path.append(current_box)
            current_box = came_from_forward[current_box]
        box_path.reverse()

        # second half
        current_box = came_from_backward[meeting_box]
        while current_box:
            box_path.append(current_box)
            current_box = came_from_backward[current_box]

        point_path = [source_point]
    
        for i in range(1, len(box_path)):
            new_point = travel_box(point_path[-1], box_path[i - 1], box_path[i])
            point_path.append(new_point)
        point_path.append(destination_point)

        return point_path, visited_forward + visited_backward

    else:
        print("No path!")
        return [], visited_forward

def point_distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def travel_box(current_point, curr_box, next_box):
    x1, x2, y1, y2 = curr_box
    Nx1, Nx2, Ny1, Ny2 = next_box

    overlap_min_x = max(x1, Nx1)
    overlap_max_x = min(x2, Nx2)
    overlap_min_y = max(y1, Ny1)
    overlap_max_y = min(y2, Ny2)

    new_x = max(overlap_min_x, min(current_point[0], overlap_max_x))
    new_y = max(overlap_min_y, min(current_point[1], overlap_max_y))

    return new_x, new_y