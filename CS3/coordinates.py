import pyproj
import matplotlib.pyplot as plt
import folium
import pandas as pd

def wgs84_to_cartesian(origin, coordinates):
    origin_lat, origin_lon = origin
    transformer = pyproj.Transformer.from_crs('epsg:4326', 'epsg:3857')  # WGS84 to Web Mercator projection

    origin_x, origin_y = transformer.transform(origin_lon, origin_lat)

    transformed_coordinates = []
    for lat, lon in coordinates:
        x, y = transformer.transform(lon, lat)
        transformed_coordinates.append((x - origin_x, y - origin_y))

    return transformed_coordinates

## case study 3

# Load the OSPAR database CSV file
df = pd.read_csv('ospar_offshore_installations_2019_01_002.csv')
# Filter the installations with the 'above water production' function
df = df[df['Function'] == 'Above water production']
# Filter the installations with the 'oil' Primary_pr
df = df[df['Primary_pr'] == 'Oil']
# filter for coordinates in the North Sea between 48 and 62 degrees latitude and 0 and 10 degrees longitude
df = df[(df['Latitude'] > 48) & (df['Latitude'] < 62) & (df['Longitude'] > -1.3) & (df['Longitude'] < 6.5)]

# create a list of the coordinates of the installation with demark as country
denmark = df[df['Country'] == 'Denmark']
denmark = denmark[['Latitude', 'Longitude']]
denmark = denmark.values.tolist()
print(denmark)

norway = df[df['Country'] == 'Norway']
norway = norway[['Latitude', 'Longitude']]
norway = norway.values.tolist()
print(norway)

uk = df[df['Country'] == 'United Kingdom']
uk = uk[['Latitude', 'Longitude']]
uk = uk.values.tolist()
print(uk)

# combine the three lists
combined = denmark + norway + uk


origin_coordinate = (53.000, -0.500)

# cartesian_coordinates = wgs84_to_cartesian(origin_coordinate, denmark)
# cartesian_coordinates = wgs84_to_cartesian(origin_coordinate, norway)
# cartesian_coordinates = wgs84_to_cartesian(origin_coordinate, uk)
cartesian_coordinates = wgs84_to_cartesian(origin_coordinate, combined)

# Print the transformed coordinates
for coordinate in cartesian_coordinates:
    print(coordinate)
# plot the coordinates
x_coordinates = [x for x, y in cartesian_coordinates]
y_coordinates = [y for x, y in cartesian_coordinates]
# plot coordinates with a number
for i, txt in enumerate(combined):
    plt.annotate(i, (y_coordinates[i], x_coordinates[i]))

# regulkar plot
plt.scatter(y_coordinates, x_coordinates)

# set scale of both axis from 0 tot 400000
plt.xlim(0, 800000)
plt.ylim(0, 1250000)
plt.show()
