import sys
from anytree import Node, RenderTree, LevelOrderGroupIter
from anytree.importer import JsonImporter
from anytree.exporter import DictExporter


class ModuleMain:
    def __str__(self):
        return 'I am module main'

    def test(self, parent):
        return str(self) + ', my parent ' + str(parent)


class ModuleOne(ModuleMain):
    def __str__(self):
        return 'I am module 1'


class ModuleTwo(ModuleMain):
    def __str__(self):
        return 'I am module 2'


class ModuleChildrenLeftOneOne(ModuleMain):
    def __str__(self):
        return 'I am module 11'


class ModuleChildrenLeftOneTwo(ModuleMain):
    def __str__(self):
        return 'I am module 12'


class ModuleChildrenLeftTwoOne(ModuleMain):
    def __str__(self):
        return 'I am module 21'


class ModuleChildrenLeftTwoTwo(ModuleMain):
    def __str__(self):
        return 'I am module 22'


class ModuleChildrenRightOneOne(ModuleMain):
    def __str__(self):
        return 'I am module 11'


class ModuleChildrenRightOneTwo(ModuleMain):
    def __str__(self):
        return 'I am module 12'


class ModuleChildrenLeftOneTwoOne(ModuleMain):
    def __str__(self):
        return 'I am module 221'


class ModuleChildrenLeftTwoOneTwo(ModuleMain):
    def __str__(self):
        return 'I am module 112'


class ModuleChildrenLeftTwoTwoThree(ModuleMain):
    def __str__(self):
        return 'I am module 123'


importer = JsonImporter()
data = '''
 {
   "a": "ModuleMain",
   "children": [
     {
       "a": "ModuleOne",
       "children": [
         {
           "a": "ModuleChildrenLeftOneOne",
           "children": [
             {
                "a": "ModuleChildrenLeftOneTwoOne"
             },
             {
                "a": "ModuleChildrenLeftTwoOneTwo"
             },
             {
                "a": "ModuleChildrenLeftTwoTwoThree"
             }
           ]
         },
         {
            "a": "ModuleChildrenLeftOneTwo"
         },
         {
            "a": "ModuleChildrenLeftTwoOne"
         },
         {
            "a": "ModuleChildrenLeftTwoTwo"
         }
       ]
     },
     {
       "a": "ModuleTwo",
       "children": [
         {
           "a": "ModuleChildrenRightOneOne"
         },
         {
            "a": "ModuleChildrenRightOneTwo"
         }
       ]
     }
   ]
 }'''

this_mod = sys.modules[__name__]

root = importer.import_(data)

exporter = DictExporter()


def call_module(node_dict, node):
    for value in node_dict.values():
        module_obj = getattr(this_mod, value)()
        if node.parent:
            print(exporter.export(node.parent))
        # print(module_obj.test(''))


for nodes_list in LevelOrderGroupIter(root):
    print('level: {}'.format(nodes_list[0].depth))
    for node in nodes_list:
        node_dict = exporter.export(node)
        if 'children' in node_dict:
            del node_dict['children']
        call_module(node_dict, node)
