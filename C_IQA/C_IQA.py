# Comparison-based Image Quality Assessment (This version consider the sensitivity difference to the same distortion)
# This is the texture-based C-IQA (CT_IQA)
# input: image1, image2
# output: relative quality of image1 based on image2
import cv2
import numpy as np
from scipy import signal


class ComparisonIQA:
    def __init__(self, thresh=0.12, win_size = 9):
        self.thresh = thresh
        self.win_size = win_size

    def c_iqa(self, img1, img2):
        N = self.win_size
        h_filter = np.ones([N, N])/(N*N)
        input1 = img1.astype(float)
        input2 = img2.astype(float)
        diff_input = input1 - input2
        ave_input1 = signal.convolve2d(img1, h_filter)
        ave_input2 = signal.convolve2d(img2, h_filter)
        ave_diff_input = signal.convolve2d(diff_input, h_filter)
        ave_input1[ave_input1 < 1/(N*N)] = 1/(N*N)
        ave_input2[ave_input2 < 1/(N*N)] = 1 / (N * N)
        dx, dy = np.gradient(diff_input)
        ept_dx = N**2 * signal.convolve2d(dx**2, h_filter)
        ept_dy = N ** 2 * signal.convolve2d(dy ** 2, h_filter)
        ept_dx_dy = N**2 * signal.convolve2d(dx*dy, h_filter)
        lamada1 = (ept_dx + ept_dy - ((ept_dx + ept_dy)**2 - 4*(ept_dx*ept_dy - ept_dx_dy**2))/0.5)**0.5
        lamada2 = (ept_dx + ept_dy + ((ept_dx + ept_dy) ** 2 - 4 * (ept_dx * ept_dy - ept_dx_dy ** 2)) / 0.5) ** 0.5
        q_map = np.abs(lamada2 - lamada1)/(lamada1 + lamada2)
        contri1 = signal.convolve2d(input1*diff_input, h_filter) - ave_input1*ave_diff_input
        contri2 = signal.convolve2d(input2 * diff_input, h_filter) - ave_input2 * ave_diff_input
        ctrb_map = (contri1 - contri2)/(ave_input1 + ave_input2) *2
        weight_map = 2*(q_map > self.thresh) - 1
        score = np.mean(weight_map*ctrb_map)
        return score, weight_map


if __name__ == '__main__':
    CQ_ind = ComparisonIQA()
    img1 = cv2.imread('2_org.png', 0)
    img2 = cv2.imread('2_pclr.png', 0)
    print('The quality of image1 based image2 is {}').format(CQ_ind.c_iqa(img1, img2))
