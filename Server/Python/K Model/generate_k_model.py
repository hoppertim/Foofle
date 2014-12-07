import re
from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

#Divisions used to separate the features attributing to a class
points_div		= [0.90,2.80,4.70,6.60,8.50,10.40,12.30,14.20,16.10,50]
fg_50_div		= [0.15,0.30,0.45,0.60,0.75,0.90,1.05,1.20,1.35,10]
fg_40_div		= [0.20,0.40,0.60,0.80,1.00,1.20,1.40,1.60,1.80,10]
fg_0_div		= [0.40,0.80,1.20,1.60,2.00,2.40,2.80,3.20,3.60,10]
pat_div			= [0.60,1.20,1.80,2.40,3.00,3.60,4.20,4.80,5.40,10]
fg_miss_div		= [0.30,0.60,0.90,1.20,1.50,1.80,2.10,2.40,2.70,10]

#Divisions and averages used as the classes of resulting stats
result_points_div		= [-2.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0,13.0,15.0,50]
result_fg_50_div		= [0.0,1.0,2.0,10]
result_fg_40_div		= [0.0,1.0,2.0,3.0,10]
result_fg_0_div			= [0.0,1.0,2.0,3.0,4.0,10]
result_pat_div			= [0.0,1.0,2.0,3.0,4.0,10]
result_fg_miss_div		= [0.0,1.0,2.0,3.0,10]

result_points_avg		= [.397,1.489,2.562,3.586,4.535,5.496,6.509,7.479,8.469,9.477,10.443,11.491,12.392,14.429,17.833]
result_fg_50_avg		= [.127,1.080,2.108]
result_fg_40_avg		= [.296,1.186,2.125,3.129]
result_fg_0_avg			= [.509,1.352,2.219,3.179,4.051]
result_pat_avg			= [.689,1.545,2.419,3.349,4.507]
result_fg_miss_avg		= [.245,1.141,2.094,3.077]

class KModel(MRJob):

	INPUT_PROTOCOL = JSONValueProtocol

	def feature_mapper(self, _, data):

		result_points = data['result_points']
		result_fg_50 = data['result_fg_50']
		result_fg_40 = data['result_fg_40']
		result_fg_0 = data['result_fg_0']
		result_pat = data['result_pat']
		result_fg_miss = data['result_fg_miss']

		for index in range(0,len(result_points_avg)):
			if result_points <= result_points_div[index+1]:
				result_points = result_points_avg[index]
				break

		for index in range(0,len(result_fg_50_avg)):
			if result_fg_50 <= result_fg_50_div[index+1]:
				result_fg_50 = result_fg_50_avg[index]
				break

		for index in range(0,len(result_fg_40_avg)):
			if result_fg_40 <= result_fg_40_div[index+1]:
				result_fg_40 = result_fg_40_avg[index]
				break

		for index in range(0,len(result_fg_0_avg)):
			if result_fg_0 <= result_fg_0_div[index+1]:
				result_fg_0 = result_fg_0_avg[index]
				break

		for index in range(0,len(result_pat_avg)):
			if result_pat <= result_pat_div[index+1]:
				result_pat = result_pat_avg[index]
				break

		for index in range(0,len(result_fg_miss_avg)):
			if result_fg_miss <= result_fg_miss_div[index+1]:
				result_fg_miss = result_fg_miss_avg[index]
				break

		prev_amount = data['prev_amount']
		points = data['points']
		fg_50 = data['fg_50']
		fg_40 = data['fg_40']
		fg_0 = data['fg_0']
		pat = data['pat']
		fg_miss = data['fg_miss']

		for elem in points_div:
			if points <= elem:
				points = elem
				break

		for elem in fg_50_div:
			if fg_50 <= elem:
				fg_50 = elem
				break

		for elem in fg_40_div:
			if fg_40 <= elem:
				fg_40 = elem
				break

		for elem in fg_0_div:
			if fg_0 <= elem:
				fg_0 = elem
				break

		for elem in pat_div:
			if pat <= elem:
				pat = elem
				break

		for elem in fg_miss_div:
			if fg_miss <= elem:
				fg_miss = elem
				break

		model = {}
		model['points']		= {points : 1}
		model['fg_50']		= {fg_50 : 1}
		model['fg_40']		= {fg_40 : 1}
		model['fg_0']		= {fg_0 : 1}
		model['pat']		= {pat : 1}
		model['fg_miss']	= {fg_miss : 1}


		yield 'points', [result_points, prev_amount, model]
		yield 'points', ['total', prev_amount, model]

		yield 'fg_50', [result_fg_50, prev_amount, model]
		yield 'fg_50', ['total', prev_amount, model]

		yield 'fg_40', [result_fg_40, prev_amount, model]
		yield 'fg_40', ['total', prev_amount, model]

		yield 'fg_0', [result_fg_0, prev_amount, model]
		yield 'fg_0', ['total', prev_amount, model]

		yield 'pat', [result_pat, prev_amount, model]
		yield 'pat', ['total', prev_amount, model]

		yield 'fg_miss', [result_fg_miss, prev_amount, model]
		yield 'fg_miss', ['total', prev_amount, model]


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
    KModel().run()