# pymkcmd | dale@pbdr.info | http://pbdr.info
# CLI: concat_strings

from pymkcmd import mkcmd


def concat_strings(str0: 'String One.',
                   str1: 'String Two.',
                   sep: 'The seperator to concatenate the strings.'=' '):
    '''Concatenate two strings with a seperator.'''
    return sep.join([str0, str1])

if __name__ == '__main__':
    mkcmd(concat_strings)()
