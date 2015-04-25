# pymkcmd | dale@pbdr.info | http://pbdr.info
# CLI: add_number

from pymkcmd import mkcmd


def add_numbers(int0: int, float0: float=0.0):
    '''Add two numbers.'''
    return int0 + float0

if __name__ == '__main__':
    mkcmd(add_numbers)()
