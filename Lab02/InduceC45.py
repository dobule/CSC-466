# Name: Ryan Gelston
# Class: CSC 466-01
# Term: Fall 2018
#
# Filename: InduceC45.py
# Usage: python InduceC45.py <domainFile.xml> <trainingSetFile.csv>
# [<restrictions.csv>]
# Description: Prints an xml decision tree to stdout. TODO 

import sys
from C45Node import C45Node
from C45Util import *

THRESHOLD = 0.05

def main():
    if not (len(sys.argv) in [3, 4]):
        print("python InduceC45.py <domainFile.xml> " +
        "<trainingSetFile.csv> [<restrictions.csv>]")
        return
    attr = parse_attr(sys.argv[1])
    data = parse_data(sys.argv[2])
    categ = parse_categ(sys.argv[1])

    # Puts returnes data in a standardized form
    data = sanitize_data(attr, data, categ)

    # Impose restrictions if provided
    if len(sys.argv) == 4:
        rest = parse_rest(sys.argv[3], sys.argv[1])
        rest_attr(rest, data)

    tree = C45Node()
    tree.C45_algorithm(attr, data, categ, THRESHOLD)
    xmltree = tree.to_xml_tree("C45DecisionTree")

    print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    xmltree.write("C45DecisionTree.xml")

if __name__=="__main__":
    main()
