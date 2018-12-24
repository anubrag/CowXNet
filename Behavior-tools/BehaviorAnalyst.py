####################################################
# Dependencies
####################################################

# Dependencies for behavioral analysis
from sklearn.metrics.pairwise import euclidean_distances

class BehaviorAnalyst:
	def __init__(self):

	def calculateDistance(self, point_a, point_b):
		return euclidean_distances(point_a, point_b)[0][0]

	def verifyBodyPart(self, part_a, part_b):
		pass

	def examineDistance(self, dist):
		pass

	def analyzeHeatProbOnFrame(self, examined_result):

		if examined_result:
			# heat state is True, and CS is increased
		else:
			# heat state is False, and CS is decreased

		# Save state
