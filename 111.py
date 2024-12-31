# # Import necessary libraries for plotting
# import matplotlib.pyplot as plt
# import networkx as nx

# # Define nodes with attributes
# nodes = [
#     ('Initialize Object Detection', {'compute_time': 0.3, 'data_volume': 2}),
#     ('Load YOLOv5 Model', {'compute_time': 1.0, 'data_volume': 50}),
#     ('Start Object Detection', {'compute_time': 0.2, 'data_volume': 5}),
#     ('Run YOLO Inference', {'compute_time': 2.0, 'data_volume': 10}),
#     ('Parse Detection Results', {'compute_time': 0.5, 'data_volume': 5}),
#     ('Save Detection Image', {'compute_time': 0.1, 'data_volume': 2}),
#     ('Start Stop Sign Detection', {'compute_time': 0.2, 'data_volume': 5}),
#     ('Get Nearest Stop Sign', {'compute_time': 0.3, 'data_volume': 3}),
#     ('Run YOLO Detection', {'compute_time': 1.5, 'data_volume': 10}),
#     ('Get Pixel Width', {'compute_time': 0.3, 'data_volume': 2}),
#     ('Calculate Focal Length', {'compute_time': 0.4, 'data_volume': 2}),
#     ('Annotate Image', {'compute_time': 0.3, 'data_volume': 5}),
#     ('Save Annotated Image', {'compute_time': 0.1, 'data_volume': 2}),
#     ('Start Real-time Detection', {'compute_time': 0.3, 'data_volume': 3}),
#     ('Render Real-time Results', {'compute_time': 0.4, 'data_volume': 5}),
#     ('Display Real-time Results', {'compute_time': 0.1, 'data_volume': 2}),
# ]

# # Define edges
# edges = [
#     ('Initialize Object Detection', 'Load YOLOv5 Model'),
#     ('Initialize Object Detection', 'Start Stop Sign Detection'),
#     ('Load YOLOv5 Model', 'Start Object Detection'),
#     ('Start Object Detection', 'Run YOLO Inference'),
#     ('Run YOLO Inference', 'Parse Detection Results'),
#     ('Run YOLO Inference', 'Start Real-time Detection'),
#     ('Parse Detection Results', 'Save Detection Image'),
#     ('Parse Detection Results', 'Get Pixel Width'),
#     ('Start Stop Sign Detection', 'Get Nearest Stop Sign'),
#     ('Get Nearest Stop Sign', 'Run YOLO Detection'),
#     ('Run YOLO Detection', 'Parse Detection Results'),
#     ('Get Pixel Width', 'Calculate Focal Length'),
#     ('Calculate Focal Length', 'Annotate Image'),
#     ('Annotate Image', 'Save Annotated Image'),
#     ('Start Real-time Detection', 'Render Real-time Results'),
#     ('Render Real-time Results', 'Display Real-time Results')
# ]

# # Create a directed graph
# G = nx.DiGraph()

# # Add nodes and edges
# G.add_nodes_from(nodes)
# G.add_edges_from(edges)

# # Set the layout for the graph
# pos = nx.spring_layout(G, seed=42)

# # Plot the graph
# plt.figure(figsize=(12, 10))

# # Draw the graph
# nx.draw(G, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, font_weight='bold', arrowsize=20)
# plt.title("Directed Graph of Object Detection Process")
# plt.show()

import matplotlib.pyplot as plt
import networkx as nx

# 构建有向图
G = nx.DiGraph()

# 添加节点和属性
nodes = [
    ('Initialize Object Detection', {'compute_time': 0.3, 'data_volume': 2}),
    ('Load YOLOv5 Model', {'compute_time': 1.0, 'data_volume': 50}),
    ('Start Object Detection', {'compute_time': 0.2, 'data_volume': 5}),
    ('Run YOLO Inference', {'compute_time': 2.0, 'data_volume': 10}),
    ('Parse Detection Results', {'compute_time': 0.5, 'data_volume': 5}),
    ('Save Detection Image', {'compute_time': 0.1, 'data_volume': 2}),
    ('Start Stop Sign Detection', {'compute_time': 0.2, 'data_volume': 5}),
    ('Get Nearest Stop Sign', {'compute_time': 0.3, 'data_volume': 3}),
    ('Run YOLO Detection', {'compute_time': 1.5, 'data_volume': 10}),
    ('Get Pixel Width', {'compute_time': 0.3, 'data_volume': 2}),
    ('Calculate Focal Length', {'compute_time': 0.4, 'data_volume': 2}),
    ('Annotate Image', {'compute_time': 0.3, 'data_volume': 5}),
    ('Save Annotated Image', {'compute_time': 0.1, 'data_volume': 2}),
    ('Start Real-time Detection', {'compute_time': 0.3, 'data_volume': 3}),
    ('Render Real-time Results', {'compute_time': 0.4, 'data_volume': 5}),
    ('Display Real-time Results', {'compute_time': 0.1, 'data_volume': 2}),
]
edges = [
    ('Initialize Object Detection', 'Load YOLOv5 Model'),
    ('Initialize Object Detection', 'Start Stop Sign Detection'),
    ('Load YOLOv5 Model', 'Start Object Detection'),
    ('Start Object Detection', 'Run YOLO Inference'),
    ('Run YOLO Inference', 'Parse Detection Results'),
    ('Run YOLO Inference', 'Start Real-time Detection'),
    ('Parse Detection Results', 'Save Detection Image'),
    ('Parse Detection Results', 'Get Pixel Width'),
    ('Start Stop Sign Detection', 'Get Nearest Stop Sign'),
    ('Get Nearest Stop Sign', 'Run YOLO Detection'),
    ('Run YOLO Detection', 'Parse Detection Results'),
    ('Get Pixel Width', 'Calculate Focal Length'),
    ('Calculate Focal Length', 'Annotate Image'),
    ('Annotate Image', 'Save Annotated Image'),
    ('Start Real-time Detection', 'Render Real-time Results'),
    ('Render Real-time Results', 'Display Real-time Results'),
]

G.add_nodes_from([(n, attrs) for n, attrs in nodes])
G.add_edges_from(edges)

# 计算网络属性
assortativity = nx.degree_assortativity_coefficient(G)
average_degree = sum(dict(G.degree()).values()) / G.number_of_nodes()
average_path_length = nx.average_shortest_path_length(G) if nx.is_strongly_connected(G) else "Not strongly connected"

# 打印分析结果
print("Assortativity:", assortativity)
print("Average Degree:", average_degree)
print("Average Path Length:", average_path_length)

# 绘制网络图
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold", arrowsize=15)
plt.title("Application Graph")
plt.show()
