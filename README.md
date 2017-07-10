PyVDF
==
Parse VDFs and Valve KeyValue Files

[![Code Climate](https://codeclimate.com/github/amreuland/PyVDF/badges/gpa.svg)](https://codeclimate.com/github/amreuland/PyVDF)
[![Build Status](https://img.shields.io/travis/amreuland/PyVDF.svg?branch=master)](https://travis-ci.org/amreuland/PyVDF)
[![PyPI version](https://img.shields.io/pypi/v/pyvdf.svg)](https://pypi.python.org/pypi/PyVDF)
[![Coverage Status](https://img.shields.io/coveralls/amreuland/PyVDF.svg)](https://coveralls.io/r/amreuland/PyVDF)


## Documentation
* PyVDF - https://amreuland.github.io/PyVDF
* KeyValues - https://developer.valvesoftware.com/wiki/KeyValues

## Installation
`pip install PyVDF`

## API
All functionality is provided through the PyVDF module.
import it and call it to create an instance, or just call the static methods off the import.

## Basic Usage
```python
from PyVDF import PyVDF
Foo = PyVDF()
Foo = PyVDF(data=StringOData)
Foo = PyVDF(infile="/path/to/file.ext")
Foo = PyVDF(infile=fileInstance)
```

## edit
```python
from PyVDF import PyVDF
vdf = PyVDF()
file = vdf.load('path/file.vdf')
vdf.edit('foo.id', 'value')
vdf.write_file('path/foo.vdf')
```
