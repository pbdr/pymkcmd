# pymkcmd | dale@pbdr.info | http://pbdr.info
# CLI: and3

from pymkcmd import mkcmd


def and3(bool0: bool, bool1: bool, bool2: bool):
    '''AND logic for three boolean values.'''
    return bool0 and bool1 and bool2

if __name__ == '__main__':

    # Try `parse_bool=False` and run `python3 add3.py False False False`
    # to see the difference.
    mkcmd(and3, parse_bool=True)()
