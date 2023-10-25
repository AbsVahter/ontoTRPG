import numpy as np
from pyvis.network import Network
from owlready2 import *


def get_random_color():
    color = list(np.random.choice(range(256), size = 3))
    return f"rgb({color[0]},{color[1]},{color[2]})"


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
        dict[cl] = get_random_color()
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
            to_add = res[(i - 1):(i + 2)]
            if None not in to_add and check_unique(for_edges, to_add):
                for_edges.append(to_add)
    return for_edges


def fill_net_by_sparql(net):
    query = """
        select ?subject ?predicate ?object
        { 
            ?subject ?predicate ?object .
            filter (?predicate not in (rdfs:comment, rdf:type) &&
                ?subject in (pzo2101:melee_attack_roll))
        }
        """

    sync_reasoner(infer_property_values = True, debug = 0)
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


def add_to_net(net, nodes, colors=None, root=None, edge_title=''):
    if not isinstance(nodes, list): nodes = [nodes]
    for n in nodes:
        if isinstance(n, (str, int, bool)):
            name = str(n)
            shape = "diamond"
        else:
            name = n.name
            shape = "dot"

        net.add_node(
            n_id = name,
            label = name,
            color = get_random_color() if colors is None else (
                colors if isinstance(colors, str) else colors[n.is_a[0]]),
            shape = shape,
        )
        if root is not None:
            net.add_edge(
                source = root.name,
                to = name,
                title = edge_title,
            )


def fill_net_by_owlready(net):
    pzo2101 = default_world.ontologies[
        "https://raw.githubusercontent.com/AbsVahter/trpgontologies/main/pathfinder/2ed/pzo2101.owl#"]
    sync_reasoner_pellet(debug = 0, infer_property_values = True, infer_data_property_values = True)

    color = get_random_color()

    root = pzo2101['melee_attack_check']
    add_to_net(net, root)
    add_to_net(net, root.calculations, color, root)
    neighbors = root.uses + root.check_result
    neighbors_colors = get_class_colors(neighbors)
    add_to_net(net, neighbors, neighbors_colors, root, 'uses')
    for neighbor in neighbors:
        add_to_net(net, neighbor.calculations, color, neighbor)


def show(path):
    net = Network(height = '920px', width = '100%', directed = True)
    scenario = 0
    if scenario == 1:
        fill_net_by_sparql(net)
    else:
        fill_net_by_owlready(net)

    net.toggle_physics(False)
    net.show_buttons(filter_ = ['physics'])
    net.show('graph.html', notebook = False)
