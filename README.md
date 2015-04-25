pymkcmd
=======

Make command line interfaces (CLI) for Python functions.

Currently pymkcmd only works with Python 3.

## 1. Installation

An installation scheme is under development. For now just add `src` directory
to one of Python's search paths, e.g. `PYTHONPATH` environment variable.

## 2. Usage

Please refer to `tests` directory for complete test code.

### 2.1 CLI for a Single Function

`concat_strings.py`

```python
from pymkcmd import mkcmd

def concat_strings(str0: 'String One.',
                   str1: 'String Two.',
                   sep: 'The seperator to concatenate the strings.'=' '):
    '''Concatenate two strings with a seperator.'''
    return sep.join([str0, str1])

if __name__ == '__main__':
    mkcmd(concat_strings)()
```

`mkcmd(concat_strings)` actually returns a function which invokes
`concat_strings` with a CLI argument list (`sys.argv[1:]` by default) -
Hence the second pair of parentheses. To use the CLI:

<pre>
machine:tests pbdr $ <b>python3 concat_strings.py -h</b>
usage: concat_strings.py [-h] [--sep SEP] str0 str1

Concatenate two strings with a seperator.

positional arguments:
  str0        String One.
  str1        String Two.

optional arguments:
  -h, --help  show this help message and exit
  --sep SEP   The seperator to concatenate the strings.
machine:tests pbdr $ <b>python3 concat_strings.py hi there</b>
hi there
machine:tests pbdr $ <b>python3 concat_strings.py hi there --sep=', '</b>
hi, there
</pre>

Each parameter annotation can be used as a description as shown above,
or to specify the data type:

<pre>
machine:tests pbdr $ <b>python3 add_numbers.py -h</b>
usage: add_numbers.py [-h] [--float0 FLOAT0] int0

Add two numbers.

positional arguments:
  int0             &lt;class 'int'&gt;

optional arguments:
  -h, --help       show this help message and exit
  --float0 FLOAT0  &lt;class 'float'&gt;
machine:tests pbdr $ <b>python3 add_numbers.py 4 --float0=1.23</b>
5.23
</pre>

Or both:

<pre>
machine:tests pbdr $ <b>python3 mult_numbers.py -h</b>
usage: mult_numbers.py [-h] [--float0 FLOAT0] int0

Multiply two numbers.

positional arguments:
  int0             &lt;class 'int'&gt; The integer.

optional arguments:
  -h, --help       show this help message and exit
  --float0 FLOAT0  &lt;class 'float'&gt; The float.
</pre>


### 2.2 CLI for Multiple Functions

Instead of `pymkcmd.mkcmd`, use `pymkcmd.mkcmds` to create an CLI for
multiple functions:

`funcs_cmd.py`
```python
from pymkcmd import mkcmds
from concat_strings import concat_strings
from add_numbers import add_numbers
from mult_numbers import mult_numbers

if __name__ == '__main__':
    mkcmds([concat_strings, add_numbers, mult_numbers],
           description='The CLI for multiple Python functions.')()
```

The name of the function to invoke is supplied as the first argument,
followed by its arguments:

<pre>
machine:tests pbdr $ <b>python3 funcs_cmd.py add_numbers 4 --float0=1.23</b>
5.23
</pre>

### 2.3 Adding Annotations

To make better CLI help messages for unannotated Python 3 functions or
Python 2 functions, metadata can be added to functions with
`pymkcmd.mkant`:

`sub_numbers.py`
```python
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
```

## 3. Implementation

pymkcmd utilizes `inspect` module to gather metadata from functions, and
`argparse` to create corresponding CLI argument parsers.

## 4. TODO

- Compatibility for Python 2. (!)
- Add support for parsing docstrings:
  [PEP 287](https://www.python.org/dev/peps/pep-0287/), etc.
- Auto-generated short CLI argument names.
- Add support for types taking multiple arguments.
