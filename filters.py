""" The different types of matrices used for different image filters. """
from collections import namedtuple

Filter = namedtuple('SharpenFilter', ['name', 'factor', 'bias', 'filter'])


filter_blur = Filter('blur', 1.0 / 13.0, 0.0, [
      [0, 0, 1, 0, 0],
      [0, 1, 1, 1, 0],
      [1, 1, 1, 1, 1],
      [0, 1, 1, 1, 0],
      [0, 0, 1, 0, 0]
])


filter_sharpen = Filter('sharpen', 1.0, 0.0, [
    [1,  1,  1],
    [1, -7,  1],
    [1,  1,  1]
])
