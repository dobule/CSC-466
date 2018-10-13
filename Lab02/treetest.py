import xml.etree.ElementTree as et
from C45Node import *

# indent function courtesy of user ade on this stack overflow post: https://stackoverflow.com/questions/749796/pretty-printing-xml-in-python
# (user profile: https://stackoverflow.com/users/97238/ade)
def __indent(elem, level=0):
    i = "\n" + level*"  "
    j = "\n" + (level-1)*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem

def write_tree(root, tree_name):
    xml_root = et.Element("Tree", name=tree_name)
    __write_tree_r(root, xml_root)
    __indent(xml_root)
    tree = et.ElementTree(xml_root)
    tree.write("test.xml")

def __write_tree_r(root, xml_root):
    if root.isLeaf:
        et.SubElement(xml_root, "decision", choice=root.choice)
        return

    xml_child = et.SubElement(xml_root, "node", var=root.attribute)
    for child_key in root.children:
        child = root.children[child_key]
        xml_edge = et.SubElement(xml_child, "edge", var=child_key)
        write_tree_r(child, xml_edge)


xml_root = et.parse("testTree.xml").getroot().getchildren()[0]

tree = C45Node(xml_root)

write_tree(tree, "test")
