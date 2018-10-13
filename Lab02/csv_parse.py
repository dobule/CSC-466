import numpy as np
import xml.etree.ElementTree as et

domain_file = 'domain.xml'
words_file = 'Datasets/tree02-20-words.csv'


class C45Util:
    
    def parse_data(file_name):
        data = np.genfromtxt(file_name, delimiter=',', dtype=str, skip_header=3)
        headers = np.genfromtxt(file_name, delimiter=',', dtype=str,  skip_footer=len(data) + 2)

        dict = {}
        for i in range(len(headers)):
            dict[headers[i]] = data[:, i]
    
        return dict


    def parse_attr(file_name):
        xml = et.parse(file_name).getroot().getchildren()
        for category in xml:
            print(category.tag)
        return ""



C45Util.parse_attr(domain_file)
