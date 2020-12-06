import cv2
import numpy as np
# import matplotlib.pyplot as plt
from skimage import morphology
from keras.models import load_model


def PreProcess(path):
    img = cv2.imread(path,0)
    h,w = img.shape
    clane = cv2.createCLAHE(clipLimit=2, tileGridSize= (5,5))
    processed_img = clane.apply(img)
    # processed_img = img
    # processed_img = cv2.dilate(processed_img,(3,3),7)
    # processed_img = cv2.medianBlur(processed_img,3,3)
    # processed_img = cv2.GaussianBlur(processed_img,(1,1),cv2.BORDER_DEFAULT)
    processed_img = cv2.convertScaleAbs(processed_img,alpha = 1.1, beta = 0)
    processed_img = cv2.adaptiveThreshold(processed_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,5,10)
    processed_img = (255-processed_img)
    img_col_sum = np.sum(processed_img,axis=1)
    i = 0
    while (img_col_sum[i]==0) and (i <=h) : i = i +1
    j = h-1
    while (img_col_sum[j]==0) and (j >=0) : j = j -1
    processed_img= processed_img[i:j,:]
    return processed_img

def pre_classify(img):
    num_label,labels = cv2.connectedComponents(img,connectivity=8)
    h,w = img.shape
    i = np.sum(img)
    j = np.sum(img[h//2:,:])
    if j == 0 : rsl ='noise'
    else :
      if (j/i) > 0.8 and j >1: rsl = 'comma'
      else :
        rsl = 'number'
        if num_label > 2 :
          for i in range(num_label-1,0,-1):
              label = (labels == i).astype(np.uint8)
              pix_count = np.sum(label)
              br_img = label[h-h//3:,w-w//3:]
              pix_count_br= np.sum(br_img)
              ratio = pix_count_br/pix_count
              if ratio > 0.8:
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
        processed_img = morphology.thin(img).astype('uint8')
        # processed_img = img
        processed_img = processed_img * 255
        h,w = processed_img.shape
        # io.imsave('images/processed_img%s.png'%str(i),img)
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
                if img_row_sum[x] == minval and ischar == True :
                    x2 = x
                    if x2 > x1+1 :
                        char = processed_img[:,x1:x2]
                        # char = cv2.dilate(char,(3,3),3)
                        type_char = pre_classify(char)
                        # print(type_char)
                        # io.imsave('images/segmentdigit%s.png'%str(j),char)
                        if type_char == 'comma' : so = so +','
                        else :
                          if type_char != 'noise' :
                            char = img[:,x1:x2]
                            char = np.pad(char,3,mode='constant')
                            char = cv2.resize(char,(28,28))
                            # char = cv2.dilate(char,(3,3),3)
                            kq = model.predict(char.reshape(1,28,28,1))
                            chars.append(char)
                            so = so + str(np.argmax(kq))
                            if type_char == 'number with comma' : so = so + ','
                        # io.imsave('images/segmentdigit%s.png'%str(j),char)
                        j = j + 1
                    ischar = False
        return  so