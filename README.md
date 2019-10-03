# PyRhyme

Reading and manipulating Rhyme outputs.


## Installation

Using `setyp.py`:

```bash
$ git clone https://gitlab.com/rhyme-org/py-rhyme.git
$ cd py-rhyme
$ python3 setup.py install # --user in case you want to install it locally
```

Using `pip`:

```bash
$ git clone https://gitlab.com/rhyme-org/py-rhyme.git
$ cd py-rhyme
$ pip install . # --user in case you want to install it locally
$ pip3 install . # --user in case you want to install it locally
```

To install the package locally in editable mode, run:

```bash
$ pip install -e . --user
$ pip3 install -e . --user
```


## Usage

```
    >>> from py_rhyme import PyRhyme
    >>> rhyme = PyRhyme('/path/to/rhyme/output')
```


## Running tests

To make sure that the CHOMBO test file is updated, run

```bash
$ python3 setup.py chombo
```

This command will create a CHOMBO test file inside `py-rhyme/tests/assets`.

To run the tests, execute the following command:

```bash
$ python3 ./setup.py test
```

or

```bash
$ py.test # -s to show stdout
```
