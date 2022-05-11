import matplotlib.pyplot as plt
from math import sin, cos, radians as rad
import random
from shapely.geometry import Polygon, LineString, mapping, MultiPolygon
from shapely.ops import polygonize

from geojson import Feature, FeatureCollection, dump

height = 100
length = 100
step = 10

# схрон полигонов
pole = [Polygon([(0, 0), (0, height), (length, height), (length, 0)])]

# количество трещин
f = 2
for i in range(f):
    if i % 2:
        x, y = 0, random.randint(0, height)
        fi = 0
    else:
        x, y = random.randint(0, length), 0
        fi = 90

    b = [(x, y)]
    while 0 <= x < length and 0 <= y < height:
        a = rad(random.randint(-90 + fi, 90 + fi))
        x += step * cos(a)
        y += step * sin(a)

        b += [(x, y)]

    pole_2 = []
    for k in pole:
        pole_2 += [poly for poly in polygonize(k.boundary.union(LineString(b))) if
                   poly.representative_point().within(k)]
    pole = pole_2

# нарисовать их

# for i in pole:
#     plt.plot(*i.exterior.xy)
# plt.show()


pole = MultiPolygon(pole)
with open('fragments.geojson', 'w') as f:
    dump(mapping(pole), f)