# Name: Ryan Gelston, Lucas Robertson
# Class: CSC 466 (Fall 2018)
# Filename: Classifier.py
# Description:
# Usage: python Classifier <CSVFile> <XMLFile>

import sys
from C45Util import *

SILENT_RUN = True


def main(argv):
    if len(argv) != 3:
        print("Invalid number of arguments\nUsage is 'python Classifer <CSVFile> <XMLFile>'")
        exit(1)
    else:
        diagnostics = classify(argv[1], argv[2])
        print_results(diagnostics)


def classify(csv_filename, xml_filename):
    tree = tree_from_xml(xml_filename)
    data = parse_data(csv_filename)
    entry_count = len(list(data.values())[0])
    categ = get_categ_label(csv_filename)
    diagnostics = {
        'records_processed': entry_count,
        'correct': 0,
        'incorrect': 0,
        'accuracy': 0.0,
        'error_rate': 0.0,
        'errors': 0
    }

    for i in range(entry_count):
        itemized_entry = itemize_entry(data, i)
        result = ""
        try:
            result = tree.classify(itemized_entry)
        except KeyError:
            print(("[{}] Error classifying row!".format(i), "[{}]\tError!".format(i))[SILENT_RUN])
            diagnostics['errors'] += 1
            continue
        if categ in itemized_entry:
            is_correct = result == itemized_entry[categ]
            if is_correct:
                diagnostics['correct'] += 1
            else:
                diagnostics['incorrect'] += 1

            verbose_message = "[{}] {} : {} | {}".format(i, itemized_entry, result,
                                                         ('Incorrect', 'Correct')[is_correct])
            silent_message = "[{}]\tWas {}\t| Should be {}".format(i, result, itemized_entry[categ])
        else:
            verbose_message = "[{}] {} : {}".format(i, itemized_entry, result)
            silent_message = "[{}]\tWas {}".format(i, result)

        print((verbose_message, silent_message)[SILENT_RUN])

    diagnostics['accuracy'] = diagnostics['correct'] / diagnostics['records_processed'] * 100
    diagnostics['error_rate'] = diagnostics['incorrect'] / diagnostics['records_processed'] * 100
    if categ not in itemized_entry:
        diagnostics['correct'] = 'N/a'
        diagnostics['incorrect'] = 'N/a'
        diagnostics['accuracy'] = 'N/a'
        diagnostics['error_rate'] = 'N/a'

    return diagnostics


def print_results(diagnostics):
    print("\n\n====================================")
    print("Records Processed: ", diagnostics['records_processed'])
    print("Records Not Processed:", diagnostics['errors'])
    print("# Correct: ", diagnostics['correct'])
    print("# Incorrect: ", diagnostics['incorrect'])
    print("% Correct: {}%".format(diagnostics['accuracy']))
    print("% Incorrect: {}%".format(diagnostics['error_rate']))
    print("======================================\n\n")


def itemize_entry(data, index):
    entry = {}
    for key in data:
        entry[key] = data[key][index]

    return entry


if __name__ == "__main__":
    main(sys.argv)