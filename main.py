import numpy as np
import png
import numpy


def load_image(file: str):
    r = png.Reader(filename=file)
    cols, rows, pixels, meta = r.asDirect()

    img_2d = numpy.vstack(map(numpy.uint8, pixels))
    img_3d = numpy.reshape(img_2d, (rows, cols, 4))

    return cols, rows, img_3d, meta


def generate_background(pattern, pal: tuple, image_3d):
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


def replace_background(img, bg):
    for i in range(row_count):
        for j in range(col_count):
            a = img[i][j][3]
            out = [i for _ in range(4)]
            out[0] = ((255 - a)/255 * bg[i][j][0]) + (a/255 * img[i][j][0])
            out[1] = ((255 - a)/255 * bg[i][j][1]) + (a/255 * img[i][j][1])
            out[2] = ((255 - a)/255 * bg[i][j][2]) + (a/255 * img[i][j][2])
            out[3] = 255
            img[i][j] = out


if __name__ == '__main__':
    col_count, row_count, image_3d, metadata = load_image('./in/smoke.png')
    bg_dots = [[1, 0], [0, 0]]              # 0 bg; 1 fg
    bg_lines = [[1, 0, 0], [1, 0, 1], [0, 0, 1]]
    bg_check = [[1, 0], [0, 1]]
    palette = ([66, 12, 8, 255], [145, 45, 25, 255])  # bg; fg

    background = generate_background(bg_check, palette, image_3d)

    replace_background(image_3d, background)

    image_2d = numpy.reshape(image_3d, (-1, col_count * 4))
    print(image_2d[0][0:8])
    f = open('./out/out1.png', 'wb')
    w = png.Writer(col_count, row_count, greyscale=False, bitdepth=8, alpha=True)
    w.write(f, image_2d)
    f.close()
