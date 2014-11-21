import re
from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

points_div		=	[2.16, 6.68, 9.56, 11.5, 13.04, 14.5, 15.91, 17.53, 19.44, 100]
pass_att_div	=	[7.6, 21.2, 26.4, 28.8, 31, 32.8, 34.4, 36.4, 39, 100]
pass_cmp_div	=	[4.2, 11.8, 15.4, 17.2, 18.8, 20, 21.2, 22.6, 24.6, 100]
pass_yds_div	=	[45.3, 131.75, 178, 201.4, 216.5, 231.6, 247.6, 268, 291.4, 1000]
pass_tds_div	=	[0, .5, .8, 1, 1.2, 1.4, 1.6, 1.8, 2.2, 10]
int_div			=	[0, .33, .4, .6, .8, 1, 1.2, 1.4, 10]
rush_att_div	=	[.8, 1.2, 1.4, 1.8, 2, 2.4, 2.8, 3.4, 4.25, 100]
rush_yds_div	=	[0, .8, 2.2, 3.8, 5.6, 8, 11, 15.2, 21.8, 1000]
fumble_div		=	[0, .2, .4, 10]
td_div			=	[0, .2, 10]

class QBModel(MRJob):

	INPUT_PROTOCOL = JSONValueProtocol

	def feature_mapper(self, _, data):
		key = 'none'
		result_points = data['result_points']
		prev_amount = data['prev_amount']
		points = data['points']
		pass_att = data['pass_att']
		pass_cmp = data['pass_cmp']
		pass_yds = data['pass_yds']
		pass_tds = data['pass_tds']
		int = data['int']
		rush_att = data['rush_att']
		rush_yds = data['rush_yds']
		fumble = data['fumble']
		td = data['td']
		if result_points <= -.1:
			key = -3.47
		elif result_points <= .6:
			key = .25
		elif result_points <= 2.2:
			key = 1.4
		elif result_points <= 4.22:
			key = 3.21
		elif result_points <= 6:
			key = 5.11
		elif result_points <= 7.56:
			key = 6.78
		elif result_points <= 9.12:
			key = 8.34
		elif result_points <= 10.46:
			key = 9.79
		elif result_points <= 11.82:
			key = 11.14
		elif result_points <= 12.9:
			key = 12.36
		elif result_points <= 14.08:
			key = 13.49
		elif result_points <= 15.1:
			key = 14.59
		elif result_points <= 16.18:
			key = 15.64
		elif result_points <= 17.5:
			key = 16.84
		elif result_points <= 18.66:
			key = 18.08
		elif result_points <= 20.04:
			key = 19.35
		elif result_points <= 21.82:
			key = 20.93
		elif result_points <= 24.38:
			key = 23.1
		elif result_points <= 28.12:
			key = 26.25
		else:
			key = 32.3

		for elem in points_div:
			if points <= elem:
				points = elem
				break

		for elem in pass_att_div:
			if pass_att <= elem:
				pass_att = elem
				break

		for elem in pass_cmp_div:
			if pass_cmp <= elem:
				pass_cmp = elem
				break

		for elem in pass_yds_div:
			if pass_yds <= elem:
				pass_yds = elem
				break

		for elem in pass_tds_div:
			if pass_tds <= elem:
				pass_tds = elem
				break

		for elem in int_div:
			if int <= elem:
				int = elem
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

		for elem in td_div:
			if td <= elem:
				td = elem
				break

		model = {}
		model['points']		= {points : 1}
		model['pass_att']	= {pass_att : 1}
		model['pass_cmp']	= {pass_cmp : 1}
		model['pass_yds']	= {pass_yds : 1}
		model['pass_tds']	= {pass_tds : 1}
		model['int']		= {int : 1}
		model['rush_att']	= {rush_att : 1}
		model['rush_yds']	= {rush_yds : 1}
		model['fumble']		= {fumble : 1}
		model['td']			= {td : 1}

		yield key, [prev_amount, model]

		yield 'total', [prev_amount, model]

	def model_reducer(self, points, models):
		naive_model = {'prev2': {}, 'prev5': {}, 'season': {}, 'prevseason': {}, 'career': {}}
		for model in models:
			for feature in model[1]:
				if feature not in naive_model[model[0]]:
					naive_model[model[0]][feature] = {}
				for amount in model[1][feature]:
					naive_model[model[0]][feature][amount] = naive_model[model[0]][feature].get(amount, 0) + model[1][feature][amount]

		yield [points, naive_model]

	def steps(self):
		return [self.mr(mapper=self.feature_mapper, reducer=self.model_reducer)]

if __name__ == "__main__":
    QBModel().run()