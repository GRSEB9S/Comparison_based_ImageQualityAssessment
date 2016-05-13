# Comparison-based Image Quality Assessment
# input: image1, image2
# output: relative quality of image1 based on image2
import cv2
import numpy as np

class ComparisonIQA:
    def __init__(self, thresh = 0.12):
        self.thresh = thresh
    def C_IQA(self,img1,img2):
        dif = np.mean(img1) - np.mean(img2)
        return dif

if __name__ == '__main__':
    CQ_ind = ComparisonIQA()
    img1 = cv2.imread('1_org.png')
    img2 = cv2.imread('1_pclr.png')
    print('The quality of image1 based image2 is {}').format(CQ_ind.C_IQA(img1,img2))
