__all__ = ['PyVDF']
#####################################
# PyVDF.py                          #
# Author: Austin Reuland            #
# For Reading and Writing           #
#    VDF Files                      #
#   (Valve Data File)               #
# Copyright (c) 2014 Austin Reuland #
#####################################

import re
from collections import OrderedDict

#############
# PyVDF #
#############
class PyVDF:

  _UseDict = dict
  _AllowNewlines = False
  _OutputIndentation = "\t"
  _OutputSpacing = "\t\t"
  _CondensedOutput = False
  _MaxTokenLength = 1200

  __ErrorReadLongToken__ = "Holy Long Strings Batman!\n There is a token largers than {} characters on line {}"
  __ErrorReadTokenNewline__ = "Newline in Token at line {}\n Use allowTokenNewlines(True) to ignore this."
  __ErrorReadBlockNoKey__ = "Value block without a Key at line {}.\n Last Token: {}"
  __ErrorReadCompanionBrace_ = "Expected to get a Value, got '}}' instead.\n At line {}. Last Token: {}"
  __ErrorReadEOFToken__ = "Hit End of Data while reading token"
  __ErrorReadEOFArray__ = "Missing braces"

  def __init__(self):
    self.data = PyVDF._UseDict()

  def __getitem__(self, key):
    return self.find(key)

  def __setitem__(self, key, value):
    self.edit(key, value)

  @staticmethod
  def useFastDict(var = True):
    PyVDF._UseDict = dict if var else OrderedDict

  @staticmethod
  def allowTokenNewlines(var = False):
    PyVDF._AllowNewlines = var

  @staticmethod
  def setIndention(var = "\t"):
    PyVDF._OutputIndentation = var

  @staticmethod
  def setSpacing(var = "\t\t"):
    PyVDF._OutputSpacing = var

  @staticmethod
  def setCondensed(var = False):
    PyVDF._CondensedOutput = var

  @staticmethod
  def setMaxTokenLength(var = 1024):
    PyVDF._MaxTokenLength = var

  @staticmethod
  def parse(s):
    ci = 0
    line = 0
    grabKey = True
    UsageDict = PyVDF._UseDict
    tokenNewLines = ValueError if PyVDF._AllowNewlines else Exception
    data = UsageDict()
    keys = list()
    keyApp = keys.append
    keyPop = keys.pop
    tree = data
    maxTokenLength = PyVDF._MaxTokenLength

    if PyVDF._AllowNewlines:
      re_quoted_token = re.compile(r'"(?:\\.|[^"])*"', re.M)
    else:
      re_quoted_token = re.compile(r'"(?:\\.|[^"])*"')

    re_unquoted_token = re.compile(r'^(?:\\.|[^\\"\s\{\}\[\]])*')

    try:
      while 1:
        char = s[ci]

        while char in ('\t', ' '):
          ci += 1
          char = s[ci]

        if char == '"':
          try:
            string = re_quoted_token.match(s[ci:ci + maxTokenLength]).group()[1:-1]
            ci += len(string) + 1
          except AttributeError:
            # string = ''
            # while 1:
            #   ci += 1
            #   char = s[ci]
            #   if char == '\0':
            #     raise Exception(PyVDF.__ErrorReadEOFToken__)

            #   if char == '"':
            #     break

            #   if char in ('\r', '\n'):
            #     try:
            #       raise tokenNewLines(PyVDF.__ErrorReadTokenNewline__.format(line))
            #     except ValueError:
            #       line += 1
            #       ci += 1
            #   if char == '\\':
            #     ci += 1
            #     char = s[ci]
            #     if char == '\0':
            #       raise Exception(PyVDF.__ErrorReadEOFToken__)

            #   string += char
            raise Exception(PyVDF.__ErrorReadLongToken__.format(maxTokenLength, line))

          if grabKey:
            k = string
          else:
            tree[k] = string
          grabKey = not grabKey

        elif char == '{':
          if not grabKey:
            keyApp(k)
            tree[k] = UsageDict()
            tree = tree[k]
            grabKey = True
          else:
            raise Exception(__ErrorReadBlockNoKey__.format(line, k))

        elif char == '}':
          if grabKey:
            keyPop()
            tree = data
            for key in keys:
              tree = tree[key]
          else:
            Exception(PyVDF.__ErrorReadCompanionBrace_.format(line, k))

        elif char == '\n':
          if s[ci + 1] == '\r':
            ci += 1
          line += 1

        elif char == '\r':
          if s[ci + 1] == '\n':
            ci += 1
          line += 1

        elif char == '/' and s[ci + 1] == '/':
          line += 1
          ci += 1
          while 1:
            ci += 1
            if s[ci] in ('\n', '\r'):
              break

        elif char == '[':
          while 1:
            ci += 1
            if s[ci] == ']':
              break

        else:
          try:
            string = re_unquoted_token.match(s[ci:ci + maxTokenLength]).group()
            ci += len(string)
          except AttributeError:
            # string = ''
            # while 1:
            #   if char in ('\t', ' ', '\n', '\r', '{', '}', '[', ']', '"'):
            #     break

            #   if char == '\\':
            #     ci += 1
            #     char = s[ci]
            #     if char == '\0': raise Exception(PyVDF.__ErrorReadEOFToken__)

            #   string += char

            #   ci += 1
            #   char = s[ci]
            #   if char == '\0':
            #     raise Exception()
            raise Exception(PyVDF.__ErrorReadLongToken__.format(maxTokenLength, line))

          if grabKey:
            k = string
          else:
            tree[k] = string
          grabKey = not grabKey
          continue

        ci += 1

    except IndexError:
      if len(keys) == 0:
        return data
      raise Exception(PyVDF.__ErrorReadEOFArray__)

  @staticmethod
  def formatData(data):
    condensed = PyVDF._CondensedOutput
    indentation = PyVDF._OutputIndentation
    spacing = PyVDF._OutputSpacing
    def loop(array, tab=''):
      string = ''
      for k, v in array.iteritems():
        string += '{}"{}"'.format(tab,k)
        if isinstance(v, dict):
          string += '{}{{\n{}{}}}\n'.format(
            '' if condensed else '\n' + tab,
            loop(v, tab + indentation),
            tab)
        else:
            string += '{}"{}"\n'.format(spacing, v)
      return string
    return loop(data)

  @staticmethod
  def writeData(filename, data):
    if not isinstance(data, dict):
      if isinstance(data, list):
        raise Exception("Cannot write out List Data\n {}".format(repr(data)))
      else:
        raise Exception("Data to write is not a Dictionary\n {}".format(repr(data)))
    try:
      filec = open(filename, 'w')
      data = PyVDF.formatData(data)
      filec.write(data)
      filec.close()
    except IOError as e:
      print("Could not open '" + filename + "' for writing.")
      print(e)
    
  def load_file(self, filename):
    try:
      with open(filename) as filec:
        self.data = PyVDF.parse(filec.read())
        filec.close()
    except IOError as e:
      print("Could not open '" + filename + "' for reading.")
      print("Ignore this if you are creating a new file.")

  def load_string(self, string):
    self.data = PyVDF.parse(string)

  def getData(self):
    return self.data

  def setData(self, data):
    self.data = data

  def find(self, path):
    p = [re.sub('[\[\]]', '', w) for w in re.findall(r'[^\.\[\]]+|\[[^\[\]]*\]', path)]
    array = self.data
    for c in p:
      try:
        array = array[c]
      except KeyError:
        return ''
    return array

  def edit(self, path, value):
    UsageDict = PyVDF._UseDict
    p = [re.sub('[\[\]]', '', w) for w in re.findall(r'[^\.\[\]]+|\[[^\[\]]*\]', path)]
    array = self.data
    a = array
    for c in p[:-1]:
      try:
        if not isinstance(a[c], dict):
          a[c] = UsageDict()
      except KeyError:
        a[c] = UsageDict()
      a = a[c]
    if value == ";;DELETE;;":
      a.pop(p[-1], None)
    else:
      a[p[-1]] = value
    self.data = array

  def findMany(self, paths):
    return map(self.find, paths)

  def editMany(self, paths):
    map((lambda (p, v): self.edit(p, v)), paths)

  def write_file(self, filename):
    self.writeData(filename, self.data)

  def toString(self):
    return PyVDF.formatData(self.data)

  # def toJson(self):
  #   for k, v in

  # def fromJson(self):
