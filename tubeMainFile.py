import csv
from tkinter import messagebox

import matplotlib.pyplot as plt

from tkinter import *

# Fetching values from the CSV File
list1 = []
with open('londonconnections.csv') as csv_file:
    reader1 = csv.DictReader(csv_file)

    for row in reader1:
        list1.append(row)  # list of all the items in the londonconnection.csv file

list2 = []
with open('londonstations.csv') as csv_file:
    reader2 = csv.DictReader(csv_file)

    for row in reader2:
        list2.append(row)  # list of all the items in the londonstations.csv file

list3 = []
lines = {}
with open('londonlines.csv') as line_file:
    li_reader = csv.DictReader(line_file)
    for row in li_reader:
        list3.append(row)
        for i in list3:
            lines[int(i['line_id'])] = i
        # indices.append(row['line'])
        # indices = [int(item) for item in indices]
# lines = pd.DataFrame(dict(l=li_list), index=indices)
# print(list3)

list_final = []
for i in list1:
    for j in list2:
        if i['station1'] == j['id']:
            temp = i | j
            list_final.append(temp)  # Combined values of both the list1 and list2

header = 'edge_id'
for i in range(len(list_final)):
    list_final[i][header] = i  # Addition column to connect with the other entities

hub_ids_list = []  # Empty list for all the Tuple(station, line_id)
for i in list_final:
    hub_ids_list.append((int(i['station1']), int(i['line_id'])))
    hub_ids_list.append((int(i['station2']), int(i['line_id'])))

x = set(hub_ids_list)
unique_hub_list = list(x)  # Sorted List of Tuples


# defining a function to fetch attribute values
def getStationAttributes(ids, attribute):
    for v in list2:
        if int(v['id']) == ids:
            return v[attribute]


# this function convert the datatype from string to integer
def strToInt_Conversion(r, f):
    attribute = r[f]
    r[f] = int(attribute)


# this function convert the datatype from string to float
def strToFloat_Conversion(r, f):
    attribute = r[f]
    r[f] = float(attribute)


# converting some attribute's datatype in the final list
for i in list_final:
    strToInt_Conversion(i, 'station1')
    strToInt_Conversion(i, 'station2')
    strToInt_Conversion(i, 'line_id')
    strToInt_Conversion(i, 'time')
    strToInt_Conversion(i, 'id')
    strToInt_Conversion(i, 'total_lines')
    strToFloat_Conversion(i, 'latitude')
    strToFloat_Conversion(i, 'longitude')


# opening a class Vertex and defining its constructor
class Vertex:
    def __init__(self, unique_node_id, name, station_id, latitude, longitude):
        self.unique_node_id = unique_node_id
        self.name = name
        self.station_id = station_id  # tuple
        self.latitude = latitude
        self.longitude = longitude
        self.viewed = False
        self.neighbours_id = []  # station_id
        self.edges = []


# opening a class Edge and defining its constructor
class Edge:
    def __init__(self, edge_id, departure, destination, time, line):
        self.edge_id = edge_id
        self.time = time
        self.line = line
        self.departure = departure
        self.destination = destination


# class graph which allocate data to the graph
class Graph:
    def __init__(self):
        self.dict1 = dict1  # dictionary containing nodes
        self.dict2 = dict2  # dictionary containing edges

    def get_vertices(self, node_id):
        return self.dict1[node_id]

    def get_edges_among(self, departure, destination):  # function defines the edges between the two nodes
        if departure.station_id not in destination.neighbours_id:
            return 'Link between the stations are not available'
        else:
            for edge_id in departure.edges:
                edge = self.dict2[edge_id]
                if destination.station_id in [edge.destination, edge.departure] and departure.station_id in [edge.destination, edge.departure]:
                    return edge

    def get_coordinates(self, edge, from_id):  # type Graph, type Edge, tuple representing vertex.station_id
        v1 = self.get_vertices(edge.departure)  # type Vertex
        v2 = self.get_vertices(edge.destination)  # type Vertex
        if from_id == v1.station_id:
            edge.coordinates = {'lat_from': v1.latitude, 'long_from': v1.longitude, 'lat_to': v2.latitude,
                                'long_to': v2.longitude}
        if from_id == v2.station_id:
            edge.coordinates = {'lat_from': v2.latitude, 'long_from': v2.longitude, 'lat_to': v1.latitude,
                                'long_to': v1.longitude}
        return edge.coordinates

    @staticmethod
    def searchStation(name):  # search stations in list of stations file contents
        for n in list2:
            if n['name'].casefold() == name.casefold():  # making names case-insensitive
                return 1
        return 0

    @staticmethod
    def searchId(name):  # search id in list of stations file contents
        for i in list2:
            if i['name'].casefold() == name.casefold():
                return i['id']

    # By using Dijkstra's algorithm for shortest path
    # this function defining the shortest distance between the two searched stations
    def shortest_path(self, departure, destination):
        try:
            if Graph.searchStation(departure):
                departure_id = Graph.searchId(departure)
                for i in self.dict1:
                    if i[0] == int(departure_id):
                        departure = self.dict1[i]
                        break
            else:
                message = 'Departure station does not exist.'
                messagebox.showinfo("showinfo", message)
                return message

            if Graph.searchStation(destination):
                destination_id = Graph.searchId(destination)
                for j in self.dict1:
                    if j[0] == int(destination_id):
                        destination = self.dict1[j]
                        break
            else:
                message = 'Destination station does not exist.'
                messagebox.showinfo("showinfo", message)
                return message

            not_viewed = dict([(node_id, 1000) for (node_id, node) in self.dict1.items()])
            not_viewed[departure.station_id] = 0
            viewed = []
            recent = departure
            ways = {recent.station_id: [{'name': recent.name, 'station_id': recent.station_id}]}

            while not destination.viewed:

                for neigh_id in recent.neighbours_id:
                    neighbour = self.get_vertices(neigh_id)
                    meet_neighbour = self.get_edges_among(recent, neighbour)  # []
                    if meet_neighbour.time == time_to_change_lines and (
                            meet_neighbour.departure == departure.station_id or
                            meet_neighbour.destination == destination.station_id):
                        meet_neighbour.time = 0

                    # store the quickest path to each visited station in a dict called Routes:
                    if neighbour.station_id in not_viewed:
                        if not_viewed[neighbour.station_id] > (
                                not_viewed[recent.station_id] + meet_neighbour.time):
                            not_viewed[neighbour.station_id] = not_viewed[recent.station_id] + meet_neighbour.time
                            ways[neighbour.station_id] = ways[recent.station_id][:]
                            ways[neighbour.station_id].append(
                                {"name": neighbour.name, 'station_id': neighbour.station_id})

                recent.viewed = True
                viewed.append(not_viewed.pop(recent.station_id))
                for station_id, overall_time in not_viewed.items():
                    if overall_time == min(not_viewed.values()):
                        next_station = station_id
                recent = self.get_vertices(next_station)

            # return f'The minimum time takes you to reach your destination is {viewed[-1]} minutes.'

            def navigator(way):
                try:
                    coordinates_limits = dict(
                        zip(['min_lat', 'max_lat', 'min_long', 'max_long'], [1000, -1000, 1000, -1000]))
                    latest_line_colour = None
                    getLineColour = lambda line_id: '#999999' if line_id is None else str(
                        '#' + lines[line_id]['colour'])
                    getLineName = lambda line_id: None if line_id is None else str(lines[line_id]['name'])
                    ax = plt.subplot()

                    for r in range(1,
                                   len(way)):  # loop through a list of dictionaries, one for each station on the
                        # selected route
                        departure = self.get_vertices(way[r - 1]['station_id'])
                        destination = self.get_vertices(way[r]['station_id'])
                        connection = self.get_edges_among(departure, destination)
                        self.get_coordinates(connection, departure.station_id)

                        # update max and min coordinates
                        if True:
                            if float(connection.coordinates['lat_from']) > float(coordinates_limits['max_lat']):
                                coordinates_limits['max_lat'] = connection.coordinates['lat_from']
                            if float(connection.coordinates['lat_from']) < float(coordinates_limits['min_lat']):
                                coordinates_limits['min_lat'] = connection.coordinates['lat_from']
                            if float(connection.coordinates['long_from']) > float(coordinates_limits['max_long']):
                                coordinates_limits['max_long'] = connection.coordinates['long_from']
                            if float(connection.coordinates['long_from']) < float(coordinates_limits['min_long']):
                                coordinates_limits['min_long'] = connection.coordinates['long_from']
                            if float(connection.coordinates['lat_to']) > float(coordinates_limits['max_lat']):
                                coordinates_limits['max_lat'] = connection.coordinates['lat_to']
                            if float(connection.coordinates['lat_to']) < float(coordinates_limits['min_lat']):
                                coordinates_limits['min_lat'] = connection.coordinates['lat_to']
                            if float(connection.coordinates['long_to']) > float(coordinates_limits['max_long']):
                                coordinates_limits['max_long'] = connection.coordinates['long_to']
                            if float(connection.coordinates['long_to']) < float(coordinates_limits['min_long']):
                                coordinates_limits['min_long'] = connection.coordinates['long_to']

                        line_colour = getLineColour(connection.line)
                        if line_colour == latest_line_colour:
                            line_name = None
                        else:
                            line_name = getLineName(connection.line)
                        latest_line_colour = line_colour
                        plt.plot([connection.coordinates['long_from'], connection.coordinates['long_to']],
                                 [connection.coordinates['lat_from'], connection.coordinates['lat_to']], marker='o',
                                 linestyle='--',
                                 color=line_colour, label=line_name)

                        ax.annotate(departure.name,
                                    xy=(connection.coordinates['long_from'], connection.coordinates['lat_from']),
                                    xytext=(
                                        float(connection.coordinates['long_from']) + 0.002,
                                        float(connection.coordinates['lat_from']) - 0.002))

                        ax.annotate(destination.name,
                                    xy=(connection.coordinates['long_to'], connection.coordinates['lat_to']),
                                    xytext=(
                                        float(connection.coordinates['long_to']) + 0.002,
                                        float(connection.coordinates['lat_to']) - 0.002))

                    ax.set_xticks(
                        [-0.60, -0.55, -0.50, -0.45, -0.40, -0.35, -0.30, -0.25, -0.20, -0.15, -0.10, -0.05, 0, 0.05,
                         0.10,
                         0.15, 0.20])

                    ax.set_yticks([51.40, 51.45, 51.50, 51.55, 51.60, 51.65, 51.70])
                    ax.set_xlim((float(coordinates_limits['min_long']) - 0.02),
                                (float(coordinates_limits['max_long']) + 0.02))
                    ax.set_ylim((float(coordinates_limits['min_lat']) - 0.02),
                                (float(coordinates_limits['max_lat']) + 0.02))
                    plt.xlabel('Longitude')
                    plt.ylabel('Latitude')
                    plt.legend()
                    plt.show()
                except EXCEPTION:
                    pass
            messagebox.showinfo("showinfo",
                                f"Travelling from {departure.name} to {destination.name} will take {viewed[-1]} minutes.")

            a = messagebox.askyesno("askyesno", "do you want to see the route?")
            if a:
                navigator(way=ways[destination.station_id])
            else:
                root.destroy()
        except EXCEPTION:
            pass




dict1 = {}
dict2 = {}
###################Dictionary of Nodes######################
for i in unique_hub_list:
    temp1 = {}
    temp2 = {}
    for j in list_final:
        if i[0] == j['station1'] and i[1] == j['line_id']:
            temp1[i] = Vertex(j['id'], j['name'], i, j['latitude'], j['longitude'])
            dict1 = dict1 | temp1
        if i[0] == j['station2'] and i[1] == j['line_id']:
            temp2[i] = Vertex(j['station2'], getStationAttributes(int(j['station2']), 'name'),
                              i, getStationAttributes(j['station2'], 'latitude'),
                              getStationAttributes(j['station2'], 'longitude'))
            dict1 = dict1 | temp2

####################Dictonary of Edges########################
for i in list_final:
    temp = {i['edge_id']: Edge(i['edge_id'], tuple([i['station1'], i['line_id']]),
                               tuple([i['station2'], i['line_id']]),
                               i['time'], i['line_id'])}
    dict2 = dict2 | temp

###################################################
for i in range(len(list_final)):
    a = dict1[tuple([list_final[i]['station1'], list_final[i]['line_id']])]
    b = dict1[tuple([list_final[i]['station2'], list_final[i]['line_id']])]
    a.edges.append(i)
    b.edges.append(i)
    a.neighbours_id.append(tuple([list_final[i]['station2'], list_final[i]['line_id']]))
    b.neighbours_id.append(tuple([list_final[i]['station1'], list_final[i]['line_id']]))

keys = range(1, len(list2) + 2)
values = [[] for i in keys]
hubs = dict(zip(keys, values))

for id_tuple, station in dict1.items():
    hubs[id_tuple[0]].append(id_tuple)
i = 1000
time_to_change_lines = 0  # educated guess :-)
for hub in hubs.values():  # hub example: 1: [[1, 10], [1, 6], [1, 9]]
    for station in hub:  # station example: [1, 10]
        for s in hub:
            if station != s:
                dict1[station].neighbours_id.append(s)
                dict1[station].edges.append(i)
                dict2[i] = Edge(i, station, s, time_to_change_lines, None)
                i += 1

# print(Graph().shortest_path("Pimlico", "Hampstead"))

# Setting up GUI using Tkinter
root = Tk()
root.geometry("644x344")
root.title("Welcome to London Tubes")
root.maxsize(500,140)
root.minsize(500,140)

Label(root, text="Plan a journey", font="comicsansms 13 bold", pady=15).grid(row=0, column=3)
Label(root, text="From").grid(row=1, column=2)
Label(root, text="To").grid(row=2, column=2)

stationFromValue = StringVar()
stationToValue = StringVar()
Entry(root, borderwidth=1, textvariable=stationFromValue).grid(row=1, column=3)
Entry(root, borderwidth=1, textvariable=stationToValue).grid(row=2, column=3)


def size():
    return Graph().shortest_path(stationFromValue.get(), stationToValue.get())


Button(root, text="Search route", command=size, padx=4, pady=4,
       fg="purple").grid(row=7, column=3)

root.mainloop()
