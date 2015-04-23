# pymkcmd | dale@pbdr.info | http://pbdr.info
# CLI: concat_strings, add_numbers, mult_numbers

from pymkcmd import mkcmds
from test_funcs import *

if __name__ == '__main__':
    mkcmds([concat_strings, add_numbers, mult_numbers],
           description='The CLI for a few Python functions.')()
