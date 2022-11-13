from bggenerator.bg_generator import BGGen

if __name__ == '__main__':


    bg_gen = BGGen('media/uploads/junko2022.png')
    background = bg_gen.replace_background(bg_dots_huge)



    image_2d = numpy.reshape(image_3d, (-1, col_count * 4))
    print(image_2d[0][0:8])
    f = open('./out/out1.png', 'wb')
    w = png.Writer(col_count, row_count, greyscale=False, bitdepth=8, alpha=True)
    w.write(f, image_2d)
    f.close()
