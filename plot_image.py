#!/usr/bin/env python3
#
# Copyright 2018 Daniel Estevez <daniel@destevez.net>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

import numpy as np
import matplotlib.pyplot as plt
import sys

CHUNK_SIZE = 512
NUM_CHUNKS = 32
FFT_LEN = CHUNK_SIZE * NUM_CHUNKS

def save_image(in_path, out_path):
    im = np.fromfile(in_path)
    im = im[:im.size//(FFT_LEN//2 + 1)*im.size].reshape(im.size//(FFT_LEN//2 + 1), FFT_LEN//2 + 1)
    plt.imsave(out_path, im, cmap='viridis', vmin=40, vmax=100)

def usage():
    print('Usage: {} input output'.format(sys.argv[0]))
    print('')
    print('Read averaged bandscope data from "input", write image to "output"')
    print('')
        
def main():
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)
    save_image(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()
