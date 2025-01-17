import torch
import numpy as np
import pathlib
import attr
from collections.abc import Iterable
import argparse
import pickle
from warnings import warn

def load_tensor(file, device=None):
    t = torch.load(file)
    if device is not None:
        t = t.to(device)
    return t

  
def to_dict_with_sorted_values(d, key=None):
    return {k: sorted(v, key=key) for k, v in d.items()}


def to_dict_with_set_values(d):
    result = {}
    for k, v in d.items():
        hashable_v = []
        for v_elem in v:
            if isinstance(v_elem, list):
                hashable_v.append(tuple(v_elem))
            else:
                hashable_v.append(v_elem)
        result[k] = set(hashable_v)
    return result

def save_tensor(tensor, file):
    pathlib.Path(file).parent.mkdir(parents=True, exist_ok=True)
    torch.save(tensor, file)


def toJSON(obj):
    ''' 
    Calls this instance in case of serialization failure.
    Assumes the object is attr 
    '''
    if attr.has(obj):
        return attr.asdict(obj)
    elif isinstance(obj, np.int64):
        return int(obj)
    else:
        raise NotImplementedError(
            "serialization obj not attr but {}".format(type(obj)))


def tuplify(dictionary):
    if dictionary is None:
        return tuple()
    assert isinstance(dictionary, dict)
    def value(x): return dictionary[x]
    return tuple(key for key in sorted(dictionary, key=value))


def dictify(iterable):
    assert isinstance(iterable, Iterable)
    return {v: i for i, v in enumerate(iterable)}

def dash_separated_ints(value):
    vals = value.split("-")
    for val in vals:
        try:
            int(val)
        except ValueError:
            raise argparse.ArgumentTypeError(
                "%s is not a valid dash separated list of ints" % value
            )

    return value


def dash_separated_floats(value):
    vals = value.split("-")
    for val in vals:
        try:
            float(val)
        except ValueError:
            raise argparse.ArgumentTypeError(
                "%s is not a valid dash separated list of floats" % value
            )

    return value


# TODO: Take care of serialization for specific objects
def serialize_object(obj):
    if isinstance(obj, str) or isinstance(obj, bytes):
        return obj
    else:
        warn(f"Pickle is being used to serialize object of type: {type(obj)}")
        return pickle.dumps(obj)
