# Name: Ryan Gelston, Lucas Robertson
# Class: CSC 466 (Fall 2018)
# Filename: Validation.py
# Description: Performs cross-validation analysis of the accuracy of the
#  classifiers.
# Usage: python Validation.py <CSVFile> <N> <(optional) RestrFile>

import sys
from C45Util import *
from C45Node import DEFAULT_THRESHOLD


def do_evaluation(csv_filename, n, domain_filename, restrictions_filename=None):
    restrictions = None
    if restrictions_filename:
        restrictions = parse_rest(restrictions_filename, csv_filename)

    categ = parse_categ(domain_filename)
    attr = parse_attr(domain_filename)
    input_data = parse_data(csv_filename)
    evaluation_data = split_data(input_data, n)

    for data_set in evaluation_data:
        tree = C45Node()
        tree.C45_algorithm(attr, data_set['training'], categ, DEFAULT_THRESHOLD)

        return
        # Build tree via induction
        # Classify validation data
        #


def n_fold_cross_validation(attr, data, tree):
    return


def accuracy(diagnostics):
    return diagnostics['correct'] / diagnostics['records_processed']


def error_rate(diagnostics):
    return diagnostics['incorrect'] / diagnostics['records_processed']


def precision(true_positives, false_positives):
    return true_positives / (true_positives + false_positives)


def recall(true_positives, false_negative):
    return true_positives / (true_positives + false_negative)


def f_measure(tp, fp, fn):
    return (2 * precision(tp, fp) * recall(tp, fn)) / (precision(tp, fp) + recall(tp, fn))


def pf_measure(false_positives, true_negatives):
    return false_positives / (false_positives + true_negatives)


def print_confusion_matrix(confusion_matrix):
    print("\tT\tF")
    print("P\t{}\t{}".format(confusion_matrix['true_positives'], confusion_matrix['false_positives']))
    print("N\t{}\t{}".format(confusion_matrix['true_negatives'], confusion_matrix['false_negatives']))


def print_results(diagnostics, recall, precision, pf, f):
    print("\n\n=================================")
    print_confusion_matrix(diagnostics['confustion_matrix'])
    print("Recall: {}".format(recall))
    print("Precision: {}".format(precision))
    print("PF Measure: {}".format(pf))
    print("F Measure: {}".format(f))
    print("=================================\n\n")


def main(argv):
    if len(argv) < 4 or len(argv) > 5 or (not argv[2].isdigit() and argv[2] != '-1'):
        print("Invalid usage of Validation.py\nUsage is 'python Validation.py <CSVFile> <N> <Domain File>"
              "<(optional) RestrFile>")
        exit(1)

    if argv[2] == '1':
        print("Cannot do n-fold cross validation with a value of 1")
        exit(1)

    if len(argv) == 5:
        do_evaluation(argv[1], int(argv[2]), argv[3], argv[4])
    else:
        do_evaluation(argv[1], int(argv[2]), argv[3])


if __name__ == "__main__":
    main(sys.argv)