import pyproj
import matplotlib.pyplot as plt


def wgs84_to_cartesian(origin, coordinates):
    origin_lat, origin_lon = origin
    transformer = pyproj.Transformer.from_crs('epsg:4326', 'epsg:3857')  # WGS84 to Web Mercator projection

    origin_x, origin_y = transformer.transform(origin_lon, origin_lat)

    transformed_coordinates = []
    for lat, lon in coordinates:
        x, y = transformer.transform(lon, lat)
        transformed_coordinates.append((x - origin_x, y - origin_y))

    return transformed_coordinates


## Case study 1
origin_coordinate = (51.000, 2.500)
wgs84_coordinates = [
    (51.700 , 2.928),
    (52.280 , 4.084),
    (52.714 , 4.265),
    (52.638 , 3.709),
    (53.000 , 3.795),
    (52.697 , 3.370),
    (53.136 , 3.188),
    (53.396 , 3.230),
    (53.226 , 3.965),
    (54.023 , 5.652),
    (54.247 , 5.587)
] 


cartesian_coordinates = wgs84_to_cartesian(origin_coordinate, wgs84_coordinates)

# Print the transformed coordinates
for coordinate in cartesian_coordinates:
    print(coordinate)

# plot the coordinates
x_coordinates = [x for x, y in cartesian_coordinates]
y_coordinates = [y for x, y in cartesian_coordinates]
plt.scatter(y_coordinates, x_coordinates)
# set scale of both axis from 0 tot 400000
plt.xlim(0, 400000)
plt.ylim(0, 400000)
plt.show()





