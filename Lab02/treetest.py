import xml.etree.ElementTree as et
import C45Node

tree = et.parse("testTree.xml").getroot();
print(tree.tag)
