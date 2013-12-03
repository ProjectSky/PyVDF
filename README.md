PyVDF
==

A set of Python Classes to read and write VDF (Valve Data Format) files.

###What is a VDF?
https://developer.valvesoftware.com/wiki/KeyValues#File_Format

* [VDFParser] [1]
* [VDFWriter] [2]
* [Key Paths] [3] 
  * [Get Paths] [4]
  * [Set Paths] [5]
* [Programs/Projects using PyVDF] [6]


How do I use these Wonderful Classes?
--
Simple

###VDFParser
Does what the name says, it reads a vdf and returns a useable array.

####Usage
First, import the Class. If you are in the same folder, just drop the `PyVDF.` from the Imports. Then Give it the filename of the file to read
```Python
from PyVDF.VDFParser import VDFParser
vdf = VDFParser('string')
```
You will get a warning if something went wrong, but its pretty good at fixing its own mistakes. Now to find a value from a [path] [3] (see below), just use the `find(string)` or `findMany([list])` functions:
```Python
value = vdf.find('Foo.Bar')
values = vdf.findMany(['Foo.Bar', 'Foo.Bar.FooBar'])
```
To get an array of all the keys and values, call the `getData()` function:
```Python
array = vdf.getData()
```
To read a different file without declaring a new VDFParser, the `setFile('string')` function will change to that file and automatically read it, now when you call `find()`, `findMany()`, or `getData()`, fyou will get the data from the new file

###VDFWriter
A bit trickier than VDFParser, and not as straight forward

####Usage
First, import the Class. If you are in the same folder, just drop the `PyVDF.` from the Imports. Then give the filename of a file and add in some optional data
```Python
from PyVDF.VDFWriter import VDFWriter
writer = VDFWriter('filename', data)
```
The Data must be a Dictionary (Dict) or an OrderedDictionary (OrderedDict). I use OrderedDictionaries, because I like my data to come out in the same order I put it in.

Now that we have created the writer, lets set some values. Value string must be structured like this: `Path.To.Key=Value` Once you have your key-value pair, or 'set string', you can either pass that into the `edit(string)` function or pass a list of set strings into the `editMany([list])` function. Neither will return any value. Also, if the Path to the key is not found, it will be created.
```Python
writer.edit('Foo.Bar=FooBar')
writer.editMany(['Foo.Foo=Bar', 'Foo.Bar.FooBar=FooBar'])
```
Once you have made some edits, you can write the data out to a file with `write()`. You must call this whenever you want to save. This is so there isn't any excesive file I/O.

To undo what you have edited, call the `undo()` function. THIS WILL UNDO ALL EDITS SINCE LAST WRITE. Finally, to change the file being written to, call the `setFile('string')` function.

###Key Paths
Keypaths are what I call the array structure to a value.
Say you have a file like this:
```Python
"Foo"
{
  "Fuu"   "Bar"
  "Bar"
  {
    "FooBar"    "FooBar"
  }
}
```
#####Get Paths
To get the Value `Bar`, you need to find the key `Fuu`
The Path to Fuu is `Foo.Fuu`

This is a Get Path, because you use it with the `VDFParser.find()` and `VDFParser.findMany()` functions

#####Set Paths
To set the value at Key `FooBar` to `Bar`, we have to get its path and then tell it to set the value to Bar.

`Foo.Bar.FooBar=Bar`

The the Path part is 'Foo.Bar.FooBar' and the Value is 'Bar'. 


Programs/Projects using PyVDF
--
* vdfedit - https://github.com/amreuland/vdfedit


[1]: #vdfparser "VDFParser"
[2]: #vdfwriter "VDFWriter"
[3]: #key-paths "Key Paths"
[4]: #get-paths "Get Key Paths"
[5]: #set-paths "Set Key Paths"
[6]: #programsprojects-using-pyvdf "What uses PyVDF?"