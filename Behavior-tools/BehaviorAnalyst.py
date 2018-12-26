####################################################
# Dependencies
####################################################

# Dependencies for behavioral analysis
from sklearn.metrics.pairwise import euclidean_distances

# Distance cutoff for heat possibility
DISTANCE_CUTOFF = 75

class BehaviorAnalyst:

    def calculateDistance(self, point_a, point_b):
        return euclidean_distances(point_a, point_b)[0][0]

    def verifyBodyPart(self, part_a, part_b):
        pass

    def examineDistance(self, dist):
        if dist >= DISTANCE_CUTOFF:
            return False
        return True

    def analyzeHeatProbOnFrame(self, point_a, point_b):

        dist = self.calculateDistance(point_a, point_b)
        examined_result = self.examineDistance(dist)

        # print("----> Dist =", dist)

        if examined_result:
            # heat state is True, and CS is increased
            # print("----> ++")
            return True, 1
        else:
            # heat state is False, and CS is decreased
            # print("----> --")
            return False, -1
