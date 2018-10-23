# Name: Ryan Gelston, Lucas Robertson
# Class: CSC 466 (Fall 2018)
# Filename: Classifier.py
# Description:
# Usage: python Classifier <CSVFile> <XMLFile>

import sys
from C45Util import *
import xml.etree.ElementTree as et

SILENT_RUN = True


def main(argv):
    if len(argv) != 3:
        print("Invalid number of arguments\n" +
         "Usage: 'python Classifer.py <CSVFile> <XMLFile>'")
        exit(1)
    else:
        diagnostics = classify(argv[1], argv[2])
        print_results(diagnostics)


def classify(csv_filename, xml_filename):

    elem_tree = et.parse(xml_filename).getroot().getchildren()[0]

    tree = C45Node()
    tree.build_from_elem_tree(elem_tree)
    data = parse_data(csv_filename)
    entry_count = len(list(data.values())[0])
    categ = get_categ_label(csv_filename)
    diagnostics = diagnostics = create_diagnostics(entry_count, 0, 0, 0, 0, 0)

    for i in range(entry_count):
        itemized_entry = itemize_entry(data, i)
        result = ""
        try:
            result = tree.classify(itemized_entry)
        except KeyError:
            print(("[{}] Error classifying row!".format(i), 
                   "[{}]\tError!".format(i))[SILENT_RUN])
            diagnostics['errors'] = diagnostics['errors'] + 1
            continue

        if categ in itemized_entry:
            is_correct = (itemized_entry[categ] in result)

            if is_correct:
                diagnostics['correct'] = diagnostics['correct'] + 1
            else:
                diagnostics['incorrect'] = diagnostics['incorrect'] + 1


            verbose_message = "[{}] {} : {} | {}".format(i, itemized_entry, 
             result, ('Incorrect', 'Correct')[is_correct])
            silent_message = "[{}]\t{}\tWas {}\t| Should be {}".format(i,
            ('Incorrect', 'Correct\t')[is_correct], result,
             itemized_entry[categ])
        else:
            verbose_message = "[{}] {} : {}".format(i, itemized_entry, result)
            silent_message = "[{}]\tWas {}".format(i, result)
            diagnostics['errors'] = diagnostics['errors'] + 1

        print((verbose_message, silent_message)[SILENT_RUN])

    # Calculate accuracy and error rate after classifying data set
    diagnostics['accuracy'] = (float(diagnostics['correct']) / 
                               diagnostics['records_processed'] * 100)
    diagnostics['error_rate'] = (float(diagnostics['incorrect']) / 
                                 diagnostics['records_processed'] * 100)

    if categ not in itemized_entry:
        diagnostics['correct'] = 'N/a'
        diagnostics['incorrect'] = 'N/a'
        diagnostics['accuracy'] = 'N/a'
        diagnostics['error_rate'] = 'N/a'

    return diagnostics


def print_results(diagnostics):
    print("\n\n======================================")
    print("Records Processed: ", diagnostics['records_processed'])
    print("Records Not Processed:", diagnostics['errors'])
    print("# Correct: ", diagnostics['correct'])
    print("# Incorrect: ", diagnostics['incorrect'])
    print("% Correct: {}%".format(diagnostics['accuracy']))
    print("% Incorrect: {}%".format(diagnostics['error_rate']))
    print("======================================\n\n")


if __name__ == "__main__":
    main(sys.argv)
