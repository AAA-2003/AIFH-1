from PIL import Image
import numpy as np
import math
import time

def crop_image(img):
    #finding vertical starting pixel of image:
    for i in range(len(img)):
        if False in img[i]:
            v_h = i
            break
    #find vertical last pixel of image:
    v_l = len(img) - 1
    for i in range(len(img)-1, v_h, -1):
        if False in img[i]:
            v_l = i
            break
    img = img[v_h:v_l+1]#cropping image vertically
    #Finding horizontal left(starting point) and horizontal right(ending point) of image
    h_l = len(img[0])-1
    h_r = 0
    for row in img:
        got_h_l = False
        for i in range(len(row)):
            if row[i] == False and i < h_l:
                h_l = i
                got_h_l = True
            elif row[i] == True and row[i-1] == False and  i > h_r:
                h_r = i-1
    #cropping image horizontally
    cropped_img = []
    for row in img:
        temp = []
        for i in range(h_l, h_r+1):
            if row[i]:
                temp.append(0)
            else:
                temp.append(1)
        cropped_img.append(temp)
    return cropped_img


def down_sample(img, row_p, col_p):
    raw_row = math.ceil(len(img)/float(row_p)) * row_p
    row_down = int(raw_row/row_p)
    raw_col = math.ceil(len(img[0])/float(col_p)) * col_p
    col_down = int(raw_col/col_p)
    out_img =[]
    for i in range(row_p):
        temp = []
        for x in range(col_p):
            temp.append(0)
        out_img.append(temp)

    for row_i in range(len(img)):
        for col_i in range(len(img[0])):
            if img[row_i][col_i] == 1:
                out_img[row_i/row_down][col_i/col_down] = 1
    return out_img

#opens bitmap image in f_name and crops & down samples then writtens 2D array
def get_img(f_name):
    im = Image.open("data/Character_bitmap/"+f_name+".bmp")
    p = np.array(im)
    img = crop_image(p)
    img = down_sample(img, 7, 5)
    return img

#prints monochrome image in 2D array form
def print_img(img):
    for row in img:
        temp = ''
        for i in row:
            #temp += str(i)
            if (i == 1):
                temp += '~'
            else:
                temp += ' '
        print temp

#main distance finding algorithmn works on 2D arrays
def euclidean_dist(arr1, arr2):
    s = 0
    for i in range(len(arr1)):
        for x in range(len(arr1[0])):
            d = (arr2[i][x] - arr1[i][x])**2
            s += d
    return math.sqrt(s)
    #return s

def matrix_add(arr1, arr2):
    for i in range(len(arr1)):
        for x in range(len(arr1[0])):
            arr1[i][x] += arr2[i][x]
    return arr1

#Main array which initially contains compare files of respective number
#later contains actuall 2D images of files in list
char_classes = {'9':['9a', '9b', '9c'], '8':['8a', '8b', '8c', '8d', '8e'], '7':['7a', '7b', '7c', '7d'], '6':['6a', '6b', '6c', '6d'], '5':['5a', '5e', '5g'],
                  '4':['4a', '4b', '4c'], '3':['3a', '3b', '3c', '3e', '3d', '3f', '3g'], '2':['2a', '2b', '2c'], '1':['1a', '1b', '1c'], '0':['0a', '0b', '0c']}
for key in char_classes:
    char_classes[key] = map(get_img, char_classes[key])
#computing average ideal image vectors
for key in char_classes.keys():
    avg_img = char_classes[key][0]
    n = 1
    for i in range(1, len(char_classes[key])):
        avg_img = matrix_add(avg_img, char_classes[key][i])
        n+=1
    for i in avg_img:
        for j in range(len(i)):
            i[j] = float(i[j])/n
    char_classes[key] = avg_img

#Main recoganizing class
def recoganize(img_f):
    in_img = get_img(img_f)
    lowest_dist = euclidean_dist(char_classes['9'], in_img) #setting initial compare value
    lowest_class = '9'
    for key in char_classes.keys():
        t = euclidean_dist(char_classes[key], in_img)
        if t < lowest_dist:
           lowest_class = key
           lowest_dist = t
    #print_img(in_img)
    return lowest_class

print_img(get_img('draw_pad'))

###***************************####
#Main program
print recoganize('draw_pad')
#print_img(char_classes['9'])
