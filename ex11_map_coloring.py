# ex11
# ex11_map_coloring.py
# eran_levi

from ex11_backtrack import general_backtracking

COLORS = ['red', 'blue', 'green', 'magenta', 'yellow', 'cyan']
FILE_PATH = ''

def read_adj_file(adjacency_file):
    """this function loads a text file of sudoku game into a dictionary.
    :param adjacency_file: Path to text file of adjacency.
    :return dictionary of adjacency.
    """
    adjacency = {}
    with open(adjacency_file, 'r') as wl:
        lines = wl.readlines()
        for line in lines:
            temp = line.split(':')
            if temp[1] == '\n':
                adjacency[temp[0]] = []
            else:
                adjacency[temp[0]] = temp[1][:-1].split(',')
    return adjacency


def run_map_coloring(adjacency_file, num_colors = 4, map_type = None):
    """this function solving the graph coloring problem for given adjacency
    file.
    :param adjacency_file: Dictionary of adjacency.
    :param num_colors: Int of number of colors for coloring the map.
    :param map_type: not used because instructions didn't mention how.
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
    set_of_assignments = [COLORS[k] for k in range(num_colors)]
    # map is a dictionary representation for the map
    map = {}
    for name in list_of_items:
        map[name] = '0'
    if general_backtracking(list_of_items, dict_items_to_vals, index,
                            set_of_assignments, legal_assignment_func, map,
                            adjacency_file):
        return map
    return

def legal_assignment_func(name, map, adjacency):
    """this function will check if assignment of color to name is legal.
    :param name: Name of the country which color assignment need to be check.
    :param map: dictionary data base.
    :param adjacency: dictionary of adjacency.
    :return True if assignment is legal and False otherwise.
    """
    color = map[name]
    # if adjacency is not empty
    if adjacency[name]:
        for neighbor in adjacency[name]:
            if map[neighbor] == color:
                return False
    return True

if __name__ == '__main__':
    adjacency_file = read_adj_file(FILE_PATH)
    map = run_map_coloring(adjacency_file)
    color_map(map, map_type='USA')
