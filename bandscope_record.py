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
import pcap
import struct
import sys

CHUNK_SIZE = 512
NUM_CHUNKS = 32
FFT_LEN = CHUNK_SIZE * NUM_CHUNKS
AVG = 436

def parse_chunk(x):
    seq = struct.unpack('>I', x[0x2e:0x32])[0]
    samples = np.frombuffer(x, offset = 0x32, count = 512, dtype = 'int16')
    return seq, samples

def chunks(cap):
    m = map(lambda x: parse_chunk(x[1]), cap)
    next(x for x in m if x[0] % NUM_CHUNKS == NUM_CHUNKS-1)[1] # skip first chunks until stream becomes aligned
    while True:
        yield np.concatenate([next(m)[1] for _ in range(NUM_CHUNKS)])
        
def save_averages_db(chunks, out_file, avg = AVG):
    w = np.hamming(FFT_LEN)
    while True:
        try:
            f = np.zeros(FFT_LEN//2 + 1)
            for _ in range(avg):
                f += np.abs(np.fft.rfft(w*next(chunks)))**2
            f = 10*np.log10(f/avg)
            f.tofile(out_file)
        except KeyboardInterrupt:
            return

def usage():
    print('Usage: {} interface file'.format(sys.argv[0]))
    print('')
    print('Listen on "interface", saving bandscope data to "file"')
    print('')
        
def main():
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)

    with open(sys.argv[2], 'wb') as f:
        p = pcap.pcap(sys.argv[1])
        p.setfilter('udp[8] = 0xef && udp[9] = 0xfe && udp[10] = 0x01 && udp[11] = 0x04')
        cs = chunks(p)
        print('Capturing bandscope data')
        print('Press Control+C to end')
        save_averages_db(cs, f)

if __name__ == '__main__':
    main()
