# pymkcmd | dale@pbdr.info | http://pbdr.info
# Functions for testing.


def concat_strings(str0: 'String One.', str1: 'String Two.',
                   sep: 'The seperator to concatenate the strings.'=' ',):

    '''Concatenate two strings with a seperator.'''

    concat_str = sep.join([str0, str1])
    print(concat_str)
    return concat_str


def add_numbers(int0: int, float0: float=0.0):

    '''A test function adding two numbers.'''

    print('add_numbers({}, float0={}) = {}'
          .format(int0, float0, int0 + float0))


def mult_numbers(int0: (int, 'Integer one.'),
                 float0: float=1.0):

    '''A test function multiplying two numbers.'''

    print('mult_numbers({}, float0={}) = {}'
          .format(int0, float0, int0 * float0))
