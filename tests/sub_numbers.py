# pymkcmd | dale@pbdr.info | http://pbdr.info
# CLI: sub_numbers

from pymkcmd import mkcmd, mkant
from test_funcs import sub_numbers

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
            },
            desc='This description is added by `pymkcmd.mkant`.'
        ),
    )()
