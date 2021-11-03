from PIL import Image
import numpy as np
import math


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

def get_img(f_name):
    im = Image.open("data/Character_bitmap/"+f_name+".bmp")
    p = np.array(im)
    img = crop_image(p)
    img = down_sample(img, 7, 5)
    return img

#The character image data set
number_classes = {'9':get_img('9a'), '8':get_img('8a'), '7':get_img('7a'), '6':get_img('6a'), '5':get_img('5a'),
                  '4':get_img('4a'), '3':get_img('3a'), '2':get_img('2a'), '1':get_img('1a'), '0':get_img('0a')}


def print_img(img):
    for row in img:
        temp = ''
        for i in row:
            if (i == 1):
                temp += '~'
            else:
                temp += ' '
        print temp

def euclidean_dist(arr1, arr2):
    s = 0
    for i in range(len(arr1)):
        for x in range(len(arr1[0])):
            d = (arr2[i][x] - arr1[i][x])**2
            s += d
    return math.sqrt(s)


lowest_dist = euclidean_dist(number_classes['9'], get_img('draw_pad_1'))
lowest_class = '9'
for key in number_classes.keys():
    t = euclidean_dist(number_classes[key], get_img('draw_pad_1'))
    if(t < lowest_dist):
        lowest_class = key
        lowest_dist = t
print lowest_class
print_img(get_img('draw_pad_1'))



'''
for key in number_classes:
    print '\n\n'
    print_img(number_classes[key])
'''


