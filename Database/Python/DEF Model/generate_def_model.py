import re
from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

#Divisions used to separate the features attributing to a class
points_div		= [2.94,6.35,9.76,13.17,16.58,20.00,23.41,26.82,30.23,100]
int_div			= [-0.23,0.33,0.89,1.44,2.00,2.55,3.11,3.67,4.22,10]
fumble_div		= [-0.07,0.28,0.62,0.97,1.32,1.67,2.02,2.36,2.71,10]
td_div			= [0.20,0.40,0.60,0.80,1.00,1.20,1.40,1.60,1.80,10]
block_kick_div	= [0.10,0.20,0.30,0.40,0.50,0.60,0.70,0.80,0.90,10]
safety_div		= [0.10,0.20,0.30,0.40,0.50,0.60,0.70,0.80,0.90,10]
sack_div		= [0.14,0.69,1.25,1.80,2.35,2.91,3.46,4.01,4.57,20]
pts_allowed_div	= [8.37,11.98,15.58,19.19,22.80,26.41,30.02,33.63,37.24,100]

#Divisions and averages used as the classes of resulting stats
result_points_div		= [-5.0,-1.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,11.0,12.0,14.0,15.0,19.0,100]
result_int_div			= [0.0,1.0,2.0,4.0,10]
result_fumble_div		= [0.0,1.0,2.0,3.0,10]
result_td_div			= [0.0,1.0,10]
result_block_kick_div	= [0.0,1.0,10]
result_safety_div		= [0.0,1.0]
result_sack_div			= [0.0,1.0,2.0,3.0,4.0,5.0,20]
result_pts_allowed_div	= [0.0,10.0,13.0,17.0,20.0,23.0,24.0,27.0,31.0,37.0,100]

result_points_avg		= [-1.894,.586,1.531,2.502,3.536,4.509,5.493,6.460,7.495,8.462,9.883,11.487,12.897,14.475,16.599,22.632]
result_int_avg			= [.470,1.319,2.403,4.227]
result_fumble_avg		= [.393,1.231,2.172,3.262]
result_td_avg			= [.166,1.178]
result_block_kick_avg	= [.068,1.055]
result_safety_avg		= [.024]
result_sack_avg			= [.640,1.510,2.409,3.406,4.326,5.739]
result_pts_allowed_avg	= [6.880,11.576,15.207,18.481,21.321,23.561,25.447,28.886,33.320,42.092]

class DEFModel(MRJob):

	INPUT_PROTOCOL = JSONValueProtocol

	def feature_mapper(self, _, data):

		result_points = data['result_points']
		result_int = data['result_int']
		result_fumble = data['result_fumble']
		result_td = data['result_td']
		result_block_kick = data['result_block_kick']
		result_safety = data['result_safety']
		result_sack = data['result_sack']
		result_pts_allowed = data['result_pts_allowed']

		for index in range(0,len(result_points_avg)):
			if result_points <= result_points_div[index+1]:
				result_points = result_points_avg[index]
				break

		for index in range(0,len(result_int_avg)):
			if result_int <= result_int_div[index+1]:
				result_int = result_int_avg[index]
				break

		for index in range(0,len(result_fumble_avg)):
			if result_fumble <= result_fumble_div[index+1]:
				result_fumble = result_fumble_avg[index]
				break

		for index in range(0,len(result_td_avg)):
			if result_td <= result_td_div[index+1]:
				result_td = result_td_avg[index]
				break

		for index in range(0,len(result_block_kick_avg)):
			if result_block_kick <= result_block_kick_div[index+1]:
				result_block_kick = result_block_kick_avg[index]
				break

		for index in range(0,len(result_safety_avg)):
			if result_safety <= result_safety_div[index+1]:
				result_safety = result_safety_avg[index]
				break

		for index in range(0,len(result_sack_avg)):
			if result_sack <= result_sack_div[index+1]:
				result_sack = result_sack_avg[index]
				break

		for index in range(0,len(result_pts_allowed_avg)):
			if result_pts_allowed <= result_pts_allowed_div[index+1]:
				result_pts_allowed = result_pts_allowed_avg[index]
				break

		prev_amount = data['prev_amount']
		points = data['points']
		int = data['int']
		fumble = data['fumble']
		td = data['td']
		block_kick = data['block_kick']
		safety = data['safety']
		sack = data['sack']
		pts_allowed = data['pts_allowed']

		for elem in points_div:
			if points <= elem:
				points = elem
				break

		for elem in int_div:
			if int <= elem:
				int = elem
				break

		for elem in fumble_div:
			if fumble <= elem:
				fumble = elem
				break

		for elem in td_div:
			if td <= elem:
				td = elem
				break

		for elem in block_kick_div:
			if block_kick <= elem:
				block_kick = elem
				break

		for elem in safety_div:
			if safety <= elem:
				safety = elem
				break

		for elem in sack_div:
			if sack <= elem:
				sack = elem
				break

		for elem in pts_allowed_div:
			if pts_allowed <= elem:
				pts_allowed = elem
				break

		model = {}
		model['points']			= {points : 1}
		model['int']			= {int : 1}
		model['fumble']			= {fumble : 1}
		model['td']				= {td : 1}
		model['block_kick']		= {block_kick : 1}
		model['safety']			= {safety : 1}
		model['sack']			= {sack : 1}
		model['pts_allowed']	= {pts_allowed : 1}

		yield 'points', [result_points, prev_amount, model]
		yield 'points', ['total', prev_amount, model]

		yield 'int', [result_int, prev_amount, model]
		yield 'int', ['total', prev_amount, model]

		yield 'fumble', [result_fumble, prev_amount, model]
		yield 'fumble', ['total', prev_amount, model]

		yield 'td', [result_td, prev_amount, model]
		yield 'td', ['total', prev_amount, model]

		yield 'block_kick', [result_block_kick, prev_amount, model]
		yield 'block_kick', ['total', prev_amount, model]

		yield 'safety', [result_safety, prev_amount, model]
		yield 'safety', ['total', prev_amount, model]

		yield 'sack', [result_sack, prev_amount, model]
		yield 'sack', ['total', prev_amount, model]

		yield 'pts_allowed', [result_pts_allowed, prev_amount, model]
		yield 'pts_allowed', ['total', prev_amount, model]


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
    DEFModel().run()