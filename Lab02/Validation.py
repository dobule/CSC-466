# Name: Ryan Gelston
# Class: CSC 466 (Fall 2018)
# Filename: Validation.py
# Description: Performs cross-validation analysis of the accuracy of the 
#  classifiers.

from C45Node import C45Node
from C45Util import *

import sys

def main():
    if not len(sys.argv) in range(3,7):
        print ("Usage: python Validate.py <domain.xml> <trainSet.csv> " +
            "[<restictions.csv>] -fold [<num>]")


    N = 10 # Default value for n-fold validation

    attr = parse_attr(sys.argv[1])
    data = parse_data(sys.argv[2])
    categ = parse_categ(sys.argv[1])

    data = sanitize_data(attr, data, categ)

    if len(sys.argv) >= 4 and sys.argv[3] != "-fold":
        rest = parse_rest(sys.argv[3], sys.argv[1])
        rest_attr(rest, data)

    if "-fold" in sys.argv:
        N = sys.argv[sys.argv.index("-fold") + 1]

def n_fold_cross_validation():
   return

def accuracy():
   return

def error_rate():
   return

def precision():
   return

def recall():
   return

def confusion_matrix():
   return

def f_measure():
   return


if __name__=="__main__":
    main()
