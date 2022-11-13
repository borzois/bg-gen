import os

import numpy as np
import png
import numpy
from colorthief import ColorThief


class BGGen:
    def __init__(self, filename: str):
        self.patterns = {
            'bg_solid': [[0, 0], [0, 0]],
            'bg_dots': [[1, 0], [0, 0]],
            'bg_lines': [[1, 0, 0], [1, 0, 1], [0, 0, 1]],
            'bg_check': [[1, 0], [0, 1]],
            'bg_dots_big': [[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            'bg_dots_huge': [
                [1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
            ]
        }
        self.filename = os.path.join(filename)
        self.cols, self.rows, self.image_3d, self.meta = self.load_image()

    def load_image(self):
        r = png.Reader(filename=os.path.join('../media/uploads/', self.filename))
        cols, rows, pixels, meta = r.asDirect()

        img_2d = numpy.vstack(map(numpy.uint8, pixels))
        img_3d = numpy.reshape(img_2d, (rows, cols, 4))

        return cols, rows, img_3d, meta

    def get_colors(self):
        ct = ColorThief(os.path.join('../media/uploads/', self.filename))
        ct_pal = ct.get_palette(color_count=2)

        color1 = list(ct_pal[0]) + [255]
        color2 = list(ct_pal[1]) + [255]

        return color1, color2

    def generate_background(self, pattern):
        bg = np.full_like(self.image_3d, 0)
        image_size = numpy.shape(self.image_3d)
        pattern_size = len(pattern)
        color_palette = self.get_colors()
        for i in range(image_size[0]):
            for j in range(image_size[1]):
                if pattern[i % pattern_size][j % pattern_size] == 0:
                    bg[i][j] = color_palette[0]
                else:
                    bg[i][j] = color_palette[1]

        return bg

    def replace_background(self, pattern):
        bg = self.generate_background(self.patterns[pattern])

        for i in range(self.rows):
            for j in range(self.cols):
                a = self.image_3d[i][j][3]
                out = [i for _ in range(4)]
                out[0] = ((255 - a) / 255 * bg[i][j][0]) + (a / 255 * self.image_3d[i][j][0])
                out[1] = ((255 - a) / 255 * bg[i][j][1]) + (a / 255 * self.image_3d[i][j][1])
                out[2] = ((255 - a) / 255 * bg[i][j][2]) + (a / 255 * self.image_3d[i][j][2])
                out[3] = 255
                self.image_3d[i][j] = out

    def export(self):
        image_2d = numpy.reshape(self.image_3d, (-1, self.cols * 4))
        print(image_2d[0][0:8])
        f = open(os.path.join('../media/output/', self.filename), 'wb')
        w = png.Writer(self.cols, self.rows, greyscale=False, bitdepth=8, alpha=True)
        w.write(f, image_2d)
        f.close()

