import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimg
import matplotlib.pyplot as plt
from matplotlib._png import read_png
import pandas as pd
import numpy as np
import json
import os

from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

OUT_DIR = os.path.join('out', 'raw_1k')
BBOX_FILE = os.path.join(OUT_DIR, 'bboxes.json')

def make_map(figsize=(16, 12), projection=ccrs.PlateCarree()):
    fig = plt.figure(2, figsize=figsize)
    ax = plt.axes(projection=projection)
    gl = ax.gridlines(draw_labels=True)
    gl.xlabels_top = gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    return fig, ax


def create_pie(filename, data):
    plt.pie(data, explode=(0.01, 0.01, 0.01, 0.01, 0.01), labels=None, colors=('red','pink','white',(0.9, 1, 0.9),'green'),
            autopct='%1.1f%%', startangle=90,
            radius=0.5)
    plt.axis('equal')
    plt.savefig(filename, transparent=True)
    plt.clf()


def analyze_file(fn):

    def get_bucket(x):
        if x < 0.15:
            return 0
        if x < 0.4:
            return 1
        if x < 0.6:
            return 2
        if x < 0.85:
            return 3
        return 4


    i=0
    sentiments = []
    try:
        with open(fn, 'r') as f:
            for line in f.readlines():
                i += 1
                if i % 2 == 1:
                    continue
                sentiments.append(float(line))

        sentiments = list(map(lambda x: get_bucket(x), sentiments))

        return np.bincount(sentiments)
    except:
        return [20] * 5


if __name__ == '__main__':
    bboxes = json.load(open(BBOX_FILE, 'r'))
    data = []
    for city, locations in bboxes.items():
        C_long = (float(locations[0]) + float(locations[2])) / 2
        C_lat = (float(locations[1]) + float(locations[3])) / 2
        entry = [city] + locations + [C_long, C_lat]
        data.append(entry)

    data = pd.DataFrame(data, columns=['city', 'SW_long', 'SW_lat', 'NE_long', 'NE_lat', 'C_long', 'C_lat'])
    for i, d in enumerate(data.values):
        fn = 'img/pie_{}.png'.format(d[0])
        sent_fn = os.path.join(OUT_DIR, '{}_tweets.txt.sentiment'.format(d[0]))
        create_pie(fn, analyze_file(sent_fn))

    MIN_LNG = min(data['SW_long']) - 2
    MAX_LNG = max(data['NE_long']) + 2
    MIN_LAT = min(data['SW_lat']) - 2
    MAX_LAT = max(data['NE_lat']) + 2


    extent = [MIN_LNG, MAX_LNG, MIN_LAT, MAX_LAT]
    request = cimg.OSM()
    fig, ax = make_map(figsize=(13,10), projection=request.crs)
    ax.set_extent(extent)
    ax.margins(0)
    ax.add_image(request, 6) # 14 je nastaveni zoom-level pro OSM mapy, cim vyssi cislo, tim vice detailu a tim dele trva stahovani
    for i, d in enumerate(data.values):
        fn = 'img/pie_{}.png'.format(d[0])
        coords = ((d[-2] - MIN_LNG) / (MAX_LNG - MIN_LNG), (d[-1] - MIN_LAT) / (MAX_LAT - MIN_LAT))
        imageData = read_png(fn)
        newax = fig.add_axes([coords[0] * 0.9, coords[1] * 0.75, 0.1, 0.1], zorder=10)
        newax.imshow(imageData)
        newax.axis('off')

    plt.show()
