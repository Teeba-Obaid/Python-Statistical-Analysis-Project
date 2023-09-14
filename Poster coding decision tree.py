import networkx as nx
import plotly.graph_objects as go

# Create a directed graph
G = nx.DiGraph()

# Add edges to the graph (each edge is a tuple of two nodes)
G.add_edges_from([
    ("Decision Tree", "Instance 1: Bulb"),
    ("Instance 1: Bulb", "Attribute 1"),
    ("Instance 1: Bulb", "Attribute 2"),
    ("Instance 1: Bulb", "Attribute 3"),
    ("Attribute 3", "Attribute 4"),

    ("Decision Tree", "Instance 2: Battery Voltage"),
    ("Instance 2: Battery Voltage", "Attribute 5"),
    ("Instance 2: Battery Voltage", "Attribute 6"),

    ("Decision Tree", "Instance 3: Resistance"),
    ("Instance 3: Resistance", "Attribute 7"),
    ("Attribute 7", "Attribute 8"),
    ("Attribute 7", "Attribute 9"),
    ("Attribute 7", "Attribute 10"),
    ("Attribute 7", "Attribute 11"),

    ("Decision Tree", "Instance 4: Ammeter"),
    ("Instance 4: Ammeter", "Attribute 12"),
    ("Instance 4: Ammeter", "Attribute 13"),
    ("Instance 4: Ammeter", "Attribute 14"),
    ("Instance 4: Ammeter", "Attribute 15"),

    ("Decision Tree", "Instance 5: Voltmeter"),
    ("Instance 5: Voltmeter", "Attribute 16"),
    ("Attribute 16", "Attribute 17"),
    ("Attribute 16", "Attribute 18"),
    ("Attribute 16", "Attribute 19"),
])

# Get positions for the nodes in G
pos = nx.spring_layout(G)

# Create edge trace
edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])

# Create node trace
node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers+text',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        line=dict(width=2)))

for node in G.nodes():
    x, y = pos[node]
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])
    node_trace['text'] += tuple([node])

# Create figure
fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='My Graph',
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="",
                    showarrow=False,
                    xref="paper", yref="paper") ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False,zeroline=False,showticklabels=False)))

# Save the figure as an HTML file
fig.write_html("graph.html")

