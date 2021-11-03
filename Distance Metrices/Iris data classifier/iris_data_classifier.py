'''#Created by Ayngaran Adalarasu
#date: 27/07/2019
#name: Iris data classifier
#Specifically written for Iris data set
#Classifies data into given  classes(specified in items list)
#Uses distance metrics algorithm to classify data
'''

import math #for sqrt

#Distance metrics alogrithms
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
    compare_element = 0
    for i in range(len(arr1)):
        d = abs(arr1[i] - arr2[i])
        if d  > out:
            compare_element = i
        out = max(out, d)
    #print compare_element
    return out


#matrix addition function
def matrix_add(arr1, arr2):
    for i in range(len(arr1)):
        arr1[i] = arr1[i] + arr2[i]
    return arr1

# main dictionary containing all classes
items = {'Iris-setosa': [0,0,0,0], 'Iris-versicolor': [0,0,0,0], 'Iris-virginica':[0,0,0,0]}

#items = {}


    
'''opens file and populates 'items' with mean values of all attributes(for each item)
#speccifically written for iris_data.txt
#format: "sepal_length","sepal_width","petal_length","petal_width","class"
#argument - file name (inside data folder of project)
'''
inp_data = []
def get_mean_vals(f_name):
    f = open("data\\"+f_name+".txt", "r")
    data_no = {'Iris-setosa': 0, 'Iris-versicolor': 0, 'Iris-virginica':0} #count of each observation
    for line in f:
        if "\"" in line: #doesnt parse line if findas " - for ignoring comments
            continue
        line = line.strip('\n')
        line_data = line.split(',')
        type = line_data[len(line_data)-1] #extracting last class type from line
        data_no[type] += 1
        line_data = line_data[0:len(line_data)-1]
        line_data = map(float, line_data)
        items[type] = matrix_add(items[type], line_data)
        
        inp_data.append([line_data,type])
    #dividing sum
    for cat in items.keys():
        for i in range(len(items[cat])):
            items[cat][i] /= data_no[cat]
    f.close()


def find_type(inp, items):
    out = {}
    for t in items.keys():
        dist = 0
        '''which ever distance methods we want to use should be uncommented
            More than 1 distance method can be uncommented'''
        
        dist = euclidean_dist(inp, items[t])
        dist += manhattan_dist(inp, items[t])
        dist += chebyshev_dist(inp, items[t])
        out[t] = dist
    least_dist = out.keys()[0]
    for t in out.keys():
        if out[t] < out[least_dist]:
            least_dist = t
    #print out
    #print least_dist
    return least_dist


get_mean_vals('iris_data')
print items
#find how many of given iris flowers are classified correctly
correct = 0
for flower in inp_data:
    if find_type(flower[0], items) == flower[1]:
        correct += 1
   
print correct, "/", len(inp_data)
#find_type([4.9, 2.5, 4.5, 1.7] ,items)
