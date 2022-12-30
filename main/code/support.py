#importing different csv files that help build the layout
from csv import reader
import os

#sets the working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def import_csv_layout(path):
    terrain_map = []

    with open(path) as level_map:
        layout = reader(level_map,delimiter=",")
        for row in layout:
            terrain_map.append(list(row))
            return terrain_map
