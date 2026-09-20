from numbers import Number
from typing import Union
import numpy as np


def find_property(d: dict, key: str = "length") -> Union[np.float64, Number]:
    for k, v in d.items():
        if k == key:
            return d[k]

        if isinstance(v, dict):
            try:
                length = find_property(v)
                return length
            except ValueError:
                pass

    raise ValueError("Length not found")
