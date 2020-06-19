import collisionDetector as cd
import coordsProcessor as cp
import dataExtractor as de
import sys


class Test:

    testcases = [
    ]

    def run(self, detections):
        print("working on testcases")
        dataExtractor = de.dataExtractor(outputJsonPath='json')
        self.testcases += (dataExtractor.processRawData(detections))
        for testcase in self.testcases:
            print('Testcase: ', testcase)
            coordinates_processor = cp.CoordinatesProcessor(testcase)
            coordinates_processor.processBoundingBoxes()
            collision_detector = cd.CollisionDetector(
                coordinates_processor.results)

            if collision_detector.processSamples():
                print("Riesgo de colision\n")
            else:
                print("No existe riesgo\n")
            #print('result: ', collision_detector.processSamples(), end='\n \n \n')


if __name__ == '__main__':
    test = Test()
    test.run(sys.argv[1])
