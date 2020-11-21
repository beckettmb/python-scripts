#!/usr/bin/python


import re
import sys
from functools import reduce
from collections import Counter


def get_factors(n):
    return set(reduce(
        list.__add__,
        ([i, n / i] for i in xrange(1, int(n ** 0.5) + 1) if n % i == 0)
        ))


def get_chi(text):
    letter_frequencies = {
            'A': 8.55, 'B': 1.60, 'C': 3.16, 'D': 3.87, 'E': 12.20, 'F': 2.18,
            'G': 2.09, 'H': 4.96, 'I': 7.33, 'J': 0.22, 'K': 0.81, 'L': 4.21,
            'M': 2.53, 'N': 7.17, 'O': 7.47, 'P': 2.07, 'Q': 0.10, 'R': 6.33,
            'S': 6.73, 'T': 8.94, 'U': 2.68, 'V': 1.06, 'W': 1.83, 'X': 0.19,
            'Y': 1.72, 'Z': 0.11
            }
    chi = 0
    for letter, frequency in letter_frequencies.iteritems():
        x = len(text) * (frequency / 100)
        chi += ((text.count(letter) - x) ** 2) / x
    return chi


def brute(ciphertext, keys=[]):
    if not keys:
        for i in xrange(26):
            keys.append([i])
    best_chi = 0
    best_key = 0
    for key in keys:
        plaintext = decipher(ciphertext, key)
        chi = get_chi(plaintext)
        if best_chi == 0 or chi < best_chi:
            best_chi = chi
            best_key = key
    return best_key


def decipher(ciphertext, key):
    plaintext = ""
    cipher_ascii = [ord(c) for c in ciphertext]
    i = 0
    for c in cipher_ascii:
        if c >= ord('a') and c <= ord('z'):
            c -= key[i % len(key)]
            i += 1
            if c < ord('a'):
                c += 26
        if c >= ord('A') and c <= ord('Z'):
            c -= key[i % len(key)]
            i += 1
            if c < ord('A'):
                c += 26
        plaintext += chr(c)
    return plaintext


def get_keylengths(ciphertext):
    distances = set()
    for n in xrange(3, 9):
        substr_counter = Counter(
                ciphertext[i: i + n] for i in xrange(len(ciphertext) - n)
                )
        common = substr_counter.most_common(3)
        for c in common:
            if c[1] == 1:
                continue
            occurances = [m.start() for m in re.finditer(c[0], ciphertext)]
            for i in xrange(len(occurances) - 1):
                distances.add(abs(occurances[i] - occurances[i + 1]))
    f = []
    for distance in distances:
        f.append(get_factors(distance))
    keylengths = set.intersection(*f)
    return keylengths


def get_keys(ciphertext):
    keylengths = get_keylengths(ciphertext)
    keys = []
    for keylength in keylengths:
        key = []
        substrings = [''] * keylength
        for i, c in enumerate(ciphertext):
            substrings[i % keylength] += c
        for substring in substrings:
            key.append(brute(substring)[0])
        keys.append(key)
    return keys


ciphertext = ''
original_ciphertext = ''
with open(sys.argv[1], 'r') as f:
    for line in f:
        ciphertext += line.rstrip().replace(' ', '').upper()
        original_ciphertext += line
regex = re.compile('[^A-Za-z]')
ciphertext = regex.sub('', ciphertext)

keys = get_keys(ciphertext)
key = brute(ciphertext, keys)
print decipher(original_ciphertext, key)
