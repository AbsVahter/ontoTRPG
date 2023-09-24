import numpy as np
from pyvis.network import Network
from owlready2 import *


def get_random_color():
    return list(np.random.choice(range(256), size=3))


def get_data_for_nodes(results):
    for_nodes = []
    for res in results:
        for i in range(0, len(res), 2):
            if res[i] is not None:
                for_nodes.append(res[i])
    return set(for_nodes)


def get_class_colors(for_nodes):
    classes = set([x.is_a[0] for x in for_nodes])
    dict = {}
    for cl in classes:
        color = get_random_color()
        dict[cl] = f"rgb({color[0]},{color[1]},{color[2]})"
    return dict


def check_unique(for_edges, to_add):
    for k in for_edges:
        if k == to_add:
            return False
    return True



def get_data_for_edges(results):
    for_edges = []
    for res in results:
        for i in range(1, len(res), 2):
            to_add = res[(i-1):(i+2)]
            if None not in to_add and check_unique(for_edges, to_add):
                for_edges.append(to_add)
    return for_edges

def show(onto, path):
    net = Network(height = '920px', width = '100%', directed = True)

    query = """
    select ?subject ?predicate ?object ?predicate ?object2
    { 
        ?subject a pzo2101:Language_regional .
        optional { 
            ?subject ?predicate ?object .
            ?object ?predicate ?object2 .
            filter ( ?predicate in (pzo2101:location) ).
        }
    }
    """

    results = list(default_world.sparql(query))

    for_nodes = get_data_for_nodes(results)
    class_colors = get_class_colors(for_nodes)
    for n in for_nodes:
        net.add_node(
            n_id = n.name,
            label = n.name,
            color = class_colors[n.is_a[0]],
        )

    for_edges = get_data_for_edges(results)
    for res in for_edges:
        net.add_edge(
            source = res[0].name,
            to = res[2].name,
            title = res[1].name,
        )

    net.show('graph.html', notebook = False)