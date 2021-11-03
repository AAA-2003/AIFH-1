import math #for sqrt

def euclidean_dist(arr1, arr2):
    s = 0
    for i in range(len(arr1)):
        d = (arr2[i] - arr1[i])**2
        s += d
    return math.sqrt(s)

def manhattan_dist(arr1, arr2):
    s = 0
    for i in range(len(arr1)):
        s += abs(arr1[i] - arr2[i])
    return s

def  chebyshev_dist(arr1, arr2):
    out = 0
    for i in range(len(arr1)):
        d = abs(arr1[i] - arr2[i])
        out = max(out, d)
    return out
