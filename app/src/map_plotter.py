"""
map_plotter.py
"""

import folium

class MapPlotter:
    def __init__(self):
        """
        Initializes the MapPlotter
        """
        self.map = folium.Map(location=[0, 0], zoom_start=2)
        self.map_file = "./exports/map.html"

    def plot_pins(self, gps_data):
        """
        Plots pins on the map based on the provided GPS data
        """
        for id, coord in gps_data.items():
            latitude = coord["latitude"]
            longitude = coord["longitude"]

            folium.Marker(
                [latitude, longitude],
                popup = id,
            ).add_to(self.map)

    def save_map(self):
        """
        Saves the generated map to an HTML file
        """
        self.map.save(self.map_file)


if __name__ == "__main__":

    gps_data = {}

    with open("./tmp/gps.txt", "r") as f:
        next(f)

        for line in f:
            id, latitude_str, longitude_str = line.split(',')

            latitude = float(latitude_str)
            longitude = float(longitude_str)

            gps_data[id] = {
                "latitude": latitude,
                "longitude": longitude
            }

    plotter = MapPlotter()
    plotter.plot_pins(gps_data)
    plotter.save_map()
