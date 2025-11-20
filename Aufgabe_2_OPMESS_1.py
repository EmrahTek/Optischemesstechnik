import numpy as np

def roud_measurement(mean,error):
    first_digit_pos = int(np.floor(np.log10(abs(error))))
    first_digit_int = int(np.int(np.log10))