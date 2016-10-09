import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimg
import matplotlib.pyplot as plt
from matplotlib._png import read_png
import pandas as pd
import json

from cartopy.io import shapereader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

BBOX_FILE = 'out/bboxes.json'

def make_map(figsize=(16, 12), projection=ccrs.PlateCarree()):
    fig = plt.figure(figsize=figsize)
    ax = plt.axes(projection=projection)
    gl = ax.gridlines(draw_labels=True)
    gl.xlabels_top = gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    return fig, ax

imageData = read_png('pic1.png')
ex = (-74,40,-75,41)
bboxes = json.load(open(BBOX_FILE, 'r'))
data = []
for city, locations in bboxes.items():
    C_long = (float(locations[0]) + float(locations[2])) / 2
    C_lat = (float(locations[1]) + float(locations[3])) / 2
    entry = [city] + locations + [C_long, C_lat]
    data.append(entry)

data = pd.DataFrame(data, columns=['city', 'SW_long', 'SW_lat', 'NE_long', 'NE_lat', 'C_long', 'C_lat'])
MIN_LNG = min(data['SW_long']) - 2
MAX_LNG = max(data['NE_long']) + 2
MIN_LAT = min(data['SW_lat']) - 2
MAX_LAT = max(data['NE_lat']) + 2


extent = [MIN_LNG, MAX_LNG, MIN_LAT, MAX_LAT]
print(extent)
request = cimg.OSM()
fig, ax = make_map(figsize=(13,10), projection=request.crs)
ax.set_extent(extent)
ax.margins(0)
labels=['','','','']
explode = (0,0,0,0)
colors = ['red','blue','green','cyan']
ax.add_image(request, 4) # 14 je nastaveni zoom-level pro OSM mapy, cim vyssi cislo, tim vice detailu a tim dele trva stahovani
for d in data.values:
    print(d)
    coords = ((d[-2] - MIN_LNG) / (MAX_LNG - MIN_LNG), (d[-1] - MIN_LAT) / (MAX_LAT - MIN_LAT))
    print(coords)
    # fig.figimage(imageData, fig.bbox.xmax - width, height)
    newax = fig.add_axes([coords[0] * 0.95, coords[1] * 0.85, 0.05, 0.05], zorder=10)
    newax.imshow(imageData)
    newax.axis('off')
# plt.pie(np.random.random(4), explode=explode, labels=labels, colors=colors,
#        autopct='%1.1f%%', shadow=True, startangle=90,
#        radius=0.25, center=(-1,0), frame=True)
# ax.pie(np.random.random(4), explode=explode, labels=labels, colors=colors,
#        autopct='%1.1f%%', shadow=True, startangle=90,
#        radius=0.25, center=(1, 1), frame=True)
# ax.pie(np.random.random(4), explode=explode, labels=labels, colors=colors,
#        autopct='%1.1f%%', shadow=True, startangle=90,
#        radius=0.25, center=(0, 1), frame=True)
# ax.pie(np.random.random(4), explode=explode, labels=labels, colors=colors,
#        autopct='%1.1f%%', shadow=True, startangle=90,
#        radius=0.25, center=(1, 0), frame=True)
# ax.scatter(data['C_long'], data['C_lat'], transform=ccrs.PlateCarree(), alpha=0.6, s=40, c='red')
plt.show()
