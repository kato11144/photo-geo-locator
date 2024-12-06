"""
gps_extractor.py
"""

import os
import exifread
import shutil

class GPSExtractor:
    def __init__(self):
        """
        Initializes the GPSExtractor
        """
        self.assets_path = "./assets"

    def get_jpeg_files(self):
        """
        Gets all JPEG files in assets folder
        """
        jpeg_files = []

        for f in os.listdir(self.assets_path):
            if f.lower().endswith(".jpg") or f.lower().endswith(".jpeg"):
                file_path = os.path.join(self.assets_path, f)
                jpeg_files.append(file_path)

        return jpeg_files

    def get_exif_data(self, jpeg_file):
        """
        Gets EXIF data from JPEG file
        """
        try:
            with open(jpeg_file, "rb") as f:
                exif_data = exifread.process_file(f, details=False)
            return exif_data

        except Exception as e:
            print(f"Failed to read EXIF data from {jpeg_file}: {e}")
            return None

    def get_gps_info(self, exif_data):
        """
        Gets GPS information from EXIF data
        """
        if not exif_data:
            return None

        try:
            gps_latitude = exif_data.get("GPS GPSLatitude")
            gps_latitude_ref = exif_data.get("GPS GPSLatitudeRef")
            gps_longitude = exif_data.get("GPS GPSLongitude")
            gps_longitude_ref = exif_data.get("GPS GPSLongitudeRef")

            if not (gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref):
                return None

            latitude = self._convert_to_degrees(gps_latitude)
            if gps_latitude_ref.values[0] != "N":
                latitude = -latitude

            longitude = self._convert_to_degrees(gps_longitude)
            if gps_longitude_ref.values[0] != "E":
                longitude = -longitude

            gps_info = [latitude, longitude]

            return gps_info

        except Exception as e:
            print(f"Failed to extract GPS info: {e}")
            return None

    def _convert_to_degrees(self, value):
        """
        Converts GPS coordinates from DMS (Degrees, Minutes, Seconds) format to decimal degrees
        """
        degree = float(value.values[0].num) / float(value.values[0].den)
        minute = float(value.values[1].num) / float(value.values[1].den)
        second = float(value.values[2].num) / float(value.values[2].den)

        decimal_degree = degree + (minute / 60.0) + (second / 3600.0)

        return decimal_degree

    def extract_all_gps(self):
        """
        Extracts all GPS information
        """
        jpeg_files = self.get_jpeg_files()
        gps_data = {}

        id = 1
        for jpeg_file in jpeg_files:
            exif_data = self.get_exif_data(jpeg_file)
            gps_info = self.get_gps_info(exif_data)

            if gps_info:
                shutil.copy(jpeg_file, f"./tmp/{id}.jpg")
                coord = {
                    "latitude": gps_info[0],
                    "longitude": gps_info[1]
                }
                gps_data[id] = coord
                id += 1

        return gps_data


if __name__ == "__main__":

    extractor = GPSExtractor()
    gps_data = extractor.extract_all_gps()

    with open("./tmp/gps.txt", "w") as f:
        f.write("id,latitude,longitude\n")

        for id, coords in gps_data.items():
            f.write(f"{id},{coords['latitude']},{coords['longitude']}\n")
