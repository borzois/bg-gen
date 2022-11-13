import numpy as np
import png
import numpy
from colorthief import ColorThief


class BGGen:
    def __init__(self, filename: str):
        self.filename = filename
        self.cols, self.rows, self.image_3d, self.meta = self.load_image(self.filename)
        self.color_palette = self.get_colors(self.filename)
        self.background = self.generate_background()

    def load_image(self, file: str):
        r = png.Reader(filename=file)
        cols, rows, pixels, meta = r.asDirect()

        img_2d = numpy.vstack(map(numpy.uint8, pixels))
        img_3d = numpy.reshape(img_2d, (rows, cols, 4))

        return cols, rows, img_3d, meta

    def get_colors(self, file: str):
        ct = ColorThief(file)
        ct_pal = ct.get_palette(color_count=2)

        color1 = list(ct_pal[0]) + [255]
        color2 = list(ct_pal[1]) + [255]

        return color1, color2

    def generate_background(self, pattern, pal: tuple, image_3d):
        bg = np.full_like(image_3d, 0)
        image_size = numpy.shape(image_3d)
        pattern_size = len(pattern)
        for i in range(image_size[0]):
            for j in range(image_size[1]):
                if pattern[i % pattern_size][j % pattern_size] == 0:
                    bg[i][j] = pal[0]
                else:
                    bg[i][j] = pal[1]

        return bg

    def replace_background(self, img, bg):
        for i in range(row_count):
            for j in range(col_count):
                a = img[i][j][3]
                out = [i for _ in range(4)]
                out[0] = ((255 - a) / 255 * bg[i][j][0]) + (a / 255 * img[i][j][0])
                out[1] = ((255 - a) / 255 * bg[i][j][1]) + (a / 255 * img[i][j][1])
                out[2] = ((255 - a) / 255 * bg[i][j][2]) + (a / 255 * img[i][j][2])
                out[3] = 255
                img[i][j] = out