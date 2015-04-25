pymkcmd
=======

Make command line interfaces (CLI) for Python functions.

Currently pymkcmd only works with Python 3.

## 1. Installation

An installation scheme is under development. For now just add `src` directory
to one of Python's search paths, e.g. `PYTHONPATH` environment variable.

## 2. Usage

Please refer to `tests/test_funcs.py` for complete definitions of
testing functions.

`tests/test_funcs.py`

```python
def concat_strings(str0: 'String One.', str1: 'String Two.',
                   sep: 'The seperator to concatenate the strings.'=' ',):
    '''Concatenate two strings with a seperator.'''
    ...

def add_numbers(int0: int, float0: float=0.0):
    '''A test function adding two numbers.'''
    ...

def mult_numbers(int0: (int, 'Integer one.'),
                 float0: float=1.0):
    '''A test function multiplying two numbers.'''
    ...
```

### 2.1 CLI for a Single Function

`concat_strings.py`

```python
from pymkcmd import mkcmd
from test_funcs import concat_strings

if __name__ == '__main__':
    mkcmd(concat_strings)()
```

`mkcmd(concat_strings)` actually returns a function which invokes
`concat_strings` with a CLI argument list (`sys.argv[1:]` by default).
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
machine:tests pbdr $ <b>python3 concat_strings.py --sep=', ' hi there</b>
hi, there
</pre>

Each parameter annotation is used as an argument description in this case.
You can also use annotations to specify argument types, as shown below:

<pre>
machine:tests pbdr $ <b>python3 add_numbers.py -h</b>
usage: add_numbers.py [-h] [--float0 FLOAT0] int0

A test function adding two numbers.

positional arguments:
  int0             &lt;class 'int'&gt;

optional arguments:
  -h, --help       show this help message and exit
  --float0 FLOAT0  &lt;class 'float'&gt;
machine:tests pbdr $ <b>python3 add_numbers.py --float0=1.23 4</b>
add_numbers(4, float0=1.23) = 5.23
</pre>

Help messages and types are two typical uses of annotations as described
in [PEP 3107](https://www.python.org/dev/peps/pep-3107/#rationale).
pymkcmd thus supports both simultaneously like this, as seen on argument
`int0`:

<pre>
machine:tests pbdr $ <b>python3 mult_numbers.py -h</b>
usage: mult_numbers.py [-h] [--float0 FLOAT0] int0

A test function multiplying two numbers.

positional arguments:
  int0             &lt;class 'int'&gt; Integer one.

optional arguments:
  -h, --help       show this help message and exit
  --float0 FLOAT0  &lt;class 'float'&gt;
</pre>


### 2.2 CLI for Multiple Functions

Instead of `pymkcmd.mkcmd`, use `pymkcmd.mkcmds` to create an CLI for
multiple functions:

`cli_multiple.py`
```python
from pymkcmd import mkcmds
from test_funcs import *

if __name__ == '__main__':
    mkcmds([concat_strings, add_numbers, mult_numbers],
           description='The CLI for a few Python functions.')()
```

The name of the function to invoke is supplied as the first argument,
followed by its arguments:

<pre>
machine:tests pbdr $ <b>python3 funcs_cmd.py</b>
usage: funcs_cmd.py [-h] {concat_strings,add_numbers,mult_numbers} ...

The CLI for a few Python functions.

positional arguments:
  {concat_strings,add_numbers,mult_numbers}

optional arguments:
  -h, --help            show this help message and exit

machine:tests pbdr $ <b>python3 funcs_cmd.py add_numbers --float0=1.23 4</b>
add_numbers(4, float0=1.23) = 5.23
</pre>

## 3. Implementation

pymkcmd utilizes `inspect` module to gather metadata from functions, and
`argparse` to create corresponding CLI argument parsers.

## 4. TODO

- Write return value to standard output.
- Compatibility for Python 2. (!)
- Add support for parsing docstrings:
  [PEP 287](https://www.python.org/dev/peps/pep-0287/), etc.
- Auto-generated short CLI argument names.
- Add support for types taking multiple arguments.
- Append metadata to functions before creating CLIs.
