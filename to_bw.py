import os
import cv2
import numpy as np
import random
import hashlib

def random_str():
    '''
    Return a 6 char random string.
    '''
    seed = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    string = ''
    for i in range(6):
        current_pos = random.random()
        char = seed[int(len(seed) * current_pos)]
        string += char
    return string

def md5_checker(filepath):
    '''
    Check existed md5, prevent from output dupicated picture.
    '''
    with open(filepath, 'rb') as f:
        content = f.read()
        md5 = hashlib.md5(content).hexdigest()
    return md5

def get_labels(basedir):
    '''
    Return a dictionary with filepath(content) and labels(key) in picture resource folder, picture format: .png
    '''
    labels = os.listdir(basedir)
    dic = dict()
    for i in range(len(labels)):
        file_ls = os.listdir(basedir + '/' + labels[i])
        dic[labels[i]] = [basedir + '/' + labels[i] + '/' + file for file in file_ls]
    return dic

def make_bw(path_dict, new_dirname, div = 80):
    '''
    path_dict: dictionary
    new_dirname: String
    Load pictures in source folder and save them as binary picture(black and white)
    '''
    if not os.path.exists(new_dirname):
        os.mkdir(new_dirname)
    else: 
        print('Warning: Folder ' + new_dirname + ' Already Existed')
    
    for picname in path_dict:
        file_ls = path_dict[picname]
        for pic in file_ls:
            try:
                # cannot use imread, filename contains Chinese
                img = cv2.imdecode(np.fromfile(pic, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
                im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                im_bw = cv2.threshold(im_gray, div, 255, cv2.THRESH_BINARY)[1]
                # create subfolders, folder name = label of pictures
                subfolder = new_dirname + '/' + picname
                img_towrite = cv2.imencode('.png', im_bw)[1]
                if not os.path.exists(subfolder):
                    os.mkdir(subfolder)
                    img_towrite.tofile(new_dirname + '/' + picname + '/' + random_str() +'.png')
                else:
                    files_existed = os.listdir(subfolder)
                    label = 0
                    
                    for pic in files_existed:
                        existed_md5 = md5_checker(subfolder + '/' + pic)
                        if existed_md5 == hashlib.md5(img_towrite).hexdigest():
                            label = 1
                        break
                    if label == 0:
                        img_towrite.tofile(new_dirname + '/' + picname + '/' + random_str() +'.png')

            except Exception as e:
                print(e)
                print('File ' + pic + ' error, please check file type...')
                continue

if __name__ == '__main__':
    file_dic = get_labels('./labels')
    make_bw(file_dic, 'bw')
    
    
