import os
from tagTokens import *


class CoordinatesProcessor:

    results = None

    def __init__(self, bounding_boxes_list=None):
        '''
        [bounding_boxes] contornos de cada etiqueta
        '''
        self.bounding_boxes_list = bounding_boxes_list
        self.results = []

    def defineBoundingBoxScale(self, bb_data):
        '''
        Se revisan los tamanos de cada bounding box y se obtiene
        la proporcion de dicha bounding box comparado con las constantes definidas
        en tagTokens.py
        '''
        #print(bb_data,len(bb_data))
        tag_class, x, y, h, w = bb_data
        area = h * w


        if tag_class == 'Person':
            return ((area * 100) / PERSON_AREA, x, y, h, w, "person")
        elif tag_class == "forklift":
            return ((area * 100) / FORKLIFT_AREA, x, y, h, w, "forklift")

        return None

    def processBoundingBoxes(self):
        '''
        Se procesan todas las bounding boxes de una cierta imagen
        '''

        for bb_data in self.bounding_boxes_list:
            self.results.append(self.defineBoundingBoxScale(bb_data))

        #print(self.results)

        return self.results
