import re
from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

#Divisions used to separate the features attributing to a class
points_div		=	[-5.90,-2.07,1.75,5.57,9.39,13.22,17.04,20.86,24.68,100]
fumble_div		=	[-0.25,0.00,0.24,0.49,0.74,0.99,1.24,1.49,1.73,10]
targets_div		=	[-3.25,-1.29,0.67,2.63,4.59,6.55,8.51,10.47,12.43,50]
rec_div			=	[-3.94,-2.42,-0.91,0.60,2.12,3.63,5.14,6.66,8.17,50]
rec_yds_div		=	[-26.64,-8.28,10.07,28.42,46.77,65.13,83.48,101.83,120.19,500]
yac_div			=	[-20.04,-10.51,-0.98,8.55,18.08,27.61,37.15,46.68,56.21,500]
td_div			=	[-0.65,-0.32,0.00,0.33,0.66,0.98,1.31,1.64,1.96,10]


#Divisions and averages used as the classes of resulting stats
result_points_div		=	[-3.0,0.0,0.4,0.7,0.9,1.2,1.5,1.9,2.4,2.9,3.6,4.5,5.6,6.9,8.3,10.3,13.3,100]
result_fumble_div		=	[0.0,1.0,10]
result_targets_div		=	[0.0,1.0,2.0,3.0,4.0,5.0,6.0,8.0,50]
result_rec_div			=	[0.0,1.0,2.0,3.0,4.0,5.0,50]
result_rec_yds_div		=	[-5.0,0.0,5.0,10.0,16.0,24.0,33.0,46.0,65.0,500]
result_yac_div			=	[-8.0,0.0,1.0,3.0,6.0,9.0,13.0,19.0,28.0,500]
result_td_div			=	[0.0,1.0,2.0,10]

result_points_avg		=	[-.021,.224,.566,.848,1.059,1.348,1.744,2.149,2.605,3.225,4.101,5.057,6.251,7.514,9.255,11.640,17.455]
result_fumble_avg		=	[.016,1.021]
result_targets_avg		=	[.675,1.400,2.433,3.422,4.491,5.453,7.425,10.439]
result_rec_avg			=	[.533,1.378,2.453,3.413,4.410,7.192]
result_rec_yds_avg		=	[-.032,3.222,7.840,13.374,20.322,28.849,39.780,55.043,88.350]
result_yac_avg			=	[-.044,.129,2.500,4.945,7.942,11.292,16.390,23.530,42.266]
result_td_avg			=	[.163,1.099,2.118]

class TEModel(MRJob):

	INPUT_PROTOCOL = JSONValueProtocol

	def feature_mapper(self, _, data):

		result_points = data['result_points']
		result_fumble = data['result_fumble']
		result_targets = data['result_targets']
		result_rec = data['result_rec']
		result_rec_yds = data['result_rec_yds']
		result_yac = data['result_yac']
		result_td = data['result_td']

		for index in range(0,len(result_points_avg)):
			if result_points <= result_points_div[index+1]:
				result_points = result_points_avg[index]
				break

		for index in range(0,len(result_fumble_avg)):
			if result_fumble <= result_fumble_div[index+1]:
				result_fumble = result_fumble_avg[index]
				break

		for index in range(0,len(result_targets_avg)):
			if result_targets <= result_targets_div[index+1]:
				result_targets = result_targets_avg[index]
				break

		for index in range(0,len(result_rec_avg)):
			if result_rec <= result_rec_div[index+1]:
				result_rec = result_rec_avg[index]
				break

		for index in range(0,len(result_rec_yds_avg)):
			if result_rec_yds <= result_rec_yds_div[index+1]:
				result_rec_yds = result_rec_yds_avg[index]
				break

		for index in range(0,len(result_yac_avg)):
			if result_yac <= result_yac_div[index+1]:
				result_yac = result_yac_avg[index]
				break

		for index in range(0,len(result_td_avg)):
			if result_td <= result_td_div[index+1]:
				result_td = result_td_avg[index]
				break

		prev_amount = data['prev_amount']
		points = data['points']
		fumble = data['fumble']
		targets = data['targets']
		rec = data['rec']
		rec_yds = data['rec_yds']
		yac = data['yac']
		td = data['td']

		for elem in points_div:
			if points <= elem:
				points = elem
				break

		for elem in fumble_div:
			if fumble <= elem:
				fumble = elem
				break

		for elem in targets_div:
			if targets <= elem:
				targets = elem
				break

		for elem in rec_div:
			if rec <= elem:
				rec = elem
				break

		for elem in rec_yds_div:
			if rec_yds <= elem:
				rec_yds = elem
				break

		for elem in yac_div:
			if yac <= elem:
				yac = elem
				break

		for elem in td_div:
			if td <= elem:
				td = elem
				break

		model = {}
		model['points']		= {points : 1}
		model['fumble']		= {fumble : 1}
		model['targets']	= {targets : 1}
		model['rec']		= {rec : 1}
		model['rec_yds']	= {rec_yds : 1}
		model['yac']		= {yac : 1}
		model['td']			= {td : 1}


		yield 'points', [result_points, prev_amount, model]
		yield 'points', ['total', prev_amount, model]

		yield 'fumble', [result_fumble, prev_amount, model]
		yield 'fumble', ['total', prev_amount, model]

		yield 'targets', [result_targets, prev_amount, model]
		yield 'targets', ['total', prev_amount, model]

		yield 'rec', [result_rec, prev_amount, model]
		yield 'rec', ['total', prev_amount, model]

		yield 'rec_yds', [result_rec_yds, prev_amount, model]
		yield 'rec_yds', ['total', prev_amount, model]

		yield 'yac', [result_yac, prev_amount, model]
		yield 'yac', ['total', prev_amount, model]

		yield 'td', [result_td, prev_amount, model]
		yield 'td', ['total', prev_amount, model]


	def model_reducer(self, stat, models):
		stat_model = {}

		for model in models:
			stat_amount = model[0]
			prev_amount = model[1]
			features = model[2]

			if stat_amount not in stat_model:
				stat_model[stat_amount] = {'prev2': {}, 'prev5': {}, 'season': {}, 'prevseason': {}, 'career': {}}

			for feature in features:
				if feature not in stat_model[stat_amount][prev_amount]:
					stat_model[stat_amount][prev_amount][feature] = {}
				for amount in features[feature]:
					stat_model[stat_amount][prev_amount][feature][amount] = stat_model[stat_amount][prev_amount][feature].get(amount, 0) + features[feature][amount]

		yield [stat, stat_model]

	def steps(self):
		return [self.mr(mapper=self.feature_mapper, reducer=self.model_reducer)]

if __name__ == "__main__":
    TEModel().run()