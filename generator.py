from random import randint

from PIL import Image
from PIL import ImageDraw


def open_cells(CELLSDIR, filenames, size):
    vars_of_ceil = []
    for ind, el in enumerate(filenames):
        img = Image.open(f'{CELLSDIR}/{el}')
        img = img.convert("RGB")
        img = img.resize((size, size))
        pix = img.load()
        vars_of_ceil.append(pix)
    return vars_of_ceil


def generate_map(m, n, size_ceil, vars_of_ceil, chosen_var):
    # n - height
    # m - weight
    SZLINE = 4
    img = Image.new('RGB', (n * size_ceil + (n + 1) * SZLINE,
                            m * size_ceil + (m + 1) * SZLINE))  # widgth,height
    width = img.size[0]
    height = img.size[1]
    # print(width)
    # print(height)
    draw = ImageDraw.Draw(img)
    for i in range(n):
        for j in range(m):
            now_ceil = chosen_var[i][j]
            add_x = SZLINE * (i + 1)
            add_y = SZLINE * (j + 1)
            for x in range(size_ceil * i, size_ceil * (i + 1)):
                for y in range(size_ceil * j, size_ceil * (j + 1)):
                    x_f = x - size_ceil * i
                    y_f = y - size_ceil * j
                    draw.point((x + add_x, y + add_y), vars_of_ceil[now_ceil][x_f, y_f])
    return img


if __name__ == "__main__":
    n = 20
    m = 20
    chosen_var = [[randint(0, 3) for _ in range(m)] for j in range(n)]
    img = generate_map(n, m, 200, open_cells('ceils'), chosen_var)
    img.save('compose.png')
