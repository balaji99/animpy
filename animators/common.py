import numpy as np

# Function to generate 'n' random points
def random_points(width, height, n = 1):
    x_points = np.random.uniform(0, width, n)
    y_points = np.random.uniform(0, height, n)
    return np.column_stack((x_points, y_points))


def random_rgb_color():
    red = np.random.randint(0, 255)
    green = np.random.randint(0, 255)
    blue = np.random.randint(0, 255)
    return [red, green, blue]