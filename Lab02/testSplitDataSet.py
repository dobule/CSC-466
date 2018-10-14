from C45Node import C45Node
from C45Util import *

ATTR_PATH = "./domain.xml"
DATA_PATH = "./Datasets/tree01-100-words.csv"


attr = parse_attr(ATTR_PATH)

categ = parse_categ(ATTR_PATH)

data = parse_data(DATA_PATH)
data = sanitize_data(attr, data)

tree = C45Node()
tree.C45_algorithm(attr, data, categ, 0.6)


