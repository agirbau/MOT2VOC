import numpy as np
np.random.seed(123)
import os
import time


def check_and_create(path_to_check):
    os.makedirs(path_to_check, exist_ok=True)


def concat_root_path(root_path, basename_list):
    return [os.path.join(root_path, basename) for basename in basename_list]


class Timer:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.start = time.time()
        print('{}...'.format(self.name))
        return self

    def __exit__(self, *args):
        self.end = time.time()
        print('{}: {:.6f}s'.format(self.name, self.end - self.start))


class ColorGenerator:
    def __init__(self):
        self.colors = None
        self.generate_colors()

    def generate_colors(self, colors_used=[]):
        c_r = np.linspace(1, 255, num=10, endpoint=True)
        c_g = np.linspace(1, 255, num=10, endpoint=True)
        c_b = np.linspace(1, 255, num=10, endpoint=True)

        colors = np.asarray(np.meshgrid(c_r, c_g, c_b)).reshape(3, -1).T
        # colors = np.mgrid[0:255:50, 0:255:50, 0:255:50].reshape(3, -1).T

        # Remove colors used (for existing tracks) --> shouldn't be here
        # colors_used = compare_mat1_vs_mat2(colors_used, colors)
        # colors = np.delete(colors, colors_used, axis=0)
        self.colors = np.random.permutation(colors)
