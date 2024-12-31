# application_graph.py
import networkx as nx
import matplotlib.pyplot as plt

class ApplicationGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_task(self, task_name, dependencies=None, compute_time=0, data_volume=0):
        # 添加节点
        self.graph.add_node(task_name, compute_time=compute_time, data_volume=data_volume)
        # 添加依赖关系（边）
        if dependencies:
            for dep in dependencies:
                self.graph.add_edge(dep, task_name)

    def analyze_graph(self):
        # 打印图的属性
        print("Nodes with attributes:", self.graph.nodes(data=True))
        print("Edges:", self.graph.edges())
        # 计算图的中心性
        centrality = nx.degree_centrality(self.graph)
        print("Degree Centrality:", centrality)
        # 计算最长路径（如果是DAG）
        try:
            longest_path = nx.dag_longest_path(self.graph, weight='compute_time')
            print("Critical Path:", longest_path)
        except nx.NetworkXError:
            print("Graph is not a Directed Acyclic Graph (DAG).")

    def visualize_graph(self):
        # 可视化图
        nx.draw(self.graph, with_labels=True, node_size=2000, node_color="lightblue", font_size=10)
        plt.title("Application Characterization Graph")
        plt.show()
