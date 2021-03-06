# pymkcmd | dale@pbdr.info | http://pbdr.info
# The main logic of pymkcmd.

import sys
import inspect
import argparse
import logging
from functools import wraps


def mkcmd(func, doc_format='plain', ant_format='auto', parse_bool=True):

    '''
    Generate a CLI (command line interface) for a function.

    :param func: The function to generate the CLI for.
    :param doc_format: See ``mk_cmd_parser``.
    :param ant_format: See ``mk_cmd_parser``.
    :param parse_bool: See ``mk_cmd_arg``.
    :returns: The generated CLI.
    '''

    parser = mk_cmd_parser(func, doc_format, ant_format, parse_bool)

    # The generated CLI.
    def func_cmd(argv=sys.argv[1:]):

        cmd_args = parser.parse_args(argv)

        logging.debug(cmd_args)

        # Obtain function arguments.
        args, kwargs = mk_func_args(func, cmd_args)

        ret = func(*args, **kwargs)
        sys.stdout.write(str(ret) + '\n')

    return func_cmd


def mkcmds(funcs, description='',
           doc_format='plain', ant_format='auto', parse_bool=True):

    '''
    Generate a CLI for multiple functions.

    :param funcs: The functions to generate the CLI for. Can be any
                  enumerable of functions.
    :param description: The description for the CLI.
    :param doc_format: See ``mk_cmd_parser``.
    :param ant_format: See ``mk_cmd_parser``.
    :param parse_bool: See ``mk_cmd_arg``.
    :returns: The generated CLI.
    '''

    # The top-level parser with subparsers for individual functions.
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers()

    for func in funcs:

        func_parser = subparsers.add_parser(
            func.__name__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
        mk_cmd_parser(func, doc_format, ant_format, parse_bool,
                      parser=func_parser)
        # Associate the function with its corresponding subparser.
        func_parser.set_defaults(func=func)

    # The generated CLI.
    def funcs_cmd(argv=sys.argv[1:]):

        # Help message will be displayed if no argument is supplied.
        cmd_args = parser.parse_args(argv if len(argv) > 0 else ['-h'])

        logging.debug(cmd_args)

        # Obtain the function to call and its arguments.
        func = cmd_args.func
        args, kwargs = mk_func_args(func, cmd_args)

        ret = func(*args, **kwargs)
        sys.stdout.write(str(ret) + '\n')

    return funcs_cmd


def mk_cmd_parser(func, doc_format, ant_format, parse_bool,
                  parser=None):

    '''
    Generate a CLI argument parser for a function.

    :param func: The function to generate the parser for.

    :param doc_format:
        How to interpret the docstring of the function.

        - 'plain': As a string used for the CLI description.
        - 'ignore': Ignore.

    :param ant_format:
        How to interpret the parameter annotations:

        - 'auto': Determine automatically.
        - 'str': Convert to a string documenting the parameter.
        - 'ignore': Ignore.

    :param parse_bool: See ``mk_cmd_arg``.

    :param parser:
        If a parser is supplied, new arguments will be appended to it.
        Otherwise, a new parser will be created and returned.

    :returns: The generated CLI argument parser.
    '''

    # Make a CLI argument parser if none is supplied.
    if parser is None:
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter)

    # ==== CLI description. ====

    func_desc = getattr(func, 'desc', inspect.getdoc(func))

    if doc_format == 'plain':
        cmd_desc = func_desc
    elif doc_format == 'ignore':
        cmd_desc = ''
    else:
        raise ValueError('Invalid `doc_format` value.')

    parser.description = cmd_desc

    # ==== CLI arguments. ====

    param_types = getattr(func, 'param_types', {})
    param_helps = getattr(func, 'param_helps', {})
    sig = inspect.signature(func)

    # Make a CLI argument for each function parameter.
    for param in sig.parameters.values():

        param_name = param.name
        param_type = param_types.get(param_name)
        param_help = param_helps.get(param_name)
        cmd_arg = \
            mk_cmd_arg(param, ant_format,
                       param_type, param_help, parse_bool)
        parser.add_argument(cmd_arg[0], **cmd_arg[1])

    return parser


def mk_cmd_arg(param, ant_format, param_type, param_help, parse_bool):

    '''
    Make a CLI argument for a function parameter.

    :param param: The function parameter to make the CLI argument for.
    :param ant_format: See ``mk_cmd_parser``.
    :param param_type: The parameter type.
    :param param_help: The parameter help message.
    :param parse_bool: If ``true``, only the string ``"True"`` will be
                       parsed as Python boolean `True`. Otherwise use
                       Python boolean type conversion.
    :returns: The name and the options used to create the CLI argument.
    '''

    # ==== CLI argument name. ====

    param_name = param.name

    # Make a positional CLI argument.
    if param.default == inspect.Signature.empty:
        cmd_arg_name = param_name
        cmd_default_val = None
    # Make a keyword CLI argument with a default value.
    else:
        cmd_arg_name = '--{}'.format(param_name)
        cmd_default_val = param.default

    # ==== CLI argument type and help. ====

    annotation = param.annotation

    # Automatically determine the annotation format.
    if ant_format == 'auto':

        # If the annotation is a non-empty type.
        if type(annotation) == type and \
                annotation != inspect.Signature.empty:

            cmd_type = annotation
            cmd_help = str(annotation)

        # If the annotation is a pair of non-empty type
        # and a string.
        elif type(annotation) == tuple and \
                len(annotation) == 2 and \
                type(annotation[0]) == type and \
                annotation[0] != inspect.Signature.empty:

            cmd_type = annotation[0]
            cmd_help = '{} {}'.format(*annotation)

        else:

            cmd_type = str
            cmd_help = str(annotation)

    # Use the annotation as a string for documentation.
    elif ant_format == 'str':

        cmd_type = str
        cmd_help = str(annotation)

    # Ignore the annotation.
    elif ant_format == 'ignore':

        cmd_type = str
        cmd_help = ''

    else:
        raise ValueError('Invalid `ant_format` value.')

    if param_type is not None:
        cmd_type = param_type

    # If `parse_bool` is enabled, replace `bool` with a
    # boolean string parser that only recognizes `"True"`
    # as `True`.
    if parse_bool and cmd_type == bool:
        cmd_type = lambda s: s == 'True'

    if param_help is not None:
        cmd_help = param_help

    # ==== CLI argument action. ====

    cmd_action = 'store'

    return (
        cmd_arg_name,
        {
            'default': cmd_default_val,
            'type': cmd_type,
            'help': cmd_help,
            'action': cmd_action
        })


def mk_func_args(func, cmd_args):

    '''
    Convert CLI arguments back to the arguments for a function.

    :param func: The function to convert the CLI arguments for.
    :param cmd_args: The CLI arguments to be converted.
    :returns: The function arguments.
    '''

    args = []
    kwargs = {}

    sig = inspect.signature(func)

    for param in sig.parameters.values():

        param_name = param.name
        cmd_arg_val = cmd_args.__dict__[param_name]

        # Add an positional argument.
        if param.default == inspect.Signature.empty:
            args.append(cmd_arg_val)
        # Add a keyword argument.
        else:
            kwargs[param_name] = cmd_arg_val

    return (args, kwargs)


def mkant(func, param_types=None, param_helps=None, desc=None):

    '''
    Make an annotated copy of a function. Annotations are added
    as members of the function object.

    :param func: The function to be annotated.
    :param param_types: A dictionary of parameter data types.
    :param param_helps: A dictionary of parameter help messages.
    :param desc: A description of the function.
    :returns: An annotated copy of the function.
    '''

    @wraps(func)
    def ant_func(*args, **kwargs):
        return func(*args, **kwargs)

    ant_func.param_types = param_types
    ant_func.param_helps = param_helps
    ant_func.desc = desc

    return ant_func
