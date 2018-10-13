# Name: Ryan Gelston
# Class: CSC 466-01 (Fall 2018)
# Filename: InduceC45.py
# Description: Impliments the C4.5 classifier using information gain and 
#  information gain ratio measures.

class C45Node:

   def __self__(self, attr, data, categ, threshold):
      """
         Constructor for C45Node

         attr -- dictionary that contains an array of categories for each 
            attribute

         data -- a dictionary with the attribute being the key in data and an
            array of all values in that attribute. Each datapoint is in the same 
            index across all attribute arrays.

         cated -- a string that states the attribute to categorize
      """
      self.children = {}
      self.isLeaf = False
      return

   def classify(self, item):
      """
         Takes a datapoint and classifies it using the built-in tree
      """
      return

   def to_xml_string(self):
      """
         Returns the tree as a string formatted in XML
      """
      return

   def __C45_algorithm(self, attr, data, threshold):
      """
         Constructs a decision tree using the C4.5 algorithm.
      """

      # Check termination conditions
      if self.__check_homogenous_data(attr, data, categ):
         self.__set_to_leaf(data, categ, homogenous=True)
         return
      elif len(attr.keys()) == 0:
         self.__set_to_leaf(data, categ)
         return

      # Select splitting attribute
      splitAttr = self.__select_splitting_attribute(attr, data, threshold)

      if splitAttr == NULL: 
         self.__set_to_leaf(data, categ)
      else:
         # Construct tree
         self.attribute = splitAttr
         splitData = self.__split_dataset(data, splitAttr)
         attr.pop(splitAttr, None)

         for val, dataSet in splitData:
            self.__add_child(val, dataSet, attr)

      return

   def __set_to_leaf(self, data, categ, homogenous=False):
      self.attribute = categ
      self.isLeaf = True

      if homogenous == True:
         self.value = data[0]
      else:
      
         self.value = # TODO: Get key for max value in catHist

      return

   def __find_most_frequent_label(self, data):
      catHist = {}

      for dataPoint in data: 
         if dataPoint in catHist.keys:
            catHist[dataPoint] = catHist[dataPoint] + 1
         else
            catHist[dataPoint] = 1
      
      return 

   def __select_splitting_attribute(self, attr, data, threshold):
      return

   def __entropy(self):
      return

   def __information_gain(self):
      return

   def __information_gain_ratio(self):
      return

   def __split_dataset(self, attr):
      return

   def __add_child(self):
      return
 

   
   
