# pymkcmd | dale@pbdr.info | http://pbdr.info
# CLI: mult_numbers

from pymkcmd import mkcmd


def mult_numbers(int0: (int, 'The integer.'),
                 float0: (float, 'The float.')=1.0):
    '''Multiply two numbers.'''
    return int0 * float0

if __name__ == '__main__':
    mkcmd(mult_numbers)()
