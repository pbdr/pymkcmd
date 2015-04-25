# pymkcmd | dale@pbdr.info | http://pbdr.info
# CLI: sub_numbers

from pymkcmd import mkcmd, mkant


def sub_numbers(int0, float0=0.0):
    '''Subtract two numbers.'''
    return int0 - float0

if __name__ == '__main__':

    mkcmd(
        mkant(
            sub_numbers,
            param_types={
                'int0': int,
                'float0': float
            },
            param_helps={
                'int0': 'The integer.',
                'float0': 'The float.'
            },
            desc='This description is added by `pymkcmd.mkant`.'
        ),
    )()
