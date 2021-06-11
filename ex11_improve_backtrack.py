# ex11
# ex11_improve_backtrack.py
# eran_levi

from ex11_map_coloring import legal_assignment_func, read_adj_file
from ex11_backtrack import general_backtracking

COLORS = ['red', 'blue', 'green', 'magenta', 'yellow', 'cyan']
FILE_PATH = ''

def back_track_degree_heuristic(adj_dict, colors):
    """in order to assign color to the regions by their neighbors number
    this function organizes the list of items by the number of their neighbors
    from the maximum to the minimum.
    :param adj_dict: dictionary of adjacency.
    :param colors: a list of legal colors assignments.
    :return map if solved, None otherwise.
    """
    # in list_of_items there will be all the names need to get a color
    # assignment , ordered by their number of neighbors
    list_of_items = sorted(adj_dict, key=lambda k: len(adj_dict[k]),
                           reverse=True)
    # dict_items_to_vals is a dictionary which will have the items from
    # list_of_items and their assignments
    dict_items_to_vals = {}
    # index for list_of_items to assign value to
    index = 0
    # set_of_assignments is a list with all possible colors
    set_of_assignments = colors
    # map is a dictionary representation for the map
    map = {}
    for name in list_of_items:
        map[name] = '0'
    if general_backtracking(list_of_items, dict_items_to_vals, index,
                            set_of_assignments, legal_assignment_func, map,
                            adj_dict):
        return map
    return


def run_map_coloring(adjacency_file, colors, backtrack_type='general'):
    """this function solving the graph coloring problem for given adjacency
    file, colors list and chosen backtracking formula.
    :param adjacency_file: Dictionary of adjacency.
    :param backtrack_type: getting a string tells which backtracking to solve
    with.
    :param colors: a list of legal colors assignments.
    :return map if solved, None otherwise.
    """
    # in list_of_items will be all the names need to get a color assignment
    list_of_items = [k for k in adjacency_file]
    # dict_items_to_vals is a dictionary which will have the items from
    # list_of_items and their assignments
    dict_items_to_vals = {}
    # index for list_of_items to assign value to
    index = 0
    # set_of_assignments is a list with all possible colors
    set_of_assignments = colors
    # map is a dictionary representation for the map
    map = {}
    for name in list_of_items:
        map[name] = '0'
    if backtrack_type == 'general':
        if general_backtracking(list_of_items, dict_items_to_vals, index,
                                set_of_assignments, legal_assignment_func, map,
                                adjacency_file):
            return map
        return
    if backtrack_type == 'mrv':
        if specific_backtracking_MRV(list_of_items, dict_items_to_vals, index,
                                     set_of_assignments, legal_assignment_func,
                                     map, adjacency_file):
            return map
        return
    if backtrack_type == 'fc':
        if specific_backtracking_LCV(list_of_items, dict_items_to_vals, index,
                                    set_of_assignments, legal_assignment_FC,
                                    map, adjacency_file):
                return map
        return
    if backtrack_type == 'lcv':
        if specific_backtracking_LCV(list_of_items, dict_items_to_vals, index,
                                     set_of_assignments, legal_assignment_func,
                                     map, adjacency_file):
            return map
    return


def back_track_MRV(adj_dict, colors):
    """in order to assign color to the regions by the val that have the fewest
    number of legal assignments this function organizes the list of items by
    the number of their legal assignments left, from the minimum to the
    maximum.
    :param adj_dict: dictionary of adjacency.
    :param colors: a list of legal colors assignments.
    :return map if solved, None otherwise.
    """
    return run_map_coloring(adj_dict, colors, backtrack_type='mrv')


def specific_backtracking_MRV(list_of_items, dict_items_to_vals, index,
                              set_of_assignments, legal_assignment_func,
                              *args):
    """this function is solving backtracking problems MRV formula.
    :param list_of_items: wWill contain all the names need to get a color
    assignment , ordered by their number of neighbors.
    :param  dict_items_to_vals: is a dictionary which will have the items from
    list_of_items and their assignments
    :param index: Index for list_of_items to assign value to
    :param set_of_assignments: A list of legal assignments
    :param legal_assignment_func: The function that checks if an assignment is
    legal.
    :return True if solution was found, None otherwise.
    """
    # base case: all items from list of items have got a legal assignment
    if index == len(list_of_items):
        return True
    # for MRV solution i need to pick the name with the fewest legal
    # assignments left, in order to do that, run on list of names
    # so called list_of_items and save the name with the fewest legal
    # assignments left. It means that this name have the biggest variety
    # of neighbor's colors
    neighbors_colors_variety = set()
    # this set will contain the name and the number of different neighbor's
    # colors, which will represent the number of legal assignments left
    name_of_MRV = [list_of_items[0], len(neighbors_colors_variety)]
    for name in list_of_items:
        for neighbor in args[1][name]:
            # if this neighbor is colored add his color
            if neighbor in dict_items_to_vals:
                if dict_items_to_vals[neighbor] in set_of_assignments:
                    neighbors_colors_variety.add(dict_items_to_vals[neighbor])
            if name_of_MRV[1] < len(neighbors_colors_variety):
                name_of_MRV = [name, len(neighbors_colors_variety)]
        neighbors_colors_variety.clear()
    # now give an assignment to the name we have found
    # if we are in a backtracking situation lets try a different value now
    # if not lets try the first value
    # in case of backtracking keep taking values from the place we have stop
    last_value = args[0][name_of_MRV[0]]
    if last_value not in set_of_assignments:
        last_value_index = 0
    else:
        last_value_index = set_of_assignments.index(last_value)
        last_value_index += 1
    for val in set_of_assignments[last_value_index:]:
        # assign value to dict_items_to_vals
        dict_items_to_vals[list_of_items[index]] = val
        # assign value to board for the legal_assignment_func
        args[0][list_of_items[index]] = val
        if legal_assignment_func(list_of_items[index], *args):
            # if assignment is legal "step forward"-(index+1) and keep track
            # if getting to a solution
            if specific_backtracking_MRV(list_of_items, dict_items_to_vals,
                                         index+1,set_of_assignments,
                                         legal_assignment_func, *args):
                return True
    # erasing old value for backtracking
    dict_items_to_vals[list_of_items[index]] = '0'
    args[0][list_of_items[index]] = '0'


def back_track_FC(adj_dict, colors):
    """this function is solving backtracking problems using FC formula.
    :param adj_dict: dictionary of adjacency.
    :param colors: a list of legal colors assignments.
    :return map if solved, None otherwise.
    """
    return run_map_coloring(adj_dict, colors, backtrack_type='fc')


def legal_assignment_FC(name, map, adjacency, dict_items_to_vals,
                        set_of_assignments):
    """this function will check if assignment of color to name is legal, and
    also it looks forward to make sure that this assignment isn't creating
    a situation in which other name left with no legal assignment.
    :param name: Name of the country which color assignment need to be check.
    :param map: dictionary data base.
    :param adjacency: Dictionary of adjacency.
    :param  dict_items_to_vals: is a dictionary which will have the items from
    list_of_items and their assignments
    :param set_of_assignments: A list of legal assignments
    :return True if solution was found, None otherwise.
    """
    color = map[name]
    # if adjacency is not empty
    if adjacency[name]:
        # make the basic check
        for neighbor in adjacency[name]:
            if map[neighbor] == color:
                return False
        # now look forward but never forget where you came from!
        # check if last assignment 'blocked' other neighbor from getting a
        # legal assignment, do so by making
        neighbors_of_neighbor_colors_variety = set()
        for neighbor in adjacency[name]:
            neighbors_of_neighbor_colors_variety.clear()
            # this set will contain the number of different neighbor's colors
            # if it equals to the len of set_of_assignments return False
            for neighbor_of_neighbor in adjacency[neighbor]:
                # if this neighbor is colored add his color
                if neighbor_of_neighbor in dict_items_to_vals:
                    # if this neighbor is colored
                    if dict_items_to_vals[neighbor_of_neighbor] in \
                            set_of_assignments:
                        neighbors_of_neighbor_colors_variety.add(
                            dict_items_to_vals[neighbor_of_neighbor])
            if len(set_of_assignments) == \
                    len(neighbors_of_neighbor_colors_variety):
                return False
    return True


def back_track_LCV(adj_dict, colors):
    """this function is solving backtracking problems using LCV formula.
    :param adj_dict: dictionary of adjacency.
    :param colors: a list of legal colors assignments.
    :return map if solved, None otherwise.
    """
    return run_map_coloring(adj_dict, colors, backtrack_type='lcv')


def specific_backtracking_LCV(list_of_items, dict_items_to_vals, index,
                             set_of_assignments, legal_assignment_func, *args):
    """this function is solving backtracking problems LCV formula.
    :param list_of_items: Will contain all the names need to get a color
    assignment , ordered by their number of neighbors.
    :param  dict_items_to_vals: is a dictionary which will have the items from
    list_of_items and their assignments
    :param index: Index for list_of_items to assign value to
    :param set_of_assignments: A list of legal assignments
    :param legal_assignment_func: The function that checks if an assignment is
    legal.
    :return True if solution was found, None otherwise.
    """
    # base case: all items from list of items have got a legal assignment
    if index == len(list_of_items):
        return True
    # if we are in a backtracking situation lets try a different value now
    # if not lets try the first value
    # in case of backtracking keep taking values from the place we have stop
    last_value = args[0][list_of_items[index]]
    if last_value not in set_of_assignments:
        last_value_index = 0
    else:
        last_value_index = set_of_assignments.index(last_value)
        last_value_index += 1
    # calling LCV check_for getting the LCV's list
    lc_vals_list = LCV_check(list_of_items, dict_items_to_vals, index,
                             set_of_assignments, legal_assignment_func, *args)
    for lc_val in lc_vals_list:
        # assign value to dict_items_to_vals
        dict_items_to_vals[list_of_items[index]] = lc_val
        # assign value to data base
        args[0][list_of_items[index]] = lc_val
        if legal_assignment_func(list_of_items[index], *args,
                                 dict_items_to_vals, set_of_assignments):
            # if assignment is legal "step forward"-(index+1) and keep track
            # if getting to a solution
            if specific_backtracking_LCV(list_of_items, dict_items_to_vals,
                                         index + 1, set_of_assignments,
                                         legal_assignment_func, *args):
                return True
        # erasing old value for backtracking
        dict_items_to_vals[list_of_items[index]] = '0'
        args[0][list_of_items[index]] = '0'


def LCV_check(list_of_items, dict_items_to_vals, index, set_of_assignments ,
              legal_assignment_func, *args):
    """this function is making the LCV list.
    :param list_of_items: Will contain all the names need to get a color
    assignment , ordered by their number of neighbors.
    :param  dict_items_to_vals: is a dictionary which will have the items from
    list_of_items and their assignments
    :param index: Index for list_of_items to assign value to
    :param set_of_assignments: A list of legal assignments
    :param legal_assignment_func: The function that checks if an assignment is
    legal.
    :return The list of values order by Least Constraining Value first.
    """
    # create a dictionary for which assignment is the best
    vals_dict = {}
    for val in set_of_assignments:
        vals_dict[val] = 0
    # check which color is the Least Constraining Value
    for val in set_of_assignments:
        # assign value to dict_items_to_vals
        dict_items_to_vals[list_of_items[index]] = val
        # assign value to data base
        args[0][list_of_items[index]] = val
        if legal_assignment_func(list_of_items[index], *args,
                                 dict_items_to_vals, set_of_assignments):
            # compute number of assignments left for each val
            neighbors_sum_of_assignments = 0
            # for all neighbors of the current name
            for neighbor in args[1][list_of_items[index]]:
                # compute how many assignments left by checking the variety of
                # colors of his neighbors
                neighbors_of_neighbor_colors_variety = set()
                # for neighbors of neighbor
                for neighbor_of_neighbor in args[1][neighbor]:
                    # if this neighbor is colored
                    if neighbor_of_neighbor in dict_items_to_vals:
                        # with a valid color
                        if dict_items_to_vals[neighbor_of_neighbor] in \
                                set_of_assignments:
                            # add his color
                            neighbors_of_neighbor_colors_variety.add(
                                dict_items_to_vals[neighbor_of_neighbor])
                # next calculation will add the number of
                # assignments left for this specific neighbor
                # to the sum of assignments left for this val
                neighbors_sum_of_assignments += \
                    len(set_of_assignments) - \
                    len(neighbors_of_neighbor_colors_variety)
            # now i'll save this number for this val
            vals_dict[val] = neighbors_sum_of_assignments
    # order values by Least Constraining Value for the current name first
    lc_vals_list = sorted(vals_dict, key=lambda k: vals_dict[k], reverse=True)
    return lc_vals_list


def fast_back_track(adj_dict, colors):
    """this function is solving backtracking problems fastest way. using MRV,
    FC and LCV.
    :param adj_dict: dictionary of adjacency.
    :param colors: a list of legal colors assignments.
    :return map if solved, None otherwise.
    """
    # MRV
    list_of_items = sorted(adj_dict, key=lambda k: len(adj_dict[k]),
                           reverse=True)
    # dict_items_to_vals is a dictionary which will have the items from
    # list_of_items and their assignments
    dict_items_to_vals = {}
    # index for list_of_items to assign value to and assign them to
    # dict_items_to_vals
    index = 0
    # set_of_assignments is a list with all possible colors
    set_of_assignments = colors
    # map is a dictionary representation for the map also called data base
    map = {}
    for name in list_of_items:
        map[name] = '0'
    if specific_backtracking_LCV(list_of_items, dict_items_to_vals, index,
                                 set_of_assignments, legal_assignment_FC,
                                 map, adj_dict):
        return map
    return


if __name__ == '__main__':
    adjacency = read_adj_file(FILE_PATH)
    # map = back_track_degree_heuristic(adjacency,COLORS)
    # map = back_track_MRV(adjacency, COLORS)
    # map = back_track_FC(adjacency, COLORS)
    map = fast_back_track(adjacency, COLORS)
    color_map(map, map_type='world')
