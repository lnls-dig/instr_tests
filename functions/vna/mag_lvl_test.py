import numpy as np
import math


def mag_lvl_test(x, y, zone_freq, zone_type, zone_mag):

    index_nearest = find_index_nearest(x, zone_freq)

    # test for each zone
    for i in range(len(index_nearest)-1):
        bot = index_nearest[i]
        top = index_nearest[i+1] + 1 # added 1 to eval last element of y array
        if zone_type[i] == -1:
            if max(y[bot:top]) > zone_mag[i]:
                return False
        elif zone_type[i] == 1:
            if min(y[bot:top]) < zone_mag[i]:
                return False
        elif zone_type[i] == 0:
            pass
        else:
            print("\nZone type must be -1, 0 or 1\n")
            exit()

    return True


def find_index_nearest(array,value):
    """find index of nearest element in array of each element in value"""
    nearest = []
    for i in value:
        idx = np.searchsorted(array, i, side="left")
        if math.fabs(i - array[idx-1]) < math.fabs(i - array[idx]):
            nearest.append(idx-1)
        else:
            nearest.append(idx)
    return nearest
