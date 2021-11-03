"""
K-Means clustering algorithm, using RANDOM initialization & FORGY
Alteration custom algorithm: result NO BETTER
Created on Sat Aug 10 17:51:43 2019
@author: Ayngaran Adalarasu
"""
# ##---Imports:---## #
import math
import random
from PIL import Image
import numpy as np

vectors = []  # houses all vectors
'''
Structure of a vector (Dictionary):
*'id'  : <name of vector>(optional)
*'data': list of numeric elements of vectors
'''

clusters = {}  # Houses all clusters
'''
Structure of Clusters (Dictionary):
*It is a dictionary with numeric indices(starting from 1) for each cluster
*Each element houses a Cluster

Structure of each Cluster (Dictionary):
*'items'   : contains all vectors(dictionaries) in a list
*'centroid': mean vector from all items, calculated by update_centroid(), has no id   
'''


# ##---Functions---## #

# load vectors from given file name(CSV) into vectors list
# Can also load images if used, f_name should be a list of image file names within data/char_bitmap
# if id is set false, it means data set of vectors have no id name
# Returns: Nothing
def load_vectors(f_name, id_index=-1, img=False, none_val=None):

    # opens bitmap image in f_name and crops & down samples then returns 2D array
    def get_img(f):
        def crop_image(img):
            # finding vertical starting pixel of image:
            for i in range(len(img)):
                if False in img[i]:
                    v_h = i
                    break
            # find vertical last pixel of image:
            v_l = len(img) - 1
            for i in range(len(img) - 1, v_h, -1):
                if False in img[i]:
                    v_l = i
                    break
            img = img[v_h:v_l + 1]  # cropping image vertically
            # Finding horizontal left(starting point) and horizontal right(ending point) of image
            h_l = len(img[0]) - 1
            h_r = 0
            for row in img:
                got_h_l = False
                for i in range(len(row)):
                    if row[i] == False and i < h_l:
                        h_l = i
                        got_h_l = True
                    elif row[i] == True and row[i - 1] == False and i > h_r:
                        h_r = i - 1
            # cropping image horizontally
            cropped_img = []
            for row in img:
                temp = []
                for i in range(h_l, h_r + 1):
                    if row[i]:
                        temp.append(0)
                    else:
                        temp.append(1)
                cropped_img.append(temp)
            return cropped_img

        def down_sample(img, row_p, col_p):
            raw_row = math.ceil(len(img) / float(row_p)) * row_p
            row_down = int(raw_row / row_p)
            raw_col = math.ceil(len(img[0]) / float(col_p)) * col_p
            col_down = int(raw_col / col_p)
            out_img = []
            for i in range(row_p):
                temp = []
                for x in range(col_p):
                    temp.append(0)
                out_img.append(temp)

            for row_i in range(len(img)):
                for col_i in range(len(img[0])):
                    if img[row_i][col_i] == 1:
                        out_img[row_i / row_down][col_i / col_down] = 1
            return out_img
        im = Image.open("data/char_bitmap/" + f + ".bmp")
        p = np.array(im)
        img = crop_image(p)
        img = down_sample(img, 7, 5)
        return img

    global vectors
    if not img:
        f = open("data/"+f_name+".txt", 'r')
        f.readline()  # omitting 1st line
        for line in f:
            elements = line.split(',')
            elements[id_index] = elements[id_index].strip('\n')
            if id_index is not None:
                data_temp = elements[0:id_index]
                if id_index != -1:
                    data_temp += elements[id_index+1::]
                data_temp = map(float, data_temp)
                if none_val is not None:
                    for x in range(len(data_temp)):
                        if data_temp[x] == none_val:
                            data_temp[x] = None
                vectors.append({'id': elements[id_index], 'data': data_temp})
            else:
                vectors.append({'id': '', 'data': map(float, elements)})
        f.close()
    elif img:
        for f in f_name:
            image_list = get_img(f)
            out = []
            for l in image_list:
                out += l
            vectors.append({'id':f, 'data':out})


# finds euclidean distance between 2 vectors
# give only vector data no id
# returns: list with input no. of elements
def distance(a, b):
    dist = 0
    for i in range(0, len(a)):
        if a[i] is not None and b[i] is not None:
            dist += math.pow((a[i]-b[i]), 2)
    #return math.sqrt(dist)
    return dist


# subroutine for matrix addition
def add(a, b):
    o = []
    for x in range(len(a)):
        if a[x] is None:
            a[x] = 0
        if b[x] is None:
            b[x] = 0
        o.append(a[x] + b[x])
    return o


# Prints entire cluster dictionary
def print_clusters(prt_id=True):
    for i in clusters.keys():
        cluster = clusters[i]
        print "Cluster "+str(i)+": (No. of items:"+str(len(cluster['items']))+")"
        for item in cluster['items']:
            if prt_id:
                print item['id'], item['data']
            else:
                print item['data']


# ##---Clustering algorithm: k-means Functions---## #

# finds closest cluster for a given vector:
# by comparing with centroids using distance()(euclidean)
# Returns least cluster index no.
def find_nearest_cluster(a):
    global clusters
    v = a['data']
    least_cluster = clusters.keys()[0]
    least_dist = None
    for i in clusters.keys():
        cluster = clusters[i]
        dist = distance(v, cluster['centroid'])
        if dist < least_dist or least_dist is None:
            least_dist = dist
            least_cluster = i
    return least_cluster


# Moves each vector of a cluster to least distance(To centroid) cluster
# iterates through each vector of each cluster, uses find_nearest_cluster() for finding ideal cluster
# Returns: True if no changes were made, false otherwise
def assignment():
    global clusters
    done = True
    for i in clusters.keys():
        cluster = clusters[i]
        for v in cluster['items']:
            target_cluster = find_nearest_cluster(v)
            if target_cluster != i:
                cluster['items'].remove(v)
                clusters[target_cluster]['items'].append(v)
                done = False
    return done


# Finds centroid for each cluster
# cluster = average of all vectors in a cluster
# Function called after calling initialize_clusters() or assignment()
# Returns: Nothing
def update_centroid():
    global clusters

    for i in clusters.keys():
        cluster = clusters[i]
        out = cluster['items'][0]['data']
        for v in cluster['items'][1:len(cluster['items'])+1]:
            out = add(out, v['data'])
        n = float(len(cluster['items']))
        for y in range(len(out)):
            out[y] = out[y]/n
        cluster['centroid'] = out


# puts EQUAL number of vectors in each cluster('items') from vectors(list) RANDOMLY
# Creates k number of clusters
# Returns: Nothing
def initialize_clusters(k):
    global vectors, clusters
    clusters = {}
    # shuffles vectors in vectors list & puts in random order
    for i in range(len(vectors)):
        x = random.randint(0, len(vectors)-1-i)
        temp = vectors[x]
        del vectors[x]
        vectors.append(temp)

    # Puts equal number of vectors in each cluster
    start = 0
    end = len(vectors)/k
    for i in range(1, k+1):
        clusters[i] = {'centroid': None, 'items': vectors[start:end]}
        start = end
        end += (len(vectors))/k
    # Puts remaining vectors 1 by 1 in each cluster
    # occurs when No. of clusters is not divisible by l
    i = 1
    end -= (len(vectors))/k
    while end < len(vectors):
        clusters[i]['items'].append(vectors[end])
        end += 1
        i += 1


def forgy_init(k, list_centroids):
    global vectors, clusters
    clusters = {}
    for i in range(1, k+1):
        clusters[i] = {'centroid': list_centroids[i], 'items': []}
    for x in vectors:
        clusters[find_nearest_cluster(x)]['items'].append(x)


# Main k-means clusterization algorithm
# calls: initialize_clusters(), update_centroid(), assignment() in proper order
# k number of clusters are created
# Runs till all items are clusterized
# Returns: true when done
def clusterize_data(k, init='random', list_of_centroids=None):
    if init == 'random':
        initialize_clusters(k)
    elif init == 'forgy':
        forgy_init(k, list_of_centroids)
    # print_clusters()
    update_centroid()
    while not (assignment()):
        update_centroid()
    return True


def adv_clusterize(k, n):
    global clusters
    list_centroids = {}
    base_centroids = {}
    clusterize_data(k)
    for x in clusters.keys():
        list_centroids[x] = [clusters[x]['centroid']]
        base_centroids[x] = {'data':clusters[x]['centroid']}
    for i in range(n-1):
        clusterize_data(k)
        for x in clusters.keys():
            nearest = find_nearest_cluster(base_centroids[x])
            list_centroids[x].append(clusters[nearest]['centroid'])

    for k in list_centroids.keys():
        clu = list_centroids[k]
        out = clu[0]
        n = float(len(clu))
        clu = clu[1::]
        for l in clu:
            out = add(out, l)
        for i in range(len(out)):
            out[i] = out[i]/n
        list_centroids[k] = out
    print list_centroids
    clusterize_data(k, init='forgy', list_of_centroids=list_centroids)
    #forgy_init(k, list_centroids)


# ##---Main Program---## #


load_vectors('iris_data')  # loading vectors array
# load_vectors(images, img=True)
# print vectors
# clusterize_data(3)

adv_clusterize(3, 10)
print_clusters()


# ##---END OF CODE---## #
