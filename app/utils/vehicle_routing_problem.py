
import haversine as hs
from haversine import Unit

from ortools.constraint_solver import routing_enums_pb2, pywrapcp

matrix1 = [
    [0, 482, 1142, 1107, 1243, 1183, 1374, 2054, 2538, 2411, 1717, 1671, 773, 990, 553, 2273],
    [482, 0, 893, 1126, 1512, 1444, 1705, 2405, 2946, 2844, 2197, 2126, 1252, 909, 1003, 2696],
    [1142, 893, 0, 617, 1323, 1258, 1603, 2250, 2909, 2897, 2682, 2743, 1704, 370, 1674, 3385],
    [1107, 1126, 617, 0, 727, 667, 1014, 1637, 2306, 2314, 2297, 2446, 1381, 273, 1518, 3124],
    [1243, 1512, 1323, 727, 0, 70, 289, 940, 1585, 1587, 1769, 2023, 1051, 953, 1391, 2711],
    [1183, 1444, 1258, 667, 70, 0, 347, 1010, 1651, 1646, 1780, 2020, 1029, 888, 1352, 2709],
    [1374, 1705, 1603, 1014, 289, 347, 0, 701, 1310, 1299, 1575, 1876, 1006, 1232, 1411, 2555],
    [2054, 2405, 2250, 1637, 940, 1010, 701, 0, 700, 817, 1745, 2147, 1547, 1885, 1998, 2768],
    [2538, 2946, 2909, 2306, 1585, 1651, 1310, 700, 0, 299, 1691, 2141, 1886, 2539, 2346, 2651],
    [2411, 2844, 2897, 2314, 1587, 1646, 1299, 817, 299, 0, 1413, 1865, 1713, 2527, 2164, 2357],
    [1717, 2197, 2682, 2297, 1769, 1780, 1575, 1745, 1691, 1413, 0, 452, 985, 2376, 1223, 1023],
    [1671, 2126, 2743, 2446, 2023, 2020, 1876, 2147, 2141, 1865, 452, 0, 1066, 2477, 1123, 688],
    [773, 1252, 1704, 1381, 1051, 1029, 1006, 1547, 1886, 1713, 985, 1066, 0, 1417, 462, 1743],
    [990, 909, 370, 273, 953, 888, 1232, 1885, 2539, 2527, 2376, 2477, 1417, 0, 1468, 3139],
    [553, 1003, 1674, 1518, 1391, 1352, 1411, 1998, 2346, 2164, 1223, 1123, 462, 1468, 0, 1720],
    [2273, 2696, 3385, 3124, 2711, 2709, 2555, 2768, 2651, 2357, 1023, 688, 1743, 3139, 1720, 0],
]

matrix2 =[
    [0, 548, 776, 696, 582, 274, 502, 194, 308, 194, 536, 502, 388, 354, 468, 776, 662],
    [548, 0, 684, 308, 194, 502, 730, 354, 696, 742, 1084, 594, 480, 674, 1016, 868, 1210],
    [776, 684, 0, 992, 878, 502, 274, 810, 468, 742, 400, 1278, 1164, 1130, 788, 1552, 754],
    [696, 308, 992, 0, 114, 650, 878, 502, 844, 890, 1232, 514, 628, 822, 1164, 560, 1358],
    [582, 194, 878, 114, 0, 536, 764, 388, 730, 776, 1118, 400, 514, 708, 1050, 674, 1244],
    [274, 502, 502, 650, 536, 0, 228, 308, 194, 240, 582, 776, 662, 628, 514, 1050, 708],
    [502, 730, 274, 878, 764, 228, 0, 536, 194, 468, 354, 1004, 890, 856, 514, 1278, 480],
    [194, 354, 810, 502, 388, 308, 536, 0, 342, 388, 730, 468, 354, 320, 662, 742, 856],
    [308, 696, 468, 844, 730, 194, 194, 342, 0, 274, 388, 810, 696, 662,320, 1084, 514],
    [194, 742, 742, 890, 776, 240, 468, 388, 274, 0, 342, 536, 422, 388, 274, 810, 468],
    [536, 1084, 400, 1232, 1118, 582, 354, 730, 388, 342, 0, 878, 764, 730, 388, 1152, 354],
    [502, 594, 1278, 514, 400, 776, 1004, 468, 810, 536, 878, 0, 114, 308, 650, 274, 844],
    [388, 480, 1164, 628, 514, 662, 890, 354, 696, 422, 764, 114, 0, 194, 536, 388, 730],
    [354, 674, 1130, 822, 708, 628, 856, 320, 662, 388, 730, 308, 194, 0, 342, 422, 536],
    [468, 1016, 788, 1164, 1050, 514, 514, 662, 320, 274, 388, 650, 536, 342, 0, 764, 194],
    [776, 868, 1552, 560, 674, 1050, 1278, 742, 1084, 810, 1152, 274, 388, 422, 764, 0, 798],
    [662, 1210, 754, 1358, 1244, 708, 480, 856, 514, 468, 354, 844, 730, 536, 194, 798, 0],
]

locations = [
    (11.53348, -72.91773, 3),
    (11.53241, -72.92202, 1),
    (11.53917, -72.92646, 4),
    (11.54254, -72.92196, 8),
    (11.54446, -72.91558, 13),
    (11.54399, -72.91601, 35),
    (11.54493, -72.91297, 6),
    (11.5498, -72.90888, 9),
    (11.55078, -72.90253, 11),
    (11.54827, -72.90154, 10),
    (11.53557, -72.90211, 7),
    (11.53152, -72.90252, 2),
    (11.53606, -72.91114, 5),
    (11.54049, -72.92334, 14),
    (11.53224, -72.91281, 21),
    (11.52739, -72.89781, 13),
]




#hs.haversine(locations[0], locations[6], unit=Unit.METERS)


def compute_euclidean_distance_matrix(locations):
    '''Creates callback to return distance between points'''
    distances = {}
    dist_matrix = []
    container_indexes = {}
    for from_counter, from_node in enumerate(locations):
        distances[from_counter] = {}
        dist_matrix.append([])
        container_indexes[from_counter] = from_node[2]
        for to_counter, to_node in enumerate(locations):
            if from_node == to_node:
                #distances[from_counter][to_counter] = 0
                dist_matrix[from_counter].append(0)
            else:
                #distances[from_counter][to_counter] = int(hs.haversine(from_node[0:2], to_node[0:2], unit=Unit.METERS))
                dist_matrix[from_counter].append(int(hs.haversine(from_node[0:2], to_node[0:2], unit=Unit.METERS)))
    return dist_matrix, container_indexes

#dist, indexes = compute_euclidean_distance_matrix(locations)
#print(dist)


def create_data_model():
    '''Stores the data from the problem'''
    data = {}
    data['num_vehicles'] = 1
    data['starts'] = [1]
    data['ends'] = [15]
    data['depot'] = 0
    _, indexes = compute_euclidean_distance_matrix(locations)
    data['distance_matrix'] = matrix1
    return data, indexes

def show_solution(data, manager, routing, solution):
    """ Print Solution on console"""
    print(f'Objective solution {solution.ObjectiveValue()}')
    max_route_distance = 0
    data_route = {}
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = f'Route for vehicle {vehicle_id}\n'
        route_distance = 0
        data_route['vehicle_id'] = vehicle_id
        nodes = []
        while not routing.IsEnd(index):
            plan_output += f' {manager.IndexToNode(index)} -> '
            nodes.append(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        plan_output += f' {manager.IndexToNode(index)} \n'
        nodes.append(manager.IndexToNode(index))
        data_route['nodes'] = nodes
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        data_route['optimal_distance'] = route_distance
        max_route_distance = max(route_distance, max_route_distance)
    print(f'Maximum of the route distances: {max_route_distance} m')
    print('\n\n')
    return data_route





def main():
    ''' Solve de VRP problem '''
    
    # Instantiate the data problem
    data, indexes = create_data_model()

    # Create a routing index manager
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['starts'], data['ends'])
    def distance_callback(from_index, to_index):
        ''' Returns the distance between two nodes'''
        # Convert from routing variable Index to distance matrix NodeIndex
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        #return data['distance_matrix'][from_node][to_node]
        return data['distance_matrix'][from_node][to_node]
    
    # Create routing model
    routing = pywrapcp.RoutingModel(manager)

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint
    dimension_name = 'Distance'
    routing.AddDimension(
        evaluator_index=transit_callback_index,
        slack_max=0, #no slack
        capacity=15000, #vehicle maximun travel dinstance
        fix_start_cumul_to_zero=True, #Start cumul to zero
        name=dimension_name
    )
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)


    ## Setting first solution heuristic
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = ( routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    ## Solve problem
    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        data_route = show_solution(data, manager, routing, solution)
        sorted_route = []
        for node in data_route['nodes']:
            sorted_route.append(indexes[node])
        
        ### Outputs
        print(indexes)
        print(data_route['nodes'])
        print(sorted_route)

if __name__ == '__main__':
    main()