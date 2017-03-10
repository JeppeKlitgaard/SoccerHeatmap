import bs4 as bs
import numpy as np
import matplotlib.pyplot as plt
import sys

BINS = (30, 30)  # Pixels of heatmap

data = open("act.tcx", "r").read()


def plot_data(data, savename=""):
    """Take TCX data and show it."""
    soup = bs.BeautifulSoup(data, "xml")

    trackpoints = soup.find_all("Trackpoint")

    lats = []
    longs = []

    for trackpoint in trackpoints:
        try:
            time = trackpoint.Time.string
            lat = float(trackpoint.LatitudeDegrees.string)
            lng = float(trackpoint.LongitudeDegrees.string)
            alt = float(trackpoint.AltitudeMeters.string)
            dist = float(trackpoint.DistanceMeters.string)
            # TODO EXTRACT SPEED
        except AttributeError as e:
            print("Got error during parsing of a trackpoint. Skipping.")
            print("Error: {}".format(e))
            continue

        lats.append(lat)
        longs.append(lng)

        print(time, lat, lng, alt, dist)
        print("###")

    heatmap, xedges, yedges = np.histogram2d(lats, longs, bins=BINS)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    plt.clf()
    plt.imshow(heatmap.T, extent=extent, origin="lower")
    plt.show()

    if savename:
        plt.savefig(savename)


if __name__ == '__main__':
    try:
        fn = sys.argv[1]
    except IndexError:
        sys.exit("Need argument: filename")

    data = open(fn, "r").read()

    savename = fn.split(".")[0] + ".png"
    plot_data(data, savename=savename)
