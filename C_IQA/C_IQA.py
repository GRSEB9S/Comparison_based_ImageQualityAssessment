# Comparison-based Image Quality Assessment (This version consider the sensitivity difference to the same distortion)
# This is the texture-based C-IQA (CT_IQA)
# input: image1, image2
# output: relative quality of image1 based on image2
import numpy as np
from scipy import signal
import matplotlib.image as mpimg

class ComparisonIQA:
    def __init__(self, thresh=0.12, win_size = 9):
        self.thresh = thresh
        self.win_size = win_size

    def c_iqa(self, img1, img2):
        N = self.win_size
        h_filter = np.ones([N, N])/(N*N)
        input1 = img1.astype(complex)
        input2 = img2.astype(complex)
        diff_input = input1 - input2
        ave_input1 = signal.convolve2d(img1, h_filter, 'valid')
        ave_input2 = signal.convolve2d(img2, h_filter, 'valid')
        ave_diff_input = signal.convolve2d(diff_input, h_filter, 'valid')
        ave_input1[ave_input1 < 1/(N*N)] = 1/(N*N)
        ave_input2[ave_input2 < 1/(N*N)] = 1 / (N * N)
        dx, dy = np.gradient(diff_input)
        ept_dx = N**2 * signal.convolve2d(dx**2, h_filter, 'valid')
        ept_dy = N ** 2 * signal.convolve2d(dy ** 2, h_filter, 'valid')
        ept_dx_dy = N**2 * signal.convolve2d(dx*dy, h_filter, 'valid')
        b = (ept_dx + ept_dy)
        a = 1
        c = ept_dx*ept_dy - ept_dx_dy**2
        lamada1 = (b - (b**2 - 4*a*c)**0.5)/2
        lamada2 = (b + (b**2 - 4*a*c)**0.5)/2
        q_map = np.abs(lamada2 - lamada1)/(lamada1 + lamada2)
        contri1 = signal.convolve2d(input1*diff_input, h_filter, 'valid') - ave_input1*ave_diff_input
        contri2 = signal.convolve2d(input2 * diff_input, h_filter, 'valid') - ave_input2 * ave_diff_input
        ctrb_map = (contri1 - contri2)/(ave_input1 + ave_input2) *2
        weight_map = 2*(q_map > self.thresh) - 1
        score = np.mean(weight_map*ctrb_map)
        return score


if __name__ == '__main__':
    CQ_ind = ComparisonIQA()
    img1 = mpimg.imread('plane1.png')*255
    img2 = mpimg.imread('plane2.png')*255
    score = CQ_ind.c_iqa(img1, img2)
    print('The quality of image1 based image2 is {}').format(score)
