import json
import xml.etree.cElementTree as ET

root = ET.Element("graphml", xmlns="http://graphml.graphdrawing.org/xmlns",xsi="http://www.w3.org/2001/XMLSchema-instance")
graph = ET.SubElement(root, "graph", id="popco-graph", edgedefault="undirected")

ET.SubElement(graph, "key", name="label", type="String", id="label")
ET.SubElement(graph, "key", name="r", type="int", gor="node", id="r")
ET.SubElement(graph, "key", name="g", type="int", gor="node", id="g")
ET.SubElement(graph, "key", name="b", type="int", gor="node", id="b")

f = open('DMID5.json',)
data = json.load(f)

with open('Mitgliederliste.txt', 'r') as file:
    data2 = file.read().replace('\n','.').split('.')

for node in data['nodes']:
    nodeG = ET.SubElement(graph, "node", id=node['name'])
    ET.SubElement(nodeG, "data", key="label").text = str(data2[int(node['name'])].split('; ')[1])
    color = node['color'].split('(')[1].split(',')
    ET.SubElement(nodeG, "data", key="r").text = str(int(float(color[0])))
    ET.SubElement(nodeG, "data", key="g").text = str(int(float(color[1])))
    ET.SubElement(nodeG, "data", key="b").text = str(int(float(color[2])))

for edge in data['links']:
	ET.SubElement(graph, "edge", source=str(edge['source']), target=str(edge['target']))
tree = ET.ElementTree(root)
tree.write("Graph.graphml")
