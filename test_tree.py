import sys
from anytree import Node, RenderTree, LevelOrderGroupIter
from anytree.importer import JsonImporter
from anytree.exporter import DictExporter


class ModuleOne:
    def __str__(self):
        return 'I am module one'

    def test(self):
        return str(self)


class ModuleTwo:
    def __str__(self):
        return 'I am module two'

    def test(self):
        return str(self)


importer = JsonImporter()
data = '''
 {
   "a": "ModuleOne",
   "b": "ModuleTwo",
   "children": [
     {
       "a": "sub0",
       "children": [
         {
           "a": "sub0A",
           "b": "foo"
         },
         {
           "a": "sub0B"
         }
       ]
     },
     {
       "a": "sub1"
     }
   ]
 }'''

this_mod = sys.modules[__name__]

root = importer.import_(data)
exporter = DictExporter()

for node in LevelOrderGroupIter(root, maxlevel=1):
    nodes_dict = exporter.export(node[0])
    del nodes_dict['children']
    for value in nodes_dict.values():
        module_obj = getattr(this_mod, value)()
        print(module_obj.test())
