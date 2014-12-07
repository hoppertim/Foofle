import re
from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

#Divisions used to separate the features attributing to a class
points_div		=	[-5.6,-1.2,3.2,7.6,12,16.4,20.8,25.2,29.6,100]#[-0.37,1.34,2.81,4.22,5.70,7.29,9.11,11.26,14.26,100],
rush_att_div	=	[-4.5,-1,2.5,6,9.5,13,16.5,20,23.5,100]#[0.07,1.06,2.05,3.45,5.29,7.52,10.45,13.87,17.35,100],
rush_yds_div	=	[-25,-3,19,41,63,85,107,129,151,500]#[-2.38,3.53,8.72,14.40,21.67,30.69,43.22,58.06,76.04,300],
fumble_div		=	[-.32,-.14,.04,.22,.4,.58,.76,.94,1.12,10]#[-0.11,-0.06,-0.02,0.00,0.03,0.06,0.10,0.16,0.26,10],
targets_div		=	[-3,-1,1,3,5,7,9,11,13,50]#[-0.41,0.29,0.79,1.26,1.70,2.22,2.83,3.55,4.63,50],
rec_div			=	[-3.9,-2.3,-.7,.9,2.5,4.1,5.7,7.3,8.9,50]#[-0.44,0.13,0.55,0.94,1.30,1.67,2.14,2.68,3.52,50],
rec_yds_div		=	[-45,-28,-11,6,23,40,57,74,91,500]#[-7.20,-1.22,3.13,6.80,10.32,14.04,18.24,23.62,31.82,500],
yac_div			=	[-21,-6,9,24,39,54,69,84,99,500]#[-3.43,0.53,3.49,6.25,8.99,12.13,15.92,20.46,28.30,500],
td_div			=	[-.6,-.2,.2,.6,1,1.4,1.8,2.2,2.6,10]#[-0.16,-0.05,0.04,0.13,0.21,0.30,0.40,0.54,0.76,10]


#Divisions and averages used as the classes of resulting stats
result_points_div		=	[-2.2,0.0,0.3,0.6,0.9,1.4,1.9,2.4,3.1,3.9,5.0,6.1,7.1,8.4,9.9,11.6,13.6,16.1,20.5,100]
result_rush_att_div		=	[0.0,1.0,3.0,5.0,7.0,10.0,14.0,19.0,100]
result_rush_yds_div		=	[-14.0,2.0,7.0,15.0,26.0,40.0,58.0,85.0,500]
result_fumble_div		=	[0.0,1.0,10]
result_targets_div		=	[0.0,1.0,2.0,3.0,4.0,5.0,50]
result_rec_div			=	[0.0,1.0,2.0,3.0,4.0,50]
result_rec_yds_div		=	[-11.0,0.0,4.0,8.0,13.0,21.0,35.0,500]
result_yac_div			=	[-17.0,0.0,4.0,8.0,13.0,20.0,33.0,500]
result_td_div			=	[0.0,1.0,2.0,3.0,4.0,10]

result_points_avg		=	[-.084,.157,.394,.752,1.193,1.699,2.146,2.741,3.491,4.424,5.600,6.626,7.768,9.184,10.748,12.458,14.788,18.076,25.800]
result_rush_att_avg		=	[.313,2.419,4.454,6.469,8.974,12.452,16.861,23.763]
result_rush_yds_avg		=	[.085,4.805,11.245,20.618,33.491,48.860,70.777,117.254]
result_fumble_avg		=	[.059,1.030]
result_targets_avg		=	[.438,1.387,2.406,3.409,4.407,7.418]
result_rec_avg			=	[.383,1.371,2.372,3.4,6.041]
result_rec_yds_avg		=	[-.149,2.727,6.546,10.879,17.216,27.329,54.670]
result_yac_avg			=	[-.025,2.576,6.448,10.841,16.805,26.213,52.066]
result_td_avg			=	[.174,1.167,2.155,3.090,4.143]

class RBModel(MRJob):

	INPUT_PROTOCOL = JSONValueProtocol

	def feature_mapper(self, _, data):

		result_points = data['result_points']
		result_rush_att = data['result_rush_att']
		result_rush_yds = data['result_rush_yds']
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

		for index in range(0,len(result_rush_att_avg)):
			if result_rush_att <= result_rush_att_div[index+1]:
				result_rush_att = result_rush_att_avg[index]
				break

		for index in range(0,len(result_rush_yds_avg)):
			if result_rush_yds <= result_rush_yds_div[index+1]:
				result_rush_yds = result_rush_yds_avg[index]
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
		rush_att = data['rush_att']
		rush_yds = data['rush_yds']
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

		for elem in rush_att_div:
			if rush_att <= elem:
				rush_att = elem
				break

		for elem in rush_yds_div:
			if rush_yds <= elem:
				rush_yds = elem
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
		model['rush_att']	= {rush_att : 1}
		model['rush_yds']	= {rush_yds : 1}
		model['fumble']		= {fumble : 1}
		model['targets']	= {targets : 1}
		model['rec']		= {rec : 1}
		model['rec_yds']	= {rec_yds : 1}
		model['yac']		= {yac : 1}
		model['td']			= {td : 1}


		yield 'points', [result_points, prev_amount, model]
		yield 'points', ['total', prev_amount, model]

		yield 'rush_att', [result_rush_att, prev_amount, model]
		yield 'rush_att', ['total', prev_amount, model]

		yield 'rush_yds', [result_rush_yds, prev_amount, model]
		yield 'rush_yds', ['total', prev_amount, model]

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
    RBModel().run()