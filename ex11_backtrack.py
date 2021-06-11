# ex11
# backtrack.py
# eran_levi


def general_backtracking(list_of_items, dict_items_to_vals, index, 
                         set_of_assignments, legal_assignment_func, *args):
    """this naive function is solving backtracking problems.
    :param list_of_items: In list_of_items there will be all the names need to
    get a color assignment.
    :param dict_items_to_vals: dict_items_to_vals is a dictionary of
    list_of_items with values from set_of_assignments
    :param index: Index for list_of_items to assign value to
    :param set_of_assignments: A list of legal assignments
    :param legal_assignment_func: The function that checks if an assignment is
    legal.
    :return: True if data base given at args[0] solved, None otherwise.
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
    for val in set_of_assignments[last_value_index:]:
        # assign value to dict_items_to_vals
        dict_items_to_vals[list_of_items[index]] = val
        # assign value to database for the legal_assignment_func
        args[0][list_of_items[index]] = val
        if legal_assignment_func(list_of_items[index], *args):
            # if assignment is legal "step forward"-(index+1) and keep track
            # if getting to a solution
            if general_backtracking(list_of_items, dict_items_to_vals,
                                    index+1,set_of_assignments,
                                    legal_assignment_func, *args):
                return True
    # erasing old value for backtracking
    dict_items_to_vals[list_of_items[index]] = '0'
    args[0][list_of_items[index]] = '0'
