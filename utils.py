import os


def get_paginated_entries(seq, index, page_size):
    if index + page_size > len(seq):
        return seq[index:]
    return seq[index:index+page_size]


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')