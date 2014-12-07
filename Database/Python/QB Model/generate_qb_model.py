import re
from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

#Divisions used to separate the features attributing to a class
points_div		=	[-5.25,-0.5,4.25,9,13.75,18.5,23.25,28,32.75,100]
pass_att_div	=	[2,8,14,20,26,32,38,44,50,100]
pass_cmp_div	=	[0,4.5,9,13.5,18,22.5,27,31.5,36,100]
pass_yds_div	=	[8,58,108,158,208,258,308,358,408,1000]
pass_tds_div	=	[0,.6,1.2,1.8,2.4,3,3.6,4.2,4.8,10]
int_div			=	[-.1,0.45,1,1.55,2.1,2.65,3.2,3.75,4.3,10]
rush_att_div	=	[-5,-3,-1,1,3,5,7,9,11,50]
rush_yds_div	=	[-35,-22,-9,4,17,30,43,56,69,300]
fumble_div		=	[-.25,0,.25,.5,.75,1,1.25,1.5,1.75,10]
td_div			=	[-.75,-.5,-.25,0,.25,.5,.75,1,1.25,1.5,10]

#Divisions and averages used as the classes of resulting stats
result_points_div		=	[-6.84,-0.1,0.58,2.2,4.22,5.98,7.58,9.1,10.46,11.76,12.9,14.04,15.04,16.12,17.44,18.62,19.98,21.76,24.16,27.94,100]
result_points_avg		=	[-1.105,.177,1.266,3.138,5.109,6.836,8.324,9.822,11.080,12.396,13.483,14.514,15.610,16.785,18.028,19.292,20.852,22.776,25.791,32.154]
result_pass_att_div		=	[0,1,5,14,19,23,25,26,28,30,31,32,34,35,36,38,40,42,44,48,100]
result_pass_att_avg		=	[.393,3.196,9.600,17.328,21.746,24.505,26.000,27.531,29.528,31.000,32.000,33.507,35.000,36.000,37.429,39.417,41.547,43.438,46.240,52.799]
result_pass_cmp_div		=	[0,2,7,10,13,14,16,17,18,19,20,21,22,23,24,25,26,28,31,60]
result_pass_cmp_avg		=	[.622,4.948,9.225,12.069,14.000,15.528,17.000,18.000,19.000,20.000,21.000,22.000,23.000,24.000,25.000,26.000,27.436,29.762,34.430]
result_pass_yds_div		=	[-7,0,24,71,115,141,162,178,192,203,217,228,240,252,264,280,298,312,335,370,800]
result_pass_yds_avg		=	[-.077,12.500,48.716,95.259,129.116,153.229,171.365,185.401,197.775,210.380,222.903,234.034,246.413,258.601,272.876,289.921,304.970,323.619,351.837,409.126]
result_pass_tds_div		=	[0,1,2,3,4,5,6,10]
result_pass_tds_avg		=	[.499,1.415,2.317,3.247, 4.160,5.258,6.2]
result_int_div			=	[0,1,2,3,10]
result_int_avg			=	[.402,1.300,2.252,4.194]
result_rush_att_div		=	[0,1,2,3,4,5,6,7,50]
result_rush_att_avg		=	[.539,1.450,2.448,3.408,4.376,5.390,6.389,9.778]
result_rush_yds_div		=	[-17,-2,-1,0,1,2,3,5,7,9,11,14,18,23,30,43,300]
result_rush_yds_avg		=	[-3.092,-1.346,-.242,.143,1.523,2.470,4.542,6.5,8.516,10.494,12.946,16.505,20.898,26.895,36.022,65.220]
result_fumble_div		=	[0,1,10]
result_fumble_avg		=	[.163,2.037]
result_td_div			=	[0,1,10]
result_td_avg			=	[.079,2.091]

class QBModel(MRJob):

	INPUT_PROTOCOL = JSONValueProtocol

	def feature_mapper(self, _, data):

		result_points = data['result_points']
		result_pass_att = data['result_pass_att']
		result_pass_cmp = data['result_pass_cmp']
		result_pass_yds = data['result_pass_yds']
		result_pass_tds = data['result_pass_tds']
		result_int = data['result_int']
		result_rush_att = data['result_rush_att']
		result_rush_yds = data['result_rush_yds']
		result_fumble = data['result_fumble']
		result_td = data['result_td']

		for index in range(0,len(result_points_avg)):
			if result_points <= result_points_div[index+1]:
				result_points = result_points_avg[index]
				break

		for index in range(0,len(result_pass_att_avg)):
			if result_pass_att <= result_pass_att_div[index+1]:
				result_pass_att = result_pass_att_avg[index]
				break

		for index in range(0,len(result_pass_cmp_avg)):
			if result_pass_cmp <= result_pass_cmp_div[index+1]:
				result_pass_cmp = result_pass_cmp_avg[index]
				break

		for index in range(0,len(result_pass_yds_avg)):
			if result_pass_yds <= result_pass_yds_div[index+1]:
				result_pass_yds = result_pass_yds_avg[index]
				break

		for index in range(0,len(result_pass_tds_avg)):
			if result_pass_tds <= result_pass_tds_div[index+1]:
				result_pass_tds = result_pass_tds_avg[index]
				break

		for index in range(0,len(result_int_avg)):
			if result_int <= result_int_div[index+1]:
				result_int = result_int_avg[index]
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

		for index in range(0,len(result_td_avg)):
			if result_td <= result_td_div[index+1]:
				result_td = result_td_avg[index]
				break

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

		yield 'points', [result_points, prev_amount, model]
		yield 'points', ['total', prev_amount, model]

		yield 'pass_att', [result_pass_att, prev_amount, model]
		yield 'pass_att', ['total', prev_amount, model]

		yield 'pass_cmp', [result_pass_cmp, prev_amount, model]
		yield 'pass_cmp', ['total', prev_amount, model]

		yield 'pass_yds', [result_pass_yds, prev_amount, model]
		yield 'pass_yds', ['total', prev_amount, model]

		yield 'pass_tds', [result_pass_tds, prev_amount, model]
		yield 'pass_tds', ['total', prev_amount, model]

		yield 'int', [result_int, prev_amount, model]
		yield 'int', ['total', prev_amount, model]

		yield 'rush_att', [result_rush_att, prev_amount, model]
		yield 'rush_att', ['total', prev_amount, model]

		yield 'rush_yds', [result_rush_yds, prev_amount, model]
		yield 'rush_yds', ['total', prev_amount, model]

		yield 'fumble', [result_fumble, prev_amount, model]
		yield 'fumble', ['total', prev_amount, model]

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
    QBModel().run()