# pymkcmd | dale@pbdr.info | http://pbdr.info
# CLI: concat_strings, add_numbers, mult_numbers

from pymkcmd import mkcmds
from concat_strings import concat_strings
from add_numbers import add_numbers

if __name__ == '__main__':
    mkcmds([concat_strings, add_numbers],
           description='The CLI for multiple Python functions.')()
