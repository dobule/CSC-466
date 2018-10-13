# Name: Ryan Gelston
# Class: CSC 466-01 (Fall 2018)
# Filename: C45Node.py
# Description: Impliments the C4.5 classifier using information gain and 
#  information gain ratio measures.

import math

class C45Node:

   def __self__(self, attr, data, categ, threshold):
      """
         Constructor for C45Node

         attr -- Dictionary that contains an array of categories for each 
            attribute. 

         data -- a dictionary with the attribute being the key in data and an
            array of all values in that attribute. Each datapoint is in the same 
            index across all attribute arrays.

         categ -- Tuple with attribute name in index 0 and an array of values
            that attribute in index 1. This parameter specifies the attribue
            that the decision tree classifies items into.

         threshold -- Information gain of an attribute must be greater than 
            this number in order to split along that attribute.
      """
      self.children = {}
      self.isLeaf = False
      self.__C45_algorithm(attr, data, categ, threshold)
      return

   def classify(self, item):
      """
         Takes a datapoint and classifies it using the built-in tree
      """
      return

   def to_xml_string(self, p=1.0):
      """
         Returns the tree as a string formatted in XML
      """
      return

   def __C45_algorithm(self, attr, data, categ, threshold):
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

      if splitAttr == None: 
         self.__set_to_leaf(data[categ[0]], categ)
      else:
         # Construct tree
         self.attribute = splitAttr
         splitData = self.__split_dataset(data, splitAttr)
         attr.pop(splitAttr, None)

         for val, dataSet in splitData:
            self.__add_child(val, dataSet, attr)

      return

   def __set_to_leaf(self, data, categ, homogenous=False):
      """
         Sets the current node to a leaf.
      """

      self.attribute = categ
      self.isLeaf = True

      if homogenous == True:
         self.value = data[0]
      else:
         self.value = self.__find_most_frequent_label(data)

      return

   def __find_most_frequent_label(self, data):
      """
         Finds the most frequent label in array 'data'.
      """

      hist = self.__histogram(data)
      return max(hist, key=hist.get)


   def __select_splitting_attribute(self, attr, data, categ, threshold):
      """
         Returns the attribute that is most apt for splitting the dataset.
      """

      # Find the entropy for the category in data
      p0 = self.__entropy(data[categ[0]])
      pA = {}
      gain = {}
      gainRatio = {}

      # Find the entropy for each attribute in data
      for a in attr.keys():
         pA[a] = self.__entropy(data[a]) 
         gain[a] = p0 - pA[a]
         gainRatio[a] = gain[a] / pA[a]

      # Find attribute with besst gain ratio
      best = max(gainRatio, key=gainRatio.get)

      if gain[best] > threshold:
         return best
      else:
         return None

   def __entropy(self, data):
   """ Calculates the entropy of the array data """

      hist = self.__histogram(data)
      sumProb

      for val in hist.values():
         prob = float(val) / len(data)
         sumProb = prob * math.log(prob, 2) 

      return -1 * sumProb

   def __split_dataset(self, attr, data):
      return

   def __add_child(self, attr, data, categ, threshold, p):

      for 
      return
 
   def __histogram(self, data):
      """ Creates histogram from data array. Returns as dict """
      hist = {}

      for val in data:
         if val in hist.keys():
            hist[val] = hist[val] + 1
         else
            hist[val] = 1
  
      return hist
