import csv

class DataMaps:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.mexican_states = {
            'Aguascalientes': [21.161908, -86.851528],
            'Baja California': [22.7680, -102.5814],
            'Baja California Sur': [30.8406, -115.2838],
            'Campeche': [24.0277, -104.6532],
            'Chiapas': [19.4326, -99.1332],
            'Chihuahua': [28.6353, -106.0889],
            'Coahuila': [27.9698, -101.1732],
            'Colima': [19.2465, -103.7272],
            'Durango': [19.3191, -98.2020],
            'Guanajuato': [22.3964, -103.7250],
            'Guerrero': [17.5707, -99.1095],
            'Hidalgo': [20.5881, -100.3899],
            'Jalisco': [20.6595, -103.3494],
            'Mexico City': [19.4326, -99.1332],
            'Mexico State': [24.8615, -98.6474],
            'Michoacán': [27.0971, -101.6666],
            'Morelos': [25.4383, -100.9737],
            'Nayarit': [21.1619, -86.8515],
            'Nuevo Leon': [19.3016, -99.1574],
            'Oaxaca': [16.7569, -93.1292],
            'Puebla': [20.5888, -87.1266],
            'Queretaro': [20.5881, -89.3380],
            'Quintana Roo': [22.4027, -100.5537],
            'San Luis Potosi': [23.6345, -102.5528],
            'Sinaloa': [27.7704, -107.6295],
            'Sonora': [25.4243, -100.9737],
            'Tabasco': [17.9883, -92.9194],
            'Tamaulipas': [21.1619, -89.0706],
            'Tlaxcala': [19.3191, -99.1836],
            'Veracruz': [16.8284, -99.8787],
            'Yucatan': [20.5881, -97.5347],
            'Zacatecas': [22.7709, -102.5832]
        }

    def counter(self):
        data = []

        with open(self.csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row

            for row in csv_reader:
                state = row[0]  # Get the Mexican state
                num_elements = sum(1 for cell in row[1:] if cell.strip())  # Count non-empty elements in the row, excluding the first column
                if state in self.mexican_states:
                    data.append([*self.mexican_states[state], num_elements])  # Append data tuple to the list

        return data

