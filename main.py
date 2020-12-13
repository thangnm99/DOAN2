import cv2
import numpy as np
# import matplotlib.pyplot as plt
from skimage import morphology,io
from keras.models import load_model

def PreProcess(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h,w = img.shape
    clane = cv2.createCLAHE(clipLimit=2, tileGridSize=(5, 5))
    processed_img = clane.apply(img)
    processed_img = cv2.GaussianBlur(processed_img, (3, 3), 0)
    processed_img = cv2.convertScaleAbs(processed_img, alpha=1.1, beta=0)
    processed_img = cv2.adaptiveThreshold(processed_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 7)
    processed_img = (255 - processed_img)
    img_col_sum = np.sum(processed_img,axis=1)
    print(thresh)
    i = 0
    while (img_col_sum[i]==0) and (i <=h) : i = i +1
    j = h-1
    while (img_col_sum[j]==0) and (j >=0) : j = j -1
    processed_img= processed_img[i:j,:]
    return processed_img

def pre_classify(img):
    h,w = img.shape
    i = np.sum(img)
    j = np.sum(img[h//2:,:])
    if j <2  : rsl ='noise'
    else :

      if (j/i) > 0.8 and j >1: rsl = 'comma'
      else :
        num_label, labels = cv2.connectedComponents(img, connectivity=8)
        rsl = 'number'
        print(num_label)
        if num_label > 2 :
          for i in range(num_label-1,0,-1):
              label = (labels == i).astype(np.uint8)
              pix_count = np.sum(label)
              br_img = label[h-h//2:,w-w//3:]
              pix_count_br= np.sum(br_img)
              ratio = pix_count_br/pix_count
              if ratio > 0.7:
                  rsl = 'number with comma'
                  break
    return  rsl


class recognize():

    # def __init__(self,path):
        # self.path = path

    def recog(path):
        model = load_model('saved_model.hdf5')
        j = 0
        img = PreProcess(path)
        # processed_img = morphology.thin(img).astype('uint8')
        processed_img = img
        # processed_img = processed_img * 255
        h,w = processed_img.shape
        io.imsave('images/processed_img.png',processed_img)
        chars = []
        img_row_sum = np.sum(processed_img ,axis=0)
        #
        ischar = False
        minval = img_row_sum.min()
        print('\n')
        so = ''
        for x in range(w):
            if img_row_sum[x] > minval and ischar == False:
                x1 = x
                ischar = True
            else :
                if (img_row_sum[x] == minval or x == w-1) and ischar == True :
                    x2 = x
                    if x2 > x1+1 :
                        char = processed_img[:,x1:x2]
                        # char = cv2.dilate(char,(3,3),3)
                        type_char = pre_classify(char)
                        # print(type_char)
                        io.imsave('images/segmentdigit%s.png'%str(j),char)
                        if type_char == 'comma' : so = so +','
                        else :
                          if type_char != 'noise' :
                            char = img[:,x1:x2]
                            char = cv2.resize(char,(16,20))
                            char = np.pad(char,((4,4),(6,6)),mode='constant')
                            io.imsave('images/segmentdigit%s.png' % str(j), char)
                            kq = model.predict(char.reshape(1,28,28,1))
                            chars.append(char)
                            so = so + str(np.argmax(kq))
                            if type_char == 'number with comma' : so = so + ','
                        print(type_char)
                        j = j + 1
                    ischar = False
        return  so

if __name__ =='__main__' :
    kq = []
    for i in range(21) :
        filedir = 'images/d%s.png'%str(i)
        predict_result = recognize.recog(filedir)
        kq.append(predict_result)
    print(kq)