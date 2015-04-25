# pymkcmd | dale@pbdr.info | http://pbdr.info
# Testing functions.


def concat_strings(str0: 'String One.', str1: 'String Two.',
                   sep: 'The seperator to concatenate the strings.'=' '):

    '''Concatenate two strings with a seperator.'''

    return sep.join([str0, str1])


def add_numbers(int0: int, float0: float=0.0):

    '''A test function adding two numbers.'''

    return int0 + float0


def mult_numbers(int0: (int, 'The integer.'),
                 float0: float=1.0):

    '''A test function multiplying two numbers.'''

    return int0 * float0


def sub_numbers(int0, float0: 'The float.'=0.0):

    '''A test function subtracting two numbers.'''

    return int0 - float0
