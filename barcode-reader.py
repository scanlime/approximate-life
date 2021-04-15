#!/usr/bin/env python3

# pip3 install ffmpeg-python
import ffmpeg

class BarcodeReader:
    def __init__(self, args):
        self.filename = args.filename
        self.bits = args.B
        self.top = args.t
        self.bottom = args.b
        self.threshold = args.T

    def read(self):
        subproc = (ffmpeg
            .input(self.filename)
            .filter('crop', y=self.top, h=self.bottom-self.top)
            .filter('scale', self.bits, 1)
            .output('pipe:', format='rawvideo', pix_fmt='gray')
            .run_async(pipe_stdout=True))
        prev = None
        count = 0
        while True:
            frame = subproc.stdout.read(self.bits)
            if not frame:
                break
            bits = ''.join(hex(sum((frame[i+j*4] >= self.threshold) << (3-i)
                for i in range(4)))[-1] for j in range(self.bits//4))
            if bits != prev:
                print(count, bits)
                prev = bits
            count += 1

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', metavar='FILE', type=str)
    parser.add_argument('-B', metavar='BITS', type=int, default=960)
    parser.add_argument('-T', metavar='LEVEL', type=int, default=100)
    parser.add_argument('-t', metavar='Y', type=int, default=1320)
    parser.add_argument('-b', metavar='Y', type=int, default=1367)
    BarcodeReader(parser.parse_args()).read()
