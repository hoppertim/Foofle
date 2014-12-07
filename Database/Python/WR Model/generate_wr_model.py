import re
from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

#Divisions used to separate the features attributing to a class
points_div		=	[-5.5,-1,3.5,8,12.5,17,21.5,26,30.5,100]
rush_att_div	=	[-6.1,-4.4,-2.7,-1,.7,2.4,4.1,5.8,7.5,50]
rush_yds_div	=	[-40,-30,-20,-10,0,10,20,30,40,500]
fumble_div		=	[-.33,-.16,.01,.18,.35,.52,.69,.86,1.03,10]
targets_div		=	[-2.1,.2,2.5,4.8,7.1,9.4,11.7,14,16.3,50]
rec_div			=	[-2.8,-.9,1,2.9,4.8,6.7,8.6,10.5,12.4,50]
rec_yds_div		=	[-25,0,25,50,75,100,125,150,175,500]
yac_div			=	[-21,-6,9,24,39,54,69,84,99,500]
td_div			=	[-.65,-.3,.05,.4,.75,1.1,1.45,1.8,2.15,10]


#Divisions and averages used as the classes of resulting stats
result_points_div		=	[-2.4,0.0,0.6,1.0,1.5,1.9,2.5,3.0,3.6,4.3,5.1,6.1,7.1,8.2,9.6,11.1,13.0,15.3,19.3,100]
result_rush_att_div		=	[0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,50]
result_rush_yds_div		=	[-18.0,0.0,20.0,40.0,500]
result_fumble_div		=	[0.0,1.0,10]
result_targets_div		=	[0.0,1.0,2.0,3.0,4.0,6.0,7.0,8.0,10.0,50]
result_rec_div			=	[0.0,1.0,2.0,3.0,4.0,5.0,6.0,50]
result_rec_yds_div		=	[-22.0,0.0,2.0,11.0,19.0,28.0,39.0,51.0,68.0,92.0,500]
result_yac_div			=	[-53.0,0.0,1.0,4.0,7.0,10.0,15.0,22.0,34.0,500]
result_td_div			=	[0.0,1.0,2.0,3.0,10]

result_points_avg		=	[-.049,.359,.791,1.303,1.750,2.244,2.796,3.344,3.959,4.687,5.639,6.645,7.701,8.885,10.306,11.999,14.059,17.068,24.427]
result_rush_att_avg		=	[.081,1.136,2.193,3.308,4.385,5.333,6.000,8.000]
result_rush_yds_avg		=	[-.074,7.927,26.957,55.147]
result_fumble_avg		=	[.029,1.026]
result_targets_avg		=	[.537,1.468,2.473,3.510,5.489,6.470,7.457,9.430,12.816]
result_rec_avg			=	[.487,1.457,2.470,3.457,4.431,5.401,7.894]
result_rec_yds_avg		=	[-.039,1.544,7.378,15.324,23.905,33.896,45.351,59.560,79.075,122.889]
result_yac_avg			=	[-.120,.138,2.965,5.960,8.930,12.835,18.739,27.762,52.742]
result_td_avg			=	[.184,1.138,2.088,3.057]

class WRModel(MRJob):

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
    WRModel().run()