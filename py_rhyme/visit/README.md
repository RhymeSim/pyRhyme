# VisIt Wrapper

## Installation
[Here](https://wci.llnl.gov/simulation/computer-codes/visit/downloads) you can
find instructions to install VisIt on your computer.

## Usage
Before importing this module, make sure that you have VisIt Python package path
in your `PYTHONPATH`, if not, find your VisIt Python package path and add it
to your `PYTHONPATH` as shown in the following,

```shell
$ export PYTHONPATH=/path/to/visit/version/arch/lib/site-packages:$PYTHONPATH
```

You might also need to set other env variables:

```shell
$ export PATH=/path/to/visit/bin:$PATH
$ export C_LIBRARY_PATH=/path/to/visit/version/arch/lib:$C_LIBRARY_PATH
$ export LD_LIBRARY_PATH=/path/to/visit/version/arch/lib:$LD_LIBRARY_PATH
$ export C_INCLUDE_PATH=/path/to/visit/version/arch/include:$C_INCLUDE_PATH
```

**Note** VisIt Python package is only compatible with Python 2.

Import `py_rhyme.visit` and enjoy the power of VisIt,

```python
>>> from py_rhyme.visit import VisItAPI as Vis
>>> v = Vis(interactive=True) # False if you don't wish to open VisIt viewer
>>> v.open('/path/output_000.h5') # For a database use: /path/output_*
>>> v.pseudocolor('rho')
>>> v.slice(origin_type='Percent', val=50, axis_type='ZAxis')
>>> v.draw()
>>> v.cycle(17)
>>> v.change_scaling('linear')
>>> v.change_variable('rho_u')
>>> v.draw()
>>> v.close()
```

To use the full power of VisIt, you also might want to import VisIt python
package:

```python
>>> import visit
```

Note, for each session, there is only one instance of visit module (I know!), so
by importing VisIt python package, you can harvest the full capability of VisIt.
