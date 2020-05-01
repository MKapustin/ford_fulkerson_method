import copy
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def init_connection_matrix(file_name="ford_fulkerson_method/graph.txt", node_amount=5):
    connection_matrix = []

    for i in range(0, node_amount):
        connection_matrix.append(list())
        for j in range(0, node_amount):
            connection_matrix[i].append(0)

    with open(file_name, 'r') as file:
        for i in file:
            row_items = i.split()
            start_node = int(row_items[0])
            end_node = int(row_items[1])
            weight = int(row_items[2])
            connection_matrix[start_node][end_node] = weight

    return connection_matrix


def _get_nodes_to_move_set(node, connection_matrix, node_marks, node_to_delete_from_nodes_to_move_set=None):  # step 2
    nodes_to_move_set = set()
    for adjacent_node, weight_to_adjacent_node in enumerate(connection_matrix[node]):
        if weight_to_adjacent_node > 0 and node_marks[adjacent_node] == None:
            nodes_to_move_set.add(adjacent_node)

    if node_to_delete_from_nodes_to_move_set:
        nodes_to_move_set.remove(node_to_delete_from_nodes_to_move_set)

    return nodes_to_move_set


def _not_empty_nodes_to_move_set_proc(node, nodes_to_move_set, connection_matrix, node_marks):  # step 3
    adjacent_node_max_weight = -1
    adjacent_node_to_move = -1
    for adjacent_node in nodes_to_move_set:
        adjacent_node_weight = connection_matrix[node][adjacent_node]
        if adjacent_node_weight > adjacent_node_max_weight:
            adjacent_node_max_weight = adjacent_node_weight
            adjacent_node_to_move = adjacent_node
    direction = "+" if adjacent_node_to_move > node else "-"
    node_marks[adjacent_node_to_move] = (adjacent_node_max_weight, node, direction)
    return adjacent_node_to_move  # new node to proc


def _empty_nodes_to_move_set_proc(node, node_marks):  # step 4: if node != 1
    node_to_delete_from_nodes_to_move_set = node
    new_node_to_proc = node_marks[node][1]
    node_marks[node] = None
    return new_node_to_proc, node_to_delete_from_nodes_to_move_set


def _selected_way_proc(node, connection_matrix, node_marks, way_weights):  # step 5
    way_min_weight = min([node_mark[0] for node_mark in node_marks if node_mark])
    way_weights.append(way_min_weight)
    while node != 0:
        node_mark = node_marks[node]
        direction = node_mark[2]
        if direction == "+":
            connection_matrix[node_mark[1]][node] -= way_min_weight
            connection_matrix[node][node_mark[1]] += way_min_weight
        elif direction == "-":
            connection_matrix[node_mark[1]][node] += way_min_weight
            connection_matrix[node][node_mark[1]] -= way_min_weight
        else:
            print("Error! Unknown direction.")
            return
        node_marks[node] = None
        node = node_mark[1]


def _get_result(way_weights, connection_matrix, connection_matrix_copy):  # step 6
    summary_weight = sum(way_weights)
    connection_matrix = np.array(connection_matrix) - np.array(connection_matrix_copy)
    return summary_weight, connection_matrix


def ford_fulkerson_method(connection_matrix):
    connection_matrix_copy = copy.deepcopy(connection_matrix)
    nodes_amount = len(connection_matrix)
    last_node = nodes_amount - 1
    node_marks = [None for _ in range(0, nodes_amount)]
    node_marks[0] = (np.inf, None, None)  # (price to move from node_from, node_from, direction: + or -)
    way_weights = list()
    proc_node = 0
    node_to_delete_from_nodes_to_move_set = None
    frame_to_save_idx = 0
    while True:
        draw_graph(connection_matrix_copy, frame_to_save_idx,
                   [(node_mark[1], node) for node, node_mark in enumerate(node_marks[1:], start=1) if node_mark])
        frame_to_save_idx += 1

        nodes_to_move_set = _get_nodes_to_move_set(proc_node, connection_matrix_copy, node_marks,
                                                   node_to_delete_from_nodes_to_move_set)
        node_to_delete_from_nodes_to_move_set = None
        if nodes_to_move_set:
            next_node_to_move = _not_empty_nodes_to_move_set_proc(proc_node, nodes_to_move_set, connection_matrix_copy,
                                                                  node_marks)
            draw_graph(connection_matrix_copy, frame_to_save_idx,
                       [(node_mark[1], node) for node, node_mark in enumerate(node_marks[1:], start=1) if node_mark])
            frame_to_save_idx += 1
            if next_node_to_move == last_node:
                _selected_way_proc(next_node_to_move, connection_matrix_copy, node_marks, way_weights)
                proc_node = 0
            else:
                proc_node = next_node_to_move
        else:
            if proc_node == 0:
                method_result, connection_matrix = _get_result(way_weights, connection_matrix, connection_matrix_copy)
                return method_result, connection_matrix
            else:
                next_node_to_move, node_to_delete_from_nodes_to_move_set = _empty_nodes_to_move_set_proc(proc_node,
                                                                                                         node_marks)
                proc_node = next_node_to_move


def get_graph(connection_matrix):
    G = nx.DiGraph()
    nodes_amount = len(connection_matrix)
    for node in range(0, nodes_amount):
        G.add_node(node)
    for node, node_connections in enumerate(connection_matrix):
        for connection_node, connection_weight in enumerate(node_connections):
            if connection_weight > 0:
                G.add_edge(node, connection_node, weight=connection_weight)
    return G


def draw_graph(connection_matrix, frame_idx, edgelist_to_mark=None):
    G = get_graph(connection_matrix)
    pos = nx.circular_layout(G)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=labels)
    if edgelist_to_mark:
        nx.draw_networkx_edges(G, pos, edgelist=edgelist_to_mark, edge_color='r', width=4)

    fig = plt.gcf()
    fig.savefig(f'ford_fulkerson_method/frames/{frame_idx}.png', dpi=100)

    plt.show()


if __name__ == "__main__":
    connection_matrix = init_connection_matrix()
    # draw_graph(connection_matrix)
    method_resut, connection_matrix = ford_fulkerson_method(connection_matrix)
    # draw_graph(connection_matrix)
    print(connection_matrix)
    print(method_resut)
