from __future__ import division
import re
import json
import nfldb
from math import log10
from math import sqrt

import sys
sys.path.append('./QB Model')
sys.path.append('./RB Model')
sys.path.append('./WR Model')
sys.path.append('./TE Model')
sys.path.append('./K Model')
sys.path.append('./DEF Model')
import generate_qb_model
import generate_rb_model
import generate_wr_model
import generate_te_model
import generate_k_model
import generate_def_model

qb_div = {
	'prev': {
		'points'		:	[-5.25,-0.5,4.25,9,13.75,18.5,23.25,28,32.75,100],
		'pass_att'		:	[2,8,14,20,26,32,38,44,50,100],
		'pass_cmp'		:	[0,4.5,9,13.5,18,22.5,27,31.5,36,100],
		'pass_yds'		:	[8,58,108,158,208,258,308,358,408,1000],
		'pass_tds'		:	[0,.6,1.2,1.8,2.4,3,3.6,4.2,4.8,10],
		'int'			:	[-.1,0.45,1,1.55,2.1,2.65,3.2,3.75,4.3,10],
		'rush_att'		:	[-5,-3,-1,1,3,5,7,9,11,50],
		'rush_yds'		:	[-35,-22,-9,4,17,30,43,56,69,300],
		'fumble'		:	[-.25,0,.25,.5,.75,1,1.25,1.5,1.75,10],
		'td'			:	[-.75,-.5,-.25,0,.25,.5,.75,1,1.25,1.5,10]
	},
	'result': {
		'points'		:	[-1.105,.177,1.266,3.138,5.109,6.836,8.324,9.822,11.080,12.396,13.483,14.514,15.610,16.785,18.028,19.292,20.852,22.776,25.791,32.154],
		'pass_att'		:	[.393,3.196,9.600,17.328,21.746,24.505,26.000,27.531,29.528,31.000,32.000,33.507,35.000,36.000,37.429,39.417,41.547,43.438,46.240,52.799],
		'pass_cmp'		:	[.622,4.948,9.225,12.069,14.000,15.528,17.000,18.000,19.000,20.000,21.000,22.000,23.000,24.000,25.000,26.000,27.436,29.762,34.430],
		'pass_yds'		:	[-.077,12.500,48.716,95.259,129.116,153.229,171.365,185.401,197.775,210.380,222.903,234.034,246.413,258.601,272.876,289.921,304.970,323.619,351.837,409.126],
		'pass_tds'		:	[.499,1.415,2.317,3.247, 4.160,5.258,6.2],
		'int'			:	[.402,1.300,2.252,4.194],
		'rush_att'		:	[.539,1.450,2.448,3.408,4.376,5.390,6.389,9.778],
		'rush_yds'		:	[-3.092,-1.346,-.242,.143,1.523,2.470,4.542,6.5,8.516,10.494,12.946,16.505,20.898,26.895,36.022,65.220],
		'fumble'		:	[.163,2.037],
		'td'			:	[.079,2.091]
	},
	'result_div': {
		'points'		:	[-6.84,-0.1,0.58,2.2,4.22,5.98,7.58,9.1,10.46,11.76,12.9,14.04,15.04,16.12,17.44,18.62,19.98,21.76,24.16,27.94,100],
		'pass_att'		:	[0,1,5,14,19,23,25,26,28,30,31,32,34,35,36,38,40,42,44,48,100],
		'pass_cmp'		:	[0,2,7,10,13,14,16,17,18,19,20,21,22,23,24,25,26,28,31,60],
		'pass_yds'		:	[-7,0,24,71,115,141,162,178,192,203,217,228,240,252,264,280,298,312,335,370,800],
		'pass_tds'		:	[0,1,2,3,4,5,6,10],
		'int'			:	[0,1,2,3,10],
		'rush_att'		:	[0,1,2,3,4,5,6,7,50],
		'rush_yds'		:	[-17,-2,-1,0,1,2,3,5,7,9,11,14,18,23,30,43,300],
		'fumble'		:	[0,1,10],
		'td'			:	[0,1,10]
	},
	'stat_factor': {
		'points'		:	1,
		'pass_att'		:	1.5,
		'pass_cmp'		:	1.25,
		'pass_yds'		:	1.25,
		'pass_tds'		:	1,
		'int'			:	1,
		'rush_att'		:	.75,
		'rush_yds'		:	.75,
		'fumble'		:	1,
		'td'			:	1
	}
}

rb_div = {
	'prev': {
		'points'		:	[-5.6,-1.2,3.2,7.6,12,16.4,20.8,25.2,29.6,100],
		'rush_att'		:	[-4.5,-1,2.5,6,9.5,13,16.5,20,23.5,100],
		'rush_yds'		:	[-25,-3,19,41,63,85,107,129,151,500],
		'fumble'		:	[-.32,-.14,.04,.22,.4,.58,.76,.94,1.12,10],
		'targets'		:	[-3,-1,1,3,5,7,9,11,13,50],
		'rec'			:	[-3.9,-2.3,-.7,.9,2.5,4.1,5.7,7.3,8.9,50],
		'rec_yds'		:	[-45,-28,-11,6,23,40,57,74,91,500],
		'yac'			:	[-21,-6,9,24,39,54,69,84,99,500],
		'td'			:	[-.6,-.2,.2,.6,1,1.4,1.8,2.2,2.6,10]
	},
	'result': {
		'points'		:	[-.084,.157,.394,.752,1.193,1.699,2.146,2.741,3.491,4.424,5.600,6.626,7.768,9.184,10.748,12.458,14.788,18.076,25.800],
		'rush_att'		:	[.313,2.419,4.454,6.469,8.974,12.452,16.861,23.763],
		'rush_yds'		:	[.085,4.805,11.245,20.618,33.491,48.860,70.777,117.254],
		'fumble'		:	[.059,1.030],
		'targets'		:	[.438,1.387,2.406,3.409,4.407,7.418],
		'rec'			:	[.383,1.371,2.372,3.4,6.041],
		'rec_yds'		:	[-.149,2.727,6.546,10.879,17.216,27.329,54.670],
		'yac'			:	[-.025,2.576,6.448,10.841,16.805,26.213,52.066],
		'td'			:	[.174,1.167,2.155,3.090,4.143]
	},
	'result_div': {
		'points'		:	[-2.2,0.0,0.3,0.6,0.9,1.4,1.9,2.4,3.1,3.9,5.0,6.1,7.1,8.4,9.9,11.6,13.6,16.1,20.5,100],
		'rush_att'		:	[0.0,1.0,3.0,5.0,7.0,10.0,14.0,19.0,100],
		'rush_yds'		:	[-14.0,2.0,7.0,15.0,26.0,40.0,58.0,85.0,500],
		'fumble'		:	[0.0,1.0,10],
		'targets'		:	[0.0,1.0,2.0,3.0,4.0,5.0,50],
		'rec'			:	[0.0,1.0,2.0,3.0,4.0,50],
		'rec_yds'		:	[-11.0,0.0,4.0,8.0,13.0,21.0,35.0,500],
		'yac'			:	[-17.0,0.0,4.0,8.0,13.0,20.0,33.0,500],
		'td'			:	[0.0,1.0,2.0,3.0,4.0,10]
	},
	'stat_factor': {
		'points'		:	1.25,
		'rush_att'		:	2,
		'rush_yds'		:	1.5,
		'fumble'		:	.5,
		'targets'		:	.5,
		'rec'			:	.75,
		'rec_yds'		:	1,
		'yac'			:	1,
		'td'			:	1.75
	}
}

wr_div = {
	'prev': {
		'points'		:	[-5.5,-1,3.5,8,12.5,17,21.5,26,30.5,100],
		'rush_att'		:	[-6.1,-4.4,-2.7,-1,.7,2.4,4.1,5.8,7.5,50],
		'rush_yds'		:	[-40,-30,-20,-10,0,10,20,30,40,500],
		'fumble'		:	[-.33,-.16,.01,.18,.35,.52,.69,.86,1.03,10],
		'targets'		:	[-2.1,.2,2.5,4.8,7.1,9.4,11.7,14,16.3,50],
		'rec'			:	[-2.8,-.9,1,2.9,4.8,6.7,8.6,10.5,12.4,50],
		'rec_yds'		:	[-25,0,25,50,75,100,125,150,175,500],
		'yac'			:	[-21,-6,9,24,39,54,69,84,99,500],
		'td'			:	[-.65,-.3,.05,.4,.75,1.1,1.45,1.8,2.15,10]
	},
	'result': {
		'points'		:	[-.049,.359,.791,1.303,1.750,2.244,2.796,3.344,3.959,4.687,5.639,6.645,7.701,8.885,10.306,11.999,14.059,17.068,24.427],
		'rush_att'		:	[.081,1.136,2.193,3.308,4.385,5.333,6.000,8.000],
		'rush_yds'		:	[-.074,7.927,26.957,55.147],
		'fumble'		:	[.029,1.026],
		'targets'		:	[.537,1.468,2.473,3.510,5.489,6.470,7.457,9.430,12.816],
		'rec'			:	[.487,1.457,2.470,3.457,4.431,5.401,7.894],
		'rec_yds'		:	[-.039,1.544,7.378,15.324,23.905,33.896,45.351,59.560,79.075,122.889],
		'yac'			:	[-.120,.138,2.965,5.960,8.930,12.835,18.739,27.762,52.742],
		'td'			:	[.184,1.138,2.088,3.057]
	},
	'result_div': {
		'points'		:	[-2.4,0.0,0.6,1.0,1.5,1.9,2.5,3.0,3.6,4.3,5.1,6.1,7.1,8.2,9.6,11.1,13.0,15.3,19.3,100],
		'rush_att'		:	[0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,50],
		'rush_yds'		:	[-18.0,0.0,20.0,40.0,500],
		'fumble'		:	[0.0,1.0,10],
		'targets'		:	[0.0,1.0,2.0,3.0,4.0,6.0,7.0,8.0,10.0,50],
		'rec'			:	[0.0,1.0,2.0,3.0,4.0,5.0,6.0,50],
		'rec_yds'		:	[-22.0,0.0,2.0,11.0,19.0,28.0,39.0,51.0,68.0,92.0,500],
		'yac'			:	[-53.0,0.0,1.0,4.0,7.0,10.0,15.0,22.0,34.0,500],
		'td'			:	[0.0,1.0,2.0,3.0,10]
	},
	'stat_factor': {
		'points'		:	1,
		'rush_att'		:	.75,
		'rush_yds'		:	.75,
		'fumble'		:	.75,
		'targets'		:	1.25,
		'rec'			:	1.25,
		'rec_yds'		:	1.25,
		'yac'			:	1.25,
		'td'			:	1.25
	}
}

te_div = {
	'prev': {
		'points'		:	[-5.90,-2.07,1.75,5.57,9.39,13.22,17.04,20.86,24.68,100],
		'fumble'		:	[-0.25,0.00,0.24,0.49,0.74,0.99,1.24,1.49,1.73,10],
		'targets'		:	[-3.25,-1.29,0.67,2.63,4.59,6.55,8.51,10.47,12.43,50],
		'rec'			:	[-3.94,-2.42,-0.91,0.60,2.12,3.63,5.14,6.66,8.17,50],
		'rec_yds'		:	[-26.64,-8.28,10.07,28.42,46.77,65.13,83.48,101.83,120.19,500],
		'yac'			:	[-20.04,-10.51,-0.98,8.55,18.08,27.61,37.15,46.68,56.21,500],
		'td'			:	[-0.65,-0.32,0.00,0.33,0.66,0.98,1.31,1.64,1.96,10]
	},
	'result': {
		'points'		:	[-.021,.224,.566,.848,1.059,1.348,1.744,2.149,2.605,3.225,4.101,5.057,6.251,7.514,9.255,11.640,17.455],
		'fumble'		:	[.016,1.021],
		'targets'		:	[.675,1.400,2.433,3.422,4.491,5.453,7.425,10.439],
		'rec'			:	[.533,1.378,2.453,3.413,4.410,7.192],
		'rec_yds'		:	[-.032,3.222,7.840,13.374,20.322,28.849,39.780,55.043,88.350],
		'yac'			:	[-.044,.129,2.500,4.945,7.942,11.292,16.390,23.530,42.266],
		'td'			:	[.163,1.099,2.118]
	},
	'result_div': {
		'points'		:	[-3.0,0.0,0.4,0.7,0.9,1.2,1.5,1.9,2.4,2.9,3.6,4.5,5.6,6.9,8.3,10.3,13.3,100],
		'fumble'		:	[0.0,1.0,10],
		'targets'		:	[0.0,1.0,2.0,3.0,4.0,5.0,6.0,8.0,50],
		'rec'			:	[0.0,1.0,2.0,3.0,4.0,5.0,50],
		'rec_yds'		:	[-5.0,0.0,5.0,10.0,16.0,24.0,33.0,46.0,65.0,500],
		'yac'			:	[-8.0,0.0,1.0,3.0,6.0,9.0,13.0,19.0,28.0,500],
		'td'			:	[0.0,1.0,2.0,10]
	},
	'stat_factor': {
		'points'		:	1,
		'fumble'		:	.75,
		'targets'		:	1.25,
		'rec'			:	1.25,
		'rec_yds'		:	1,
		'yac'			:	1,
		'td'			:	.75
	}
}

k_div = {
	'prev': {
		'points'	: [0.90,2.80,4.70,6.60,8.50,10.40,12.30,14.20,16.10,50],
		'fg_50'		: [0.15,0.30,0.45,0.60,0.75,0.90,1.05,1.20,1.35,10],
		'fg_40'		: [0.20,0.40,0.60,0.80,1.00,1.20,1.40,1.60,1.80,10],
		'fg_0'		: [0.40,0.80,1.20,1.60,2.00,2.40,2.80,3.20,3.60,10],
		'pat'		: [0.60,1.20,1.80,2.40,3.00,3.60,4.20,4.80,5.40,10],
		'fg_miss'	: [0.30,0.60,0.90,1.20,1.50,1.80,2.10,2.40,2.70,10]
	},
	'result': {
		'points'	: [.397,1.489,2.562,3.586,4.535,5.496,6.509,7.479,8.469,9.477,10.443,11.491,12.392,14.429,17.833],
		'fg_50'		: [.127,1.080,2.108],
		'fg_40'		: [.296,1.186,2.125,3.129],
		'fg_0'		: [.509,1.352,2.219,3.179,4.051],
		'pat'		: [.689,1.545,2.419,3.349,4.507],
		'fg_miss'	: [.245,1.141,2.094,3.077]
	},
	'result_div': {
		'points'	: [-2.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0,13.0,15.0,50],
		'fg_50'		: [0.0,1.0,2.0,10],
		'fg_40'		: [0.0,1.0,2.0,3.0,10],
		'fg_0'		: [0.0,1.0,2.0,3.0,4.0,10],
		'pat'		: [0.0,1.0,2.0,3.0,4.0,10],
		'fg_miss'	: [0.0,1.0,2.0,3.0,10],
	},
	'stat_factor': {
		'points'	:1,
		'fg_50'		:1,
		'fg_40'		:1,
		'fg_0'		:1,
		'pat'		:1,
		'fg_miss'	:1
	}
}

def_div = {
	'prev': {
		'points'		: [2.94,6.35,9.76,13.17,16.58,20.00,23.41,26.82,30.23,100],
		'int'			: [-0.23,0.33,0.89,1.44,2.00,2.55,3.11,3.67,4.22,10],
		'fumble'		: [-0.07,0.28,0.62,0.97,1.32,1.67,2.02,2.36,2.71,10],
		'td'			: [0.20,0.40,0.60,0.80,1.00,1.20,1.40,1.60,1.80,10],
		'block_kick'	: [0.10,0.20,0.30,0.40,0.50,0.60,0.70,0.80,0.90,10],
		'safety'		: [0.10,0.20,0.30,0.40,0.50,0.60,0.70,0.80,0.90,10],
		'sack'			: [0.14,0.69,1.25,1.80,2.35,2.91,3.46,4.01,4.57,20],
		'pts_allowed'	: [8.37,11.98,15.58,19.19,22.80,26.41,30.02,33.63,37.24,100]
	},
	'result': {
		'points'		: [-1.894,.586,1.531,2.502,3.536,4.509,5.493,6.460,7.495,8.462,9.883,11.487,12.897,14.475,16.599,22.632],
		'int'			: [.470,1.319,2.403,4.227],
		'fumble'		: [.393,1.231,2.172,3.262],
		'td'			: [.166,1.178],
		'block_kick'	: [.068,1.055],
		'safety'		: [.024],
		'sack'			: [.640,1.510,2.409,3.406,4.326,5.739],
		'pts_allowed'	: [6.880,11.576,15.207,18.481,21.321,23.561,25.447,28.886,33.320,42.092]
	},
	'result_div': {
		'points'		: [-5.0,-1.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,11.0,12.0,14.0,15.0,19.0,100],
		'int'			: [0.0,1.0,2.0,4.0,10],
		'fumble'		: [0.0,1.0,2.0,3.0,10],
		'td'			: [0.0,1.0,10],
		'block_kick'	: [0.0,1.0,10],
		'safety'		: [0.0,1.0],
		'sack'			: [0.0,1.0,2.0,3.0,4.0,5.0,20],
		'pts_allowed'	: [0.0,10.0,13.0,17.0,20.0,23.0,24.0,27.0,31.0,37.0,100]
	},
	'stat_factor': {
		'points'		: 1,
		'int'			: 1.25,
		'fumble'		: 1.25,
		'td'			: .75,
		'block_kick'	: .5,
		'safety'		: .25,
		'sack'			: 1.25,
		'pts_allowed'	: 1.5
	}
}

prev_weights = {'prev2': .25, 'prev5': .2, 'season': .4, 'prevseason': .15, 'career': .1}

_db = nfldb.connect('nfldb', 'nfldb', 'TDHaug92', 'localhost', '5432', 'US/central')

class Predictor:

	#For the prediction to work, there must always be a valid player_id or team_id
	#If the player_id is supplied then the prediction will be made for that player
	#If the team_id is supplied then the prediction will be made for that team's defense
	#If a gsis_id is supplied then the prediction will be made for that game
	#If a gsis_id is not supplied then the prediction will be made for the next game for the player/team	
	def predict(self, player_id = '', team_id = '', gsis_id = ''):
		#Calculate for the player
		if player_id:
			with nfldb.Tx(_db) as c:
				c.execute('''
					SELECT * FROM prev_games('%s', '%s', '')
					''' %(player_id, gsis_id))
				rows = c.fetchall()

				#Return 0 if the player_id is not correct
				if len(rows) == 0:
					return 0
				elif gsis_id == '':
					gsis_id = rows[0]['gsis_id']
			
			if rows[0]['position'].name == 'QB':
				return self._QB_predict(rows, player_id, gsis_id)
			elif rows[0]['position'].name == 'RB':
				return self._RB_predict(rows, player_id, gsis_id)
			elif rows[0]['position'].name == 'WR':
				return self._WR_predict(rows, player_id, gsis_id)
			elif rows[0]['position'].name == 'TE':
				return self._TE_predict(rows, player_id, gsis_id)
			elif rows[0]['position'].name == 'K':
				return self._K_predict(rows, player_id, gsis_id)
		#Calculate for the team's defense
		elif team_id:
			with nfldb.Tx(_db) as c:
				c.execute('''
					SELECT
						fp.gsis_id,
						fp.prev_amount,
						fp.points,
						fp.int,
						fp.fumble,
						fp.td,
						fp.block_kick,
						fp.safety,
						fp.sack,
						fp.pts_allowed
					FROM prev_games('', '%s', '%s') as fp
					''' %(gsis_id, team_id))
				rows = c.fetchall()

				#Return 0 if the team_id is not correct
				if len(rows) == 0:
					return 0
				elif gsis_id == '':
					gsis_id = rows[0]['gsis_id']

			return self._DEF_predict(rows, team_id, gsis_id)

		#Return zero points player and team are not valid
		return 0

	#Function used to predict the performance of QB's
	def _QB_predict(self, prev, player_id, gsis_id):
		#File name of the naive bayes model for QB's
		file_name = './QB Model/qb_naive.json'

		#Chance of the game belonging to the points category
		prediction_model = {}
		smoothing = {}

		#Initialize prediction model
		for stat in qb_div['result']:
			prediction_model[stat] = {}
			smoothing[stat] = len(qb_div['result'][stat])
			for value in qb_div['result'][stat]:
				prediction_model[stat][value] = 1

		#Execute query to get the QB's previous games
		#The performance for each game is adjusted based on the opponent to adjust for hard/weak games
		#Ex: if opponent is good against pass_yds then pass_yds increased, or if weak against rush_yds then rush_yds decreased
		rows = []
		with nfldb.Tx(_db) as c:
			c.execute('''
				SELECT 
					fantasy.pass_att - sr1.def_pass_att * sr2.def_pass_att as pass_att,
					fantasy.pass_cmp - sr1.def_pass_cmp * sr2.def_pass_cmp as pass_cmp,
					fantasy.pass_yds - sr1.def_pass_yds * sr2.def_pass_yds as pass_yds,
					fantasy.pass_tds - sr1.def_pass_tds * sr2.def_pass_tds as pass_tds,
					fantasy.int - sr1.def_int * sr2.def_int as int,
					fantasy.rush_att - sr1.def_rush_att * sr2.def_rush_att as rush_att,
					fantasy.rush_yds - sr1.def_rush_yds * sr2.def_rush_yds as rush_yds,
					fantasy.fumble - sr1.def_fumble * sr2.def_fumble as fumble,
					fantasy.td - sr1.def_rush_tds * sr2.def_rush_tds - sr1.def_rec_tds * sr2.def_rec_tds as td,
					fantasy.points - (sr1.def_pass_yds * sr2.def_pass_yds) / 25.0 - (sr1.def_pass_tds * sr2.def_pass_tds) * 4.0 + (sr1.def_int * sr2.def_int) * 2.0 - (sr1.def_rush_yds * sr2.def_rush_yds) / 10.0 + (sr1.def_fumble * sr2.def_fumble) * 2.0 - (sr1.def_rush_tds * sr2.def_rush_tds - sr1.def_rec_tds * sr2.def_rec_tds) * 6.0 as points
				FROM public.fantasy
					JOIN public.game as g on fantasy.gsis_id = g.gsis_id
					JOIN public.season_rankings as sr1
						ON sr1.season_year = g.season_year
							AND sr1.team_id = case when g.away_team = fantasy.team_id then g.home_team else g.away_team end
							AND sr1.avg = 'f'
					JOIN public.season_rankings as sr2
						ON sr2.season_year = g.season_year
							AND sr2.team_id = 'UNK'
							AND sr2.avg = 'f'
				WHERE fantasy.player_id = '%s'
					AND fantasy.gsis_id < '%s'
				''' %(player_id, gsis_id))
			rows = c.fetchall()

		#Determine the base percentage of the likelihood of each class
		for row in rows:
			for stat in qb_div['result']:
				amount = row[stat]

				#Round amount to nearest class
				for index in range(0, len(qb_div['result'][stat])):
					if amount <= qb_div['result_div'][stat][index+1]:
						amount = qb_div['result'][stat][index]
						break

				if amount in prediction_model[stat]:
					prediction_model[stat][amount] += 1

		for stat in prediction_model:
			for amount in prediction_model[stat]:
				prediction_model[stat][amount] = .3*log10(prediction_model[stat][amount] / (len(rows) + smoothing[stat]))

		#Load the naive bayes QB model from file
		f = open(file_name, 'r')
		job = generate_qb_model.QBModel()
		QBModel = {}
		for line in f:
			stat_type, model = job.parse_output_line(line)
			QBModel[stat_type] = model

		#Loop through each previous average
		for prev_avg in prev:
			prev_amount = prev_avg['prev_amount']

			#Loop through each stat of the previous average
			for stat_type in qb_div['prev']:
				#Get the value of the stat
				feature = prev_avg[stat_type]
				weighting_factor = prev_weights[prev_amount] * qb_div['stat_factor'][stat_type]

				#Round feature to nearest class
				for feature_class in qb_div['prev'][stat_type]:
					if feature <= feature_class:
						feature = feature_class
						break

				#Get the chance for each class based on previous stat
				for result_stat in qb_div['result']:
					for result_class in qb_div['result'][result_stat]:
						if str(result_class) not in QBModel[result_stat] or prev_amount not in QBModel[result_stat][str(result_class)] or stat_type not in QBModel[result_stat][str(result_class)][prev_amount]:
							chance = 1
						else:
							chance = QBModel[result_stat][str(result_class)][prev_amount][stat_type].get(str(feature), 0) + 1
						if prev_amount not in QBModel[result_stat]['total'] or stat_type not in QBModel[result_stat]['total'][prev_amount]:
							total_chance = smoothing[result_stat]
						else:
							total_chance = QBModel[result_stat]['total'][prev_amount][stat_type].get(str(feature), 0) + smoothing[result_stat]
						prediction_model[result_stat][result_class] += weighting_factor * log10(chance / total_chance)

		#Prediction for each stat has been calculated
		#Now calculated predicted value for each stat based on chances of each stat occuring
		estimate_model = {}
		for stat_type in prediction_model:
			estimate_model[stat_type] = 0

			estimate_array = [[key, prediction_model[stat_type][key]] for key in prediction_model[stat_type]]
			estimate_array.sort(lambda x,y: cmp(y[1], x[1]))
			highest = estimate_array[0][1]
			for pair in estimate_array:
				pair[1] -= highest + 1
				pair[1] = pow(10, pair[1])

			self._Normalize_Chances(estimate_array)

			for pair in estimate_array:
				estimate_model[stat_type] += pair[0] * pair[1]


		with nfldb.Tx(_db) as c:
			c.execute('''
				select sr.def_pass_yds as pass_yds
					, sr.def_pass_tds as pass_tds
					, sr.def_rush_yds as rush_yds
					, sr.def_rush_tds as td
					, sr.def_int as int
					, sr.def_fumble as fumble
				from public.player as p
					join public.game as g on p.team in (g.home_team, g.away_team)
					join public.season_rankings as sr
						on sr.season_year = g.season_year
							and 
							(
								sr.team_id = case when g.away_team = p.team then g.home_team else g.away_team end
								or sr.team_id = 'UNK'
							)
				where p.player_id = '%s'
					and g.gsis_id = '%s'
					and sr.avg = 'f'
				order by sr.team_id;
				''' %(player_id, gsis_id))
			opponent = c.fetchone()
			stddev = c.fetchone()

			#Bias the predicted stats based on the opponent
			for stat_type in opponent:
				estimate_model[stat_type] += opponent[stat_type] * stddev[stat_type]

		#Bias the predicted points based on the opponent
		estimate_model['points'] += opponent['pass_yds'] * stddev['pass_yds'] / 25 + opponent['pass_tds'] * stddev['pass_tds'] * 4 - opponent['int'] * stddev['int'] * 2 + opponent['rush_yds'] * stddev['rush_yds'] / 10 - opponent['fumble'] * stddev['fumble'] * 2 + opponent['td'] * stddev['td'] * 6

		#Predict the fantasy points based on the predicted stats of the player
		estimate_model['calc_points'] = estimate_model['pass_yds'] / 25 + estimate_model['pass_tds'] * 4 - estimate_model['int'] * 2 + estimate_model['rush_yds'] / 10 - estimate_model['fumble'] * 2 + estimate_model['td'] * 6

		prev_points = 0
		for row in prev:
			prev_amount = row['prev_amount']
			prev_points += row['points'] * prev_weights[prev_amount]

		return .55*estimate_model['points'] + .2*estimate_model['calc_points'] + .25 * (prev_points / 1.1)

	#Function used to predict the performance of RB's
	def _RB_predict(self, prev, player_id, gsis_id):
		#File name of the naive bayes model for RB's
		file_name = './RB Model/rb_naive.json'

		#Chance of the game belonging to the points category
		prediction_model = {}
		smoothing = {}

		#Initialize prediction model
		for stat in rb_div['result']:
			prediction_model[stat] = {}
			smoothing[stat] = len(rb_div['result'][stat])
			for value in rb_div['result'][stat]:
				prediction_model[stat][value] = 1

		#Execute query to get the RB's previous games
		#The performance for each game is adjusted based on the opponent to adjust for hard/weak games
		#Ex: if opponent is good against pass_yds then pass_yds increased, or if weak against rush_yds then rush_yds decreased
		rows = []
		with nfldb.Tx(_db) as c:
			c.execute('''
				SELECT 
					fantasy.rush_att - sr1.def_rush_att * sr2.def_rush_att as rush_att,
					fantasy.rush_yds - sr1.def_rush_yds * sr2.def_rush_yds as rush_yds,
					fantasy.fumble - sr1.def_fumble * sr2.def_fumble as fumble,
					fantasy.targets - sr1.def_targets * sr2.def_targets as targets,
					fantasy.rec - sr1.def_rec * sr2.def_rec as rec,
					fantasy.rec_yds - sr1.def_rec_yds * sr2.def_rec_yds as rec_yds,
					fantasy.yac - sr1.def_yac * sr2.def_yac as yac,
					fantasy.td - sr1.def_rush_tds * sr2.def_rush_tds - sr1.def_rec_tds * sr2.def_rec_tds * .2 as td,
					fantasy.points - (sr1.def_rush_yds * sr2.def_rush_yds) / 10.0 - (sr1.def_rec_yds * sr2.def_rec_yds) / 10.0 + (sr1.def_fumble * sr2.def_fumble) * 2.0 - ((sr1.def_rush_tds * sr2.def_rush_tds) * 2.0 + (sr1.def_rec_tds * sr2.def_rec_tds) * .5) * 6.0 as points
				FROM public.fantasy
					JOIN public.game as g on fantasy.gsis_id = g.gsis_id
					JOIN public.season_rankings as sr1
						ON sr1.season_year = g.season_year
							AND sr1.team_id = case when g.away_team = fantasy.team_id then g.home_team else g.away_team end
							AND sr1.avg = 'f'
					JOIN public.season_rankings as sr2
						ON sr2.season_year = g.season_year
							AND sr2.team_id = 'UNK'
							AND sr2.avg = 'f'
				WHERE fantasy.player_id = '%s'
					AND fantasy.gsis_id < '%s'
				''' %(player_id, gsis_id))
			rows = c.fetchall()

		#Determine the base percentage of the likelihood of each class
		for row in rows:
			for stat in rb_div['result']:
				amount = row[stat]

				#Round amount to nearest class
				for index in range(0, len(rb_div['result'][stat])):
					if amount <= rb_div['result_div'][stat][index+1]:
						amount = rb_div['result'][stat][index]
						break

				if amount in prediction_model[stat]:
					prediction_model[stat][amount] += 1

		for stat in prediction_model:
			for amount in prediction_model[stat]:
				prediction_model[stat][amount] = .3*log10(prediction_model[stat][amount] / (len(rows) + smoothing[stat]))

		#Load the naive bayes RB model from file
		f = open(file_name, 'r')
		job = generate_rb_model.RBModel()
		RBModel = {}
		for line in f:
			stat_type, model = job.parse_output_line(line)
			RBModel[stat_type] = model

		#Loop through each previous average
		for prev_avg in prev:
			prev_amount = prev_avg['prev_amount']

			#Loop through each stat of the previous average
			for stat_type in rb_div['prev']:
				#Get the value of the stat
				feature = prev_avg[stat_type]
				weighting_factor = prev_weights[prev_amount] * rb_div['stat_factor'][stat_type]

				#Round feature to nearest class
				for feature_class in rb_div['prev'][stat_type]:
					if feature <= feature_class:
						feature = feature_class
						break

				#Get the chance for 
				for result_stat in rb_div['result']:
					for result_class in rb_div['result'][result_stat]:
						if str(result_class) not in RBModel[result_stat] or prev_amount not in RBModel[result_stat][str(result_class)] or stat_type not in RBModel[result_stat][str(result_class)][prev_amount]:
							chance = 1
						else:
							chance = RBModel[result_stat][str(result_class)][prev_amount][stat_type].get(str(feature), 0) + 1
						if prev_amount not in RBModel[result_stat]['total'] or stat_type not in RBModel[result_stat]['total'][prev_amount]:
							total_chance = smoothing[result_stat]
						else:
							total_chance = RBModel[result_stat]['total'][prev_amount][stat_type].get(str(feature), 0) + smoothing[result_stat]
						prediction_model[result_stat][result_class] += weighting_factor * log10(chance / total_chance)

		#Prediction for each stat has been calculated
		#Now calculated predicted value for each stat based on chances of each stat occuring
		estimate_model = {}
		for stat_type in prediction_model:
			estimate_model[stat_type] = 0

			estimate_array = [[key, prediction_model[stat_type][key]] for key in prediction_model[stat_type]]
			estimate_array.sort(lambda x,y: cmp(y[1], x[1]))
			highest = estimate_array[0][1]
			for pair in estimate_array:
				pair[1] -= highest + 1
				pair[1] = pow(10, pair[1])

			self._Normalize_Chances(estimate_array)

			for pair in estimate_array:
				estimate_model[stat_type] += pair[0] * pair[1]


		with nfldb.Tx(_db) as c:
			c.execute('''
				select sr.def_rush_yds as rush_yds
					, sr.def_rec_yds as rec_yds
					, (sr.def_rush_tds + sr.def_rec_tds * .2) as td
					, sr.def_fumble as fumble
				from public.player as p
					join public.game as g on p.team in (g.home_team, g.away_team)
					join public.season_rankings as sr
						on sr.season_year = g.season_year
							and 
							(
								sr.team_id = case when g.away_team = p.team then g.home_team else g.away_team end
								or sr.team_id = 'UNK'
							)
				where p.player_id = '%s'
					and g.gsis_id = '%s'
					and sr.avg = 'f'
				order by sr.team_id;
				''' %(player_id, gsis_id))
			opponent = c.fetchone()
			stddev = c.fetchone()

			#Bias the predicted stats based on the opponent
			for stat_type in opponent:
				estimate_model[stat_type] += opponent[stat_type] * stddev[stat_type]

		#Bias the predicted points based on the opponent
		estimate_model['points'] += opponent['rush_yds'] * stddev['rush_yds'] / 10 + opponent['rec_yds'] * stddev['rec_yds'] / 10 - opponent['fumble'] * stddev['fumble'] * 2 + opponent['td'] * stddev['td'] * 6

		#Predict the fantasy points based on the predicted stats of the player
		estimate_model['calc_points'] = estimate_model['rush_yds'] / 10.0 + estimate_model['rec_yds'] / 10.0 + estimate_model['td'] * 6.0 - estimate_model['fumble'] * 2.0


		prev_points = 0
		for row in prev:
			prev_amount = row['prev_amount']
			prev_points += row['points'] * prev_weights[prev_amount]

		prediction = .2*estimate_model['points'] + .4*estimate_model['calc_points'] + .4 * (prev_points / 1.1)

		if prediction < 0:
			prediction /= 3
		return prediction

	#Function used to predict the performance of WR's
	def _WR_predict(self, prev, player_id, gsis_id):
		#File name of the naive bayes model for RB's
		file_name = './WR Model/wr_naive.json'

		#Chance of the game belonging to the points category
		prediction_model = {}
		smoothing = {}

		#Initialize prediction model
		for stat in wr_div['result']:
			prediction_model[stat] = {}
			smoothing[stat] = len(wr_div['result'][stat])
			for value in wr_div['result'][stat]:
				prediction_model[stat][value] = 1

		#Execute query to get the WR's previous games
		#The performance for each game is adjusted based on the opponent to adjust for hard/weak games
		#Ex: if opponent is good against pass_yds then pass_yds increased, or if weak against rush_yds then rush_yds decreased
		rows = []
		with nfldb.Tx(_db) as c:
			c.execute('''
				SELECT 
					fantasy.rush_att - sr1.def_rush_att * sr2.def_rush_att * .2 as rush_att,
					fantasy.rush_yds - sr1.def_rush_yds * sr2.def_rush_yds * .2 as rush_yds,
					fantasy.fumble - sr1.def_fumble * sr2.def_fumble as fumble,
					fantasy.targets - sr1.def_targets * sr2.def_targets as targets,
					fantasy.rec - sr1.def_rec * sr2.def_rec as rec,
					fantasy.rec_yds - sr1.def_rec_yds * sr2.def_rec_yds as rec_yds,
					fantasy.yac - sr1.def_yac * sr2.def_yac as yac,
					fantasy.td - sr1.def_rush_tds * sr2.def_rush_tds * .2 - sr1.def_rec_tds * sr2.def_rec_tds as td,
					fantasy.points - (sr1.def_rush_yds * sr2.def_rush_yds) / 10.0 - (sr1.def_rec_yds * sr2.def_rec_yds) / 10.0 + (sr1.def_fumble * sr2.def_fumble) * 2.0 - ((sr1.def_rush_tds * sr2.def_rush_tds) * .1 + (sr1.def_rec_tds * sr2.def_rec_tds)) * 6.0 as points
				FROM public.fantasy
					JOIN public.game as g on fantasy.gsis_id = g.gsis_id
					JOIN public.season_rankings as sr1
						ON sr1.season_year = g.season_year
							AND sr1.team_id = case when g.away_team = fantasy.team_id then g.home_team else g.away_team end
							AND sr1.avg = 'f'
					JOIN public.season_rankings as sr2
						ON sr2.season_year = g.season_year
							AND sr2.team_id = 'UNK'
							AND sr2.avg = 'f'
				WHERE fantasy.player_id = '%s'
					AND fantasy.gsis_id < '%s'
				''' %(player_id, gsis_id))
			rows = c.fetchall()

		#Determine the base percentage of the likelihood of each class
		for row in rows:
			for stat in wr_div['result']:
				amount = row[stat]

				#Round amount to nearest class
				for index in range(0, len(wr_div['result'][stat])):
					if amount <= wr_div['result_div'][stat][index+1]:
						amount = wr_div['result'][stat][index]
						break

				if amount in prediction_model[stat]:
					prediction_model[stat][amount] += 1

		for stat in prediction_model:
			for amount in prediction_model[stat]:
				prediction_model[stat][amount] = .3*log10(prediction_model[stat][amount] / (len(rows) + smoothing[stat]))

		#Load the naive bayes RB model from file
		f = open(file_name, 'r')
		job = generate_wr_model.WRModel()
		WRModel = {}
		for line in f:
			stat_type, model = job.parse_output_line(line)
			WRModel[stat_type] = model

		#Loop through each previous average
		for prev_avg in prev:
			prev_amount = prev_avg['prev_amount']

			#Loop through each stat of the previous average
			for stat_type in wr_div['prev']:
				#Get the value of the stat
				feature = prev_avg[stat_type]
				weighting_factor = prev_weights[prev_amount] * wr_div['stat_factor'][stat_type]

				#Round feature to nearest class
				for feature_class in wr_div['prev'][stat_type]:
					if feature <= feature_class:
						feature = feature_class
						break

				#Get the chance for 
				for result_stat in wr_div['result']:
					for result_class in wr_div['result'][result_stat]:
						if str(result_class) not in WRModel[result_stat] or prev_amount not in WRModel[result_stat][str(result_class)] or stat_type not in WRModel[result_stat][str(result_class)][prev_amount]:
							chance = 1
						else:
							chance = WRModel[result_stat][str(result_class)][prev_amount][stat_type].get(str(feature), 0) + 1
						if prev_amount not in WRModel[result_stat]['total'] or stat_type not in WRModel[result_stat]['total'][prev_amount]:
							total_chance = smoothing[result_stat]
						else:
							total_chance = WRModel[result_stat]['total'][prev_amount][stat_type].get(str(feature), 0) + smoothing[result_stat]
						prediction_model[result_stat][result_class] += weighting_factor * log10(chance / total_chance)

		#Prediction for each stat has been calculated
		#Now calculated predicted value for each stat based on chances of each stat occuring
		estimate_model = {}
		for stat_type in prediction_model:
			estimate_model[stat_type] = 0

			estimate_array = [[key, prediction_model[stat_type][key]] for key in prediction_model[stat_type]]
			estimate_array.sort(lambda x,y: cmp(y[1], x[1]))
			highest = estimate_array[0][1]
			for pair in estimate_array:
				pair[1] -= highest + 1
				pair[1] = pow(10, pair[1])

			self._Normalize_Chances(estimate_array)

			for pair in estimate_array:
				estimate_model[stat_type] += pair[0] * pair[1]


		with nfldb.Tx(_db) as c:
			c.execute('''
				select sr.def_rush_yds *.2 as rush_yds
					, sr.def_rec_yds as rec_yds
					, (sr.def_rush_tds * .2 + sr.def_rec_tds) as td
					, sr.def_fumble as fumble
				from public.player as p
					join public.game as g on p.team in (g.home_team, g.away_team)
					join public.season_rankings as sr
						on sr.season_year = g.season_year
							and 
							(
								sr.team_id = case when g.away_team = p.team then g.home_team else g.away_team end
								or sr.team_id = 'UNK'
							)
				where p.player_id = '%s'
					and g.gsis_id = '%s'
					and sr.avg = 'f'
				order by sr.team_id;
				''' %(player_id, gsis_id))
			opponent = c.fetchone()
			stddev = c.fetchone()

			#Bias the predicted stats based on the opponent
			for stat_type in opponent:
				estimate_model[stat_type] += opponent[stat_type] * stddev[stat_type]

		#Bias the predicted points based on the opponent
		estimate_model['points'] += opponent['rush_yds'] * stddev['rush_yds'] / 10 + opponent['rec_yds'] * stddev['rec_yds'] / 10 - opponent['fumble'] * stddev['fumble'] * 2 + opponent['td'] * stddev['td'] * 6

		#Predict the fantasy points based on the predicted stats of the player
		estimate_model['calc_points'] = estimate_model['rush_yds'] / 10.0 + estimate_model['rec_yds'] / 10.0 + estimate_model['td'] * 6.0 - estimate_model['fumble'] * 2.0

		prev_points = 0
		for row in prev:
			prev_amount = row['prev_amount']
			prev_points += row['points'] * prev_weights[prev_amount]

		prediction = .2*estimate_model['points'] + .4*estimate_model['calc_points'] + .4 * (prev_points / 1.1)
		if prediction < 0:
			prediction /= 3
		return prediction

	#Function used to predict the performance of TE's
	def _TE_predict(self, prev, player_id, gsis_id):
		#File name of the naive bayes model for RB's
		file_name = './TE Model/te_naive.json'

		#Chance of the game belonging to the points category
		prediction_model = {}
		smoothing = {}

		#Initialize prediction model
		for stat in te_div['result']:
			prediction_model[stat] = {}
			smoothing[stat] = len(te_div['result'][stat])
			for value in te_div['result'][stat]:
				prediction_model[stat][value] = 1

		#Execute query to get the WR's previous games
		#The performance for each game is adjusted based on the opponent to adjust for hard/weak games
		#Ex: if opponent is good against pass_yds then pass_yds increased, or if weak against rush_yds then rush_yds decreased
		rows = []
		with nfldb.Tx(_db) as c:
			c.execute('''
				SELECT 
					fantasy.fumble - sr1.def_fumble * sr2.def_fumble as fumble,
					fantasy.targets - sr1.def_targets * sr2.def_targets as targets,
					fantasy.rec - sr1.def_rec * sr2.def_rec as rec,
					fantasy.rec_yds - sr1.def_rec_yds * sr2.def_rec_yds as rec_yds,
					fantasy.yac - sr1.def_yac * sr2.def_yac as yac,
					fantasy.td - sr1.def_rec_tds * sr2.def_rec_tds as td,
					fantasy.points - (sr1.def_rec_yds * sr2.def_rec_yds) / 10.0 + (sr1.def_fumble * sr2.def_fumble) * 2.0 - (sr1.def_rec_tds * sr2.def_rec_tds) * 6.0 as points
				FROM public.fantasy
					JOIN public.game as g on fantasy.gsis_id = g.gsis_id
					JOIN public.season_rankings as sr1
						ON sr1.season_year = g.season_year
							AND sr1.team_id = case when g.away_team = fantasy.team_id then g.home_team else g.away_team end
							AND sr1.avg = 'f'
					JOIN public.season_rankings as sr2
						ON sr2.season_year = g.season_year
							AND sr2.team_id = 'UNK'
							AND sr2.avg = 'f'
				WHERE fantasy.player_id = '%s'
					AND fantasy.gsis_id < '%s'
				''' %(player_id, gsis_id))
			rows = c.fetchall()

		#Determine the base percentage of the likelihood of each class
		for row in rows:
			for stat in te_div['result']:
				amount = row[stat]

				#Round amount to nearest class
				for index in range(0, len(te_div['result'][stat])):
					if amount <= te_div['result_div'][stat][index+1]:
						amount = te_div['result'][stat][index]
						break

				if amount in prediction_model[stat]:
					prediction_model[stat][amount] += 1

		for stat in prediction_model:
			for amount in prediction_model[stat]:
				prediction_model[stat][amount] = .3*log10(prediction_model[stat][amount] / (len(rows) + smoothing[stat]))

		#Load the naive bayes RB model from file
		f = open(file_name, 'r')
		job = generate_te_model.TEModel()
		TEModel = {}
		for line in f:
			stat_type, model = job.parse_output_line(line)
			TEModel[stat_type] = model

		#Loop through each previous average
		for prev_avg in prev:
			prev_amount = prev_avg['prev_amount']

			#Loop through each stat of the previous average
			for stat_type in te_div['prev']:
				#Get the value of the stat
				feature = prev_avg[stat_type]
				weighting_factor = prev_weights[prev_amount] * te_div['stat_factor'][stat_type]

				#Round feature to nearest class
				for feature_class in te_div['prev'][stat_type]:
					if feature <= feature_class:
						feature = feature_class
						break

				#Get the chance for 
				for result_stat in te_div['result']:
					for result_class in te_div['result'][result_stat]:
						if str(result_class) not in TEModel[result_stat] or prev_amount not in TEModel[result_stat][str(result_class)] or stat_type not in TEModel[result_stat][str(result_class)][prev_amount]:
							chance = 1
						else:
							chance = TEModel[result_stat][str(result_class)][prev_amount][stat_type].get(str(feature), 0) + 1
						if prev_amount not in TEModel[result_stat]['total'] or stat_type not in TEModel[result_stat]['total'][prev_amount]:
							total_chance = smoothing[result_stat]
						else:
							total_chance = TEModel[result_stat]['total'][prev_amount][stat_type].get(str(feature), 0) + smoothing[result_stat]
						prediction_model[result_stat][result_class] += weighting_factor * log10(chance / total_chance)

		#Prediction for each stat has been calculated
		#Now calculated predicted value for each stat based on chances of each stat occuring
		estimate_model = {}
		for stat_type in prediction_model:
			estimate_model[stat_type] = 0

			estimate_array = [[key, prediction_model[stat_type][key]] for key in prediction_model[stat_type]]
			estimate_array.sort(lambda x,y: cmp(y[1], x[1]))
			highest = estimate_array[0][1]
			for pair in estimate_array:
				pair[1] -= highest + 1
				pair[1] = pow(10, pair[1])

			self._Normalize_Chances(estimate_array)

			for pair in estimate_array:
				estimate_model[stat_type] += pair[0] * pair[1]


		with nfldb.Tx(_db) as c:
			c.execute('''
				select sr.def_rec_yds as rec_yds
					, (sr.def_rush_tds * .2 + sr.def_rec_tds) as td
					, sr.def_fumble as fumble
				from public.player as p
					join public.game as g on p.team in (g.home_team, g.away_team)
					join public.season_rankings as sr
						on sr.season_year = g.season_year
							and 
							(
								sr.team_id = case when g.away_team = p.team then g.home_team else g.away_team end
								or sr.team_id = 'UNK'
							)
				where p.player_id = '%s'
					and g.gsis_id = '%s'
					and sr.avg = 'f'
				order by sr.team_id;
				''' %(player_id, gsis_id))
			opponent = c.fetchone()
			stddev = c.fetchone()

			#Bias the predicted stats based on the opponent
			for stat_type in opponent:
				estimate_model[stat_type] += opponent[stat_type] * stddev[stat_type]

		#Bias the predicted points based on the opponent
		estimate_model['points'] += opponent['rec_yds'] * stddev['rec_yds'] / 10 - opponent['fumble'] * stddev['fumble'] * 2 + opponent['td'] * stddev['td'] * 6

		#Predict the fantasy points based on the predicted stats of the player
		estimate_model['calc_points'] = estimate_model['rec_yds'] / 10.0 + estimate_model['td'] * 6.0 - estimate_model['fumble'] * 2.0


		prev_points = 0
		for row in prev:
			prev_amount = row['prev_amount']
			prev_points += row['points'] * prev_weights[prev_amount]

		prediction = .2*estimate_model['points'] + .4*estimate_model['calc_points'] + .4 * (prev_points / 1.1)
		if prediction < 0:
			prediction /= 3
		return prediction

	#Function used to predict the performance of K's
	def _K_predict(self, prev, player_id, gsis_id):
		#File name of the naive bayes model for QB's
		file_name = './K Model/k_naive.json'

		#Chance of the game belonging to the points category
		prediction_model = {}
		smoothing = {}

		#Initialize prediction model
		for stat in k_div['result']:
			prediction_model[stat] = {}
			smoothing[stat] = len(k_div['result'][stat])
			for value in k_div['result'][stat]:
				prediction_model[stat][value] = 1

		#Execute query to get the K's previous games
		#The performance for each game is adjusted based on the opponent to adjust for hard/weak games
		#Ex: if opponent is good against pass_yds then pass_yds increased, or if weak against rush_yds then rush_yds decreased
		rows = []
		with nfldb.Tx(_db) as c:
			c.execute('''
				SELECT 
					fantasy.fg_50 - sr1.def_pts * sr2.def_pts / 4.0 as fg_50,
					fantasy.fg_40 - sr1.def_pts * sr2.def_pts / 4.0 as fg_40,
					fantasy.fg_0 - sr1.def_pts * sr2.def_pts / 4.0 as fg_0,
					fantasy.pat - sr1.def_pts * sr2.def_pts / 5.0 as pat,
					fantasy.fg_miss - sr1.def_block * sr2.def_block / 2.0 as fg_miss,
					fantasy.points
				FROM public.fantasy
					JOIN public.game as g on fantasy.gsis_id = g.gsis_id
					JOIN public.season_rankings as sr1
						ON sr1.season_year = g.season_year
							AND sr1.team_id = case when g.away_team = fantasy.team_id then g.home_team else g.away_team end
							AND sr1.avg = 'f'
					JOIN public.season_rankings as sr2
						ON sr2.season_year = g.season_year
							AND sr2.team_id = 'UNK'
							AND sr2.avg = 'f'
				WHERE fantasy.player_id = '%s'
					AND fantasy.gsis_id < '%s'
				''' %(player_id, gsis_id))
			rows = c.fetchall()

		#Determine the base percentage of the likelihood of each class
		for row in rows:
			for stat in k_div['result']:
				amount = row[stat]

				#Round amount to nearest class
				for index in range(0, len(k_div['result'][stat])):
					if amount <= k_div['result_div'][stat][index+1]:
						amount = k_div['result'][stat][index]
						break

				if amount in prediction_model[stat]:
					prediction_model[stat][amount] += 1

		for stat in prediction_model:
			for amount in prediction_model[stat]:
				prediction_model[stat][amount] = .3*log10(prediction_model[stat][amount] / (len(rows) + smoothing[stat]))

		#Load the naive bayes QB model from file
		f = open(file_name, 'r')
		job = generate_k_model.KModel()
		KModel = {}
		for line in f:
			stat_type, model = job.parse_output_line(line)
			KModel[stat_type] = model

		#Loop through each previous average
		for prev_avg in prev:
			prev_amount = prev_avg['prev_amount']

			#Loop through each stat of the previous average
			for stat_type in k_div['prev']:
				#Get the value of the stat
				feature = prev_avg[stat_type]
				weighting_factor = prev_weights[prev_amount] * k_div['stat_factor'][stat_type]

				#Round feature to nearest class
				for feature_class in k_div['prev'][stat_type]:
					if feature <= feature_class:
						feature = feature_class
						break

				#Get the chance for each class based on previous stat
				for result_stat in k_div['result']:
					for result_class in k_div['result'][result_stat]:
						if str(result_class) not in KModel[result_stat] or prev_amount not in KModel[result_stat][str(result_class)] or stat_type not in KModel[result_stat][str(result_class)][prev_amount]:
							chance = 1
						else:
							chance = KModel[result_stat][str(result_class)][prev_amount][stat_type].get(str(feature), 0) + 1
						if prev_amount not in KModel[result_stat]['total'] or stat_type not in KModel[result_stat]['total'][prev_amount]:
							total_chance = smoothing[result_stat]
						else:
							total_chance = KModel[result_stat]['total'][prev_amount][stat_type].get(str(feature), 0) + smoothing[result_stat]
						prediction_model[result_stat][result_class] += weighting_factor * log10(chance / total_chance)

		#Prediction for each stat has been calculated
		#Now calculated predicted value for each stat based on chances of each stat occuring
		estimate_model = {}
		for stat_type in prediction_model:
			estimate_model[stat_type] = 0

			estimate_array = [[key, prediction_model[stat_type][key]] for key in prediction_model[stat_type]]
			estimate_array.sort(lambda x,y: cmp(y[1], x[1]))
			highest = estimate_array[0][1]
			for pair in estimate_array:
				pair[1] -= highest + 1
				pair[1] = pow(10, pair[1])

			self._Normalize_Chances(estimate_array)

			for pair in estimate_array:
				estimate_model[stat_type] += pair[0] * pair[1]

		with nfldb.Tx(_db) as c:
			c.execute('''
				select sr.def_pts / 4.0 as fg_50
					, sr.def_pts / 4.0 as fg_40
					, sr.def_pts / 4.0 as fg_0
					, sr.def_pts / 5.0 as pat
					, sr.def_block / 2.0 as fg_miss
				from public.player as p
					join public.game as g on p.team in (g.home_team, g.away_team)
					join public.season_rankings as sr
						on sr.season_year = g.season_year
							and 
							(
								sr.team_id = case when g.away_team = p.team then g.home_team else g.away_team end
								or sr.team_id = 'UNK'
							)
				where p.player_id = '%s'
					and g.gsis_id = '%s'
					and sr.avg = 'f'
				order by sr.team_id;
				''' %(player_id, gsis_id))
			opponent = c.fetchone()
			stddev = c.fetchone()

			#Bias the predicted stats based on the opponent
			for stat_type in opponent:
				estimate_model[stat_type] += opponent[stat_type] * stddev[stat_type]

		#Bias the predicted points based on the opponent
		estimate_model['points'] += opponent['fg_50'] * stddev['fg_50'] * 5.0 + opponent['fg_40'] * stddev['fg_40'] * 4.0 + opponent['fg_0'] * stddev['fg_0'] * 3.0 + opponent['pat'] * stddev['pat'] * 1.0 - opponent['fg_miss'] * stddev['fg_miss'] * 1.0

		#Predict the fantasy points based on the predicted stats of the player
		estimate_model['calc_points'] = estimate_model['fg_50'] * 5.0 + estimate_model['fg_40'] * 4.0 + estimate_model['fg_0'] * 3.0 + estimate_model['pat'] * 1.0 - estimate_model['fg_miss'] * 1.0

		prev_points = 0
		for row in prev:
			prev_amount = row['prev_amount']
			prev_points += row['points'] * prev_weights[prev_amount]

		return .45*estimate_model['points'] + .15*estimate_model['calc_points'] + .4 * (prev_points / 1.1)

	#Function used to predict the performance of DEF's
	def _DEF_predict(self, prev, team_id, gsis_id):
		#File name of the naive bayes model for QB's
		file_name = './DEF Model/def_naive.json'

		#Chance of the game belonging to the points category
		prediction_model = {}
		smoothing = {}

		#Initialize prediction model
		for stat in def_div['result']:
			prediction_model[stat] = {}
			smoothing[stat] = len(def_div['result'][stat])
			for value in def_div['result'][stat]:
				prediction_model[stat][value] = 1

		#Execute query to get the DEF's previous games
		#The performance for each game is adjusted based on the opponent to adjust for hard/weak games
		#Ex: if opponent is good against pass_yds then pass_yds increased, or if weak against rush_yds then rush_yds decreased
		rows = []
		with nfldb.Tx(_db) as c:
			c.execute('''
				SELECT
					fantasy.int - sr1.off_int * sr2.off_int as int,
					fantasy.fumble - sr1.off_fumble * sr2.off_fumble as fumble,
					fantasy.td,
					fantasy.block_kick,
					fantasy.safety,
					fantasy.sack - sr1.off_sack * sr2.off_sack as sack,
					fantasy.pts_allowed - sr1.off_pts * sr2.off_pts as pts_allowed,
					fantasy.points
				FROM public.fantasy
					JOIN public.game as g on fantasy.gsis_id = g.gsis_id
					JOIN public.season_rankings as sr1
						ON sr1.season_year = g.season_year
							AND sr1.team_id = case when g.away_team = fantasy.team_id then g.home_team else g.away_team end
							AND sr1.avg = 'f'
					JOIN public.season_rankings as sr2
						ON sr2.season_year = g.season_year
							AND sr2.team_id = 'UNK'
							AND sr2.avg = 'f'
				WHERE fantasy.team_id = '%s'
					AND fantasy.position = 'DEF'
					AND fantasy.gsis_id < '%s'
				''' %(team_id, gsis_id))
			rows = c.fetchall()

		#Determine the base percentage of the likelihood of each class
		for row in rows:
			for stat in def_div['result']:
				amount = row[stat]

				#Round amount to nearest class
				for index in range(0, len(def_div['result'][stat])):
					if amount <= def_div['result_div'][stat][index+1]:
						amount = def_div['result'][stat][index]
						break

				if amount in prediction_model[stat]:
					prediction_model[stat][amount] += 1

		for stat in prediction_model:
			for amount in prediction_model[stat]:
				prediction_model[stat][amount] = .3*log10(prediction_model[stat][amount] / (len(rows) + smoothing[stat]))

		#Load the naive bayes QB model from file
		f = open(file_name, 'r')
		job = generate_def_model.DEFModel()
		DEFModel = {}
		for line in f:
			stat_type, model = job.parse_output_line(line)
			DEFModel[stat_type] = model

		#Loop through each previous average
		for prev_avg in prev:
			prev_amount = prev_avg['prev_amount']

			#Loop through each stat of the previous average
			for stat_type in def_div['prev']:
				#Get the value of the stat
				feature = prev_avg[stat_type]
				weighting_factor = prev_weights[prev_amount] * def_div['stat_factor'][stat_type]

				#Round feature to nearest class
				for feature_class in def_div['prev'][stat_type]:
					if feature <= feature_class:
						feature = feature_class
						break

				#Get the chance for each class based on previous stat
				for result_stat in def_div['result']:
					for result_class in def_div['result'][result_stat]:
						if str(result_class) not in DEFModel[result_stat] or prev_amount not in DEFModel[result_stat][str(result_class)] or stat_type not in DEFModel[result_stat][str(result_class)][prev_amount]:
							chance = 1
						else:
							chance = DEFModel[result_stat][str(result_class)][prev_amount][stat_type].get(str(feature), 0) + 1
						if prev_amount not in DEFModel[result_stat]['total'] or stat_type not in DEFModel[result_stat]['total'][prev_amount]:
							total_chance = smoothing[result_stat]
						else:
							total_chance = DEFModel[result_stat]['total'][prev_amount][stat_type].get(str(feature), 0) + smoothing[result_stat]
						prediction_model[result_stat][result_class] += weighting_factor * log10(chance / total_chance)

		#Prediction for each stat has been calculated
		#Now calculated predicted value for each stat based on chances of each stat occuring
		estimate_model = {}
		for stat_type in prediction_model:
			estimate_model[stat_type] = 0

			estimate_array = [[key, prediction_model[stat_type][key]] for key in prediction_model[stat_type]]
			estimate_array.sort(lambda x,y: cmp(y[1], x[1]))
			highest = estimate_array[0][1]
			for pair in estimate_array:
				pair[1] -= highest + 1
				pair[1] = pow(10, pair[1])

			self._Normalize_Chances(estimate_array)

			for pair in estimate_array:
				estimate_model[stat_type] += pair[0] * pair[1]

		with nfldb.Tx(_db) as c:
			c.execute('''
				select sr.off_int as int
					, sr.off_fumble as fumble
					, sr.off_sack as sack
					, sr.off_pts as pts_allowed
				from public.game as g
					join public.season_rankings as sr
						on sr.season_year = g.season_year
							and 
							(
								sr.team_id = case when g.away_team = '%s' then g.home_team else g.away_team end
								or sr.team_id = 'UNK'
							)
				where '%s' in (g.away_team, g.home_team)
					and g.gsis_id = '%s'
					and sr.avg = 'f'
				order by sr.team_id;
				''' %(team_id, team_id, gsis_id))

			opponent = c.fetchone()
			stddev = c.fetchone()

			#Bias the predicted stats based on the opponent
			for stat_type in opponent:
				estimate_model[stat_type] += opponent[stat_type] * stddev[stat_type] * 1.5

		#Bias the predicted points based on the opponent
		estimate_model['points'] += opponent['int'] * stddev['int'] * 2.0 + opponent['fumble'] * stddev['fumble'] * 2.0 + opponent['sack'] * stddev['sack'] * 1.0 - opponent['pts_allowed'] * stddev['pts_allowed'] / 6.0

		#Predict the fantasy points based on the predicted stats of the player
		estimate_model['calc_points'] = estimate_model['int'] * 2.0 + estimate_model['fumble'] * 2.0 + estimate_model['td'] * 6.0 + estimate_model['block_kick'] * 2.0 + estimate_model['safety'] * 2.0 + estimate_model['sack'] * 1.0
		if estimate_model['pts_allowed']  == 0:
			estimate_model['calc_points'] += 5
		elif estimate_model['pts_allowed'] < 7:
			estimate_model['calc_points'] += 4
		elif estimate_model['pts_allowed'] < 14:
			estimate_model['calc_points'] += 3
		elif estimate_model['pts_allowed'] < 18:
			estimate_model['calc_points'] += 1
		elif estimate_model['pts_allowed'] < 28:
			estimate_model['calc_points'] += 0
		elif estimate_model['pts_allowed'] < 35:
			estimate_model['calc_points'] += -1
		elif estimate_model['pts_allowed'] < 46:
			estimate_model['calc_points'] += -3
		else:
			estimate_model['calc_points'] += -5

		prev_points = 0
		for row in prev:
			prev_amount = row['prev_amount']
			prev_points += row['points'] * prev_weights[prev_amount]

		return .15*estimate_model['points'] + .55*estimate_model['calc_points'] + .3 * (prev_points / 1.1)

	#Function used to normalize the chances so they sum up to 1
	def _Normalize_Chances(self, chances):
		total = 0
		for pair in chances:
			total += pair[1]

		for pair in chances:
			pair[1] = pair[1] / total

if __name__ == '__main__':
	p = Predictor()

	diff = []
	total_diff = 0
	calc_diff = []
	total_calc_diff = 0

	for index in range(1,14):
		rows = []

		with nfldb.Tx(_db) as c:
			c.execute('''
				select f.gsis_id
					, f.player_id
					, f.team_id
					, p.full_name
					, f.points
					, f.rush_att
				from public.fantasy as f
					join public.game as g on f.gsis_id = g.gsis_id
					left outer join public.player as p on f.player_id = p.player_id
				where g.week = '%s' and g.season_year = 2014 and f.position = 'QB'
				''' %(index))
			rows = c.fetchall()

		f = open('week_%s_predictions.json' %(index), 'w')

		ordered_pred = []

		for r in rows:
			points = p.predict(r['player_id'], r['team_id'], r['gsis_id'])
			difference = abs(points - r['points'])
			diff.append(difference)
			total_diff += diff[len(diff) - 1]

			ordered_pred.append([difference,r['full_name'],r['points'],points,r['team_id']])

			#Write the prediction vs. real points to file
		ordered_pred.sort(lambda x,y: cmp(x[0],y[0]))

		for elem in ordered_pred:	
			f.write(json.dumps({'full_name': elem[1], 'team': elem[4],'Points':elem[2],'Pred_points':elem[3],'Diff':elem[0]}) + '\n')


	#Calculate the average and standard deviation for the predictions
	avg = total_diff / len(diff)
	var = 0
	stddev = 0

	for d in diff:
		var += pow(avg - d, 2)

	stddev = sqrt(var / len(diff))

	print 'Avg: %f, Std Dev: %f' %(avg, stddev)

	RMSE = 0
	for val in diff:
		RMSE += pow(val,2)
	RMSE /= len(diff)
	RMSE = sqrt(RMSE)

	print RMSE