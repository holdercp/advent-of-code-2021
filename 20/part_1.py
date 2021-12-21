algo = ''
img = {}
with open('20/input.txt') as f:
    algo, img_raw = f.read().strip().split('\n\n')
    img_list = img_raw.splitlines()
    for y, row in enumerate(img_list):
        for x, pixel in enumerate(row):
            img[(x, y)] = pixel


def get_pixels(pixel, img):
    x, y = pixel
    pixels = {}

    for py in range(y-1, y+2):
        for px in range(x-1, x+2):
            p_loc = (px, py)
            pixels[p_loc] = img[p_loc] if p_loc in img else pad

    return pixels


def get_bin_num(pixels):
    sorted_pixels = sorted(pixels.items(), key=lambda p: p[0][1])
    bin_str = ''.join('1' if p[1] == '#' else '0' for p in sorted_pixels)
    return int(bin_str, 2)


def pad_img(img, pad):
    pixels = img.keys()
    x_min = min(pixels)[0] - 1
    x_max = max(pixels)[0] + 1
    y_min = min(pixels, key=lambda p: p[1])[1] - 1
    y_max = max(pixels, key=lambda p: p[1])[1] + 1

    for y in range(y_min, y_max+1):
        img[(x_min, y)] = pad
        img[(x_max, y)] = pad
    for x in range(x_min, x_max+1):
        img[(x, y_min)] = pad
        img[(x, y_max)] = pad

    return img


def process_img(img):
    output = {}
    for pixel in img.keys():
        pixels = get_pixels(pixel, img)
        bin_num = get_bin_num(pixels)
        output_pixel = algo[bin_num]
        output[pixel] = output_pixel
    return output


pad = '.'
processed_img = pad_img(img, pad)
for i in range(2):
    processed_img = process_img(processed_img)

    if algo[0] == '#':
        pad = algo[0] if i % 2 == 0 else algo[511]

    processed_img = pad_img(processed_img, pad)


print(len([p for p in processed_img.values() if p == '#']))
