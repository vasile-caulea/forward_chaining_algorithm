import os

import matplotlib
from PIL import Image
from graphviz import Digraph
from matplotlib import pyplot as plt, pylab

from fca_algorithm.clause import Clause
from fca_algorithm.literal import Literal

matplotlib.use('Qt5Agg')


def plot_graph(file_name: str, demonstration_steps: list[tuple[Clause, Literal]]):
    name = os.path.basename(file_name).split('.')[0]
    plot_path = 'image_plots/' + name

    dot = Digraph(format='png', graph_attr={'rankdir': 'BT'}, node_attr={'shape': 'box'},
                  edge_attr={'dir': 'forward', 'length': '20'})
    for premise, conclusion in demonstration_steps:
        for literal in premise.premises:
            dot.edge(f"{literal}", f"{conclusion}")

    dot.render(plot_path, format='png', cleanup=True)

    figure = plt.figure()
    figure.canvas.manager.set_window_title(f'{plot_path}.png')
    img = Image.open(f'{plot_path}.png')
    plt.imshow(img)
    plt.axis('off')
    plt.show()
