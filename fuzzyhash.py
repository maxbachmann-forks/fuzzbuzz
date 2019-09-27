from collections import Counter
from pyblake2 import blake2b


HASH_SIZE = 64


def ngram(string, n=2):
    return [string[i:i+n] for i in range(len(string)-n+1)]


def hash(string):
    return int.from_bytes(blake2b(string.encode('utf-8'), 8).digest(), 'big')


def features(string):
    tokens = ['$' + token + '$' for token in string.split()]
    out = Counter()
    for token in tokens:
        for gram in ngram(token):
            out[hash(gram)] += 1
    return out


def int2bits(integer):
    return list(bin(integer)[2:].zfill(HASH_SIZE))


def hamming2(s1, s2):
    """Calculate the Hamming distance between two bit strings"""
    s1 = int2bits(s1)
    s2 = int2bits(s2)
    # Taken from https://stackoverflow.com/a/31007358/140837
    assert len(s1) == len(s2)
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))


distance = hamming2


def simhash(string):
    input = features(string)
    intermediate = [0] * HASH_SIZE
    for feature, count in input.items():
        for index, bit in enumerate(int2bits(feature)):
            intermediate[index] += count if bit == '1' else -count
    # compute simhash
    simhash = ''.join(['1' if v > 0 else '0' for v in intermediate])
    simhash = int(simhash, 2)
    return simhash


fuzzyhash = simhash