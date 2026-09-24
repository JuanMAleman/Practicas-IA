from numbers import Number
from typing import Union
import numpy as np
import logging
import re


UNITS = {3: "ms", 6: "us", 9: "ns", 12: "ps"}


def find_property(d: dict, key: str) -> Union[np.float64, Number]:
    for k, v in d.items():
        if k == key:
            return d[k]

        if isinstance(v, dict):
            try:
                length = find_property(v, key)
                return length
            except ValueError:
                pass

    raise ValueError("Length not found")


def format_time(start_time: float, end_time: float) -> str:
    if end_time == -1 or start_time == -1:
        logging.warning("_is_timeout: no se realizó llamada a _start_timer o _end_timer")
        return "-1"

    t = end_time - start_time
    t /= 10e8
    if t > 1:
        return f"{t:.4f} s"

    zeros = len(re.findall("^0+", f"{t:.12f}".replace(".", ""))[0])
    while zeros < 13:
        if zeros in UNITS:
            return f"{t * 10 ** zeros:.4f} {UNITS[zeros]}"
        zeros += 1

    logging.warning("_is_timeout: el tiempo de ejecución termino en menos de 1 pico segundo")
    return f"{t:.12f} s"
