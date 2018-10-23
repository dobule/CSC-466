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

THRESHOLD = 0.10001


def induce_c45(domain_filename, csv_filename, restrictions_filename=None, input_data=None):
    attr = parse_attr(domain_filename)
    data = None
    if input_data:
        data = input_data
    else:
        data = parse_data(csv_filename)
    categ = parse_categ(domain_filename)

    # Puts returnes data in a standardized form
    data = sanitize_data(attr, data, categ)

    # Impose restrictions if provided
    if restrictions_filename:
        rest = parse_rest(restrictions_filename, csv_filename)
        rest_attr(rest, data)

    tree = C45Node()
    tree.C45_algorithm(attr, data, categ, THRESHOLD)
    xmltree = tree.to_xml_tree("C45DecisionTree")

    #print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    xmltree.write("C45DecisionTree.xml")
    return "C45DecisionTree.xml"

def main():
    if not (len(sys.argv) in [3, 4]):
        print("python InduceC45.py <domainFile.xml> " +
        "<trainingSetFile.csv> [<restrictions.csv>]")
        return

    if len(sys.argv) == 4:
        induce_c45(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        induce_c45(sys.argv[1], sys.argv[2])

if __name__=="__main__":
    main()
