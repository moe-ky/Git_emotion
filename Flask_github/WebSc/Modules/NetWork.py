import json
import networkx as nx
from networkx.readwrite import json_graph
import os
from Modules import Functions


class Graph:
    def create_graph(name):
        groups = open("Emotion_Groups.json", "r")
        connected = open("connected.json", "r")
        load_groups = json.load(groups)
        load_connect = json.load(connected)

        G = nx.Graph()

        file_list = Functions.open_folder('result\\' + name + '\\')
        for file in file_list:
            load = open(file, "r")
            result_json = json.load(load)
            print(os.path.basename(file))

            G.add_node("Emotion", x=500, y=400, fixed=True)
            for wd in result_json['emotions']:
                for word in wd:
                    # G.add_node(word, group=load_groups[word], x=200, y=300, fixed=True)
                    G.add_node(word, group=load_groups[word])
                    G.add_edge("Emotion", word, value=wd[word])

            d = json_graph.node_link_data(G)
            file = open("result\\" + name + "\\Force_layout\\" + os.path.basename(file), 'w')
            json.dump(d, file)
            print(d)

