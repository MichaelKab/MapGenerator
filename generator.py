import os
from random import randint

from PIL import Image
from PIL import ImageDraw


def open_cells(CELLSDIR, size):
    vars_of_ceil = []
    SAVE_CONFIG = os.getenv('SAVE_CONFIG')
    is_use = [True for i in range(100)]
    with open(SAVE_CONFIG, 'r') as file:
        is_use = list(map(int, file.read().split()))
    for ind, el in enumerate(os.listdir(CELLSDIR)):
        if not is_use[ind]:
            continue
        img = Image.open(f'{CELLSDIR}/{el}')
        img = img.convert("RGB")
        img = img.resize((size, size))
        print(img.width, img.height)
        pix = img.load()
        vars_of_ceil.append(pix)
    return vars_of_ceil


def generate_map(n, m, size_ceil, vars_of_ceil):
    # n - height
    # m - weight
    SZLINE = 5
    map = [[randint(0, len(vars_of_ceil) - 1) for _ in range(m)] for j in range(n)]
    img = Image.new('RGB', (n * size_ceil + (n + 1) * SZLINE,
                            m * size_ceil + (m + 1) * SZLINE))  # widgth,height
    width = img.size[0]
    height = img.size[1]
    print(width)
    print(height)
    draw = ImageDraw.Draw(img)
    for i in range(n):
        for j in range(m):
            now_ceil = map[i][j]
            add_x = SZLINE * (i + 1)
            add_y = SZLINE * (j + 1)
            for x in range(size_ceil * i, size_ceil * (i + 1)):
                for y in range(size_ceil * j, size_ceil * (j + 1)):
                    x_f = x - size_ceil * i
                    y_f = y - size_ceil * j
                    draw.point((x + add_x, y + add_y), vars_of_ceil[now_ceil][x_f, y_f])
    return img


if __name__ == "__main__":
    img = generate_map(20, 20, 200, open_cells('ceils'))
    img.save('compose.png')

# generate_map(5, 5, 30, [0])
# img = Image.new('RGB', (100, 100), color='red')
# img.save('ceils/ceil_2.png')
