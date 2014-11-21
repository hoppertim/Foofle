from __future__ import division
import re
import json
import nfldb
import generate_qb_model
from math import log10
from math import sqrt

qb_div = {
	'points'		:	[2.16, 6.68, 9.56, 11.5, 13.04, 14.5, 15.91, 17.53, 19.44, 100],
	'pass_att'		:	[7.6, 21.2, 26.4, 28.8, 31, 32.8, 34.4, 36.4, 39, 100],
	'pass_cmp'		:	[4.2, 11.8, 15.4, 17.2, 18.8, 20, 21.2, 22.6, 24.6, 100],
	'pass_yds'		:	[45.3, 131.75, 178, 201.4, 216.5, 231.6, 247.6, 268, 291.4, 1000],
	'pass_tds'		:	[0, .5, .8, 1, 1.2, 1.4, 1.6, 1.8, 2.2, 10],
	'int'			:	[0, .33, .4, .6, .8, 1, 1.2, 1.4, 10],
	'rush_att'		:	[.8, 1.2, 1.4, 1.8, 2, 2.4, 2.8, 3.4, 4.25, 100],
	'rush_yds'		:	[0, .8, 2.2, 3.8, 5.6, 8, 11, 15.2, 21.8, 1000],
	'fumble'		:	[0, .2, .4, 10],
	'td'			:	[0, .2, 10]
}


qb_result_points	=	[-3.47,0.25,1.4,3.21,5.11,6.78,8.34,9.79,11.14,12.36,13.49,14.59,15.64,16.84,18.08,19.35,20.93,23.1,26.25,32.3]

_db = nfldb.connect('nfldb', 'nfldb', 'TDHaug92', 'localhost', '5432', 'US/central')

class Predictor:

	def predict(self, player_id, gsis_id):
		with nfldb.Tx(_db) as c:
			c.execute('''
				SELECT *
				FROM public.fantasy_prev as fp
				WHERE fp.player_id = '%s' AND fp.gsis_id = '%s'
				''' %(player_id, gsis_id))
			rows = c.fetchall()
		
		if len(rows) == 0:
			return
		elif rows[0]['position'].name == 'QB':
			return self._QB_predict(rows, player_id, gsis_id)

	def _QB_predict(self, prev, player_id, gsis_id):
		#File name of the naive bayes model for QB's
		file_name = 'qb_naive.json'

		#Chance of the game belonging to the points category
		points_chance = {}

		#Smoothing factor
		smoothing = len(qb_result_points)

		#Load the points classes from predetermined values
		for point_value in qb_result_points:
			points_chance[point_value] = 1

		#Execute query to get the QB's previous games
		with nfldb.Tx(_db) as c:
			c.execute('''
				SELECT f.points
				FROM public.fantasy as f
				WHERE f.player_id = '%s' AND f.gsis_id < '%s'
				''' %(player_id, gsis_id))
			rows = c.fetchall()

		#Determine the base percentage of the likelihood of each class
		for row in rows:
			points = row['points']
			for index in range(0, len(qb_result_points)):
				if index == len(qb_result_points) - 1:
					points_chance[qb_result_points[index]] += 1
					break
				if points >= qb_result_points[index] and  points < qb_result_points[index+1]:
					prev_dist = points - qb_result_points[index]
					next_dist = qb_result_points[index+1] - points
					if prev_dist < next_dist:
						points_chance[qb_result_points[index]] += 1
					else:
						points_chance[qb_result_points[index+1]] += 1
					break
		total = smoothing + len(rows)
		for point_class in points_chance:
			points_chance[point_class] = log10(points_chance[point_class] / total)
		
		#Load the naive bayes QB model from file
		f = open(file_name, 'r')
		job = generate_qb_model.QBModel()
		QBModel = {}
		for line in f:
			model_points, model = job.parse_output_line(line)
			QBModel[model_points] = model

		#prev -> list of averages
		#list of averages -> prev_amount, average values
		#loop through prev
		#loop through each key in qb_div (corresponds to values used to determine chances)
		#assign class feature to average value in prev
		#based on feature determine the likelikhood of each point class occuring

		#loop through the previous averages
		for avg in prev:
			prev_amount = avg['prev_amount']
			#loop through each key in qb_div (corresponds to values in previous averages)
			for key in qb_div:
				amount = avg[key]
				feature = None
				#Assign class to feature
				for feature_class in qb_div[key]:
					if amount <= feature_class:
						feature = feature_class
						break
				#Break if no class; should never happen
				if feature == None:
					break

				#Calculate chance of that feature occuring for each points class
				#Loop through each possible point class
				for point_class in points_chance:
					points_chance[point_class] = points_chance[point_class] + log10((QBModel[point_class][prev_amount][key].get(str(feature), 0) + 1) / (QBModel['total'][prev_amount][key].get(str(feature), 0) + smoothing))

		points_chance_order = [[point_class, points_chance[point_class]] for point_class in  points_chance]
		points_chance_order.sort(lambda x,y: cmp(y[1], x[1]))

		largest = points_chance_order[0][1]
		for index in range(0, len(points_chance_order)):
			points_chance_order[index][1] = points_chance_order[index][1] - largest - 1

		for chance_pair in points_chance_order:
			chance_pair[1] = pow(10, chance_pair[1])

		self._Normalize_Chances(points_chance_order)

		points_estimate = 0
		for top in points_chance_order:
			points_estimate += top[0] * top[1]

		return points_estimate

	def _Normalize_Chances(self, chances):
		total = 0
		for pair in chances:
			total += pair[1]

		for pair in chances:
			pair[1] = pair[1] / total


if __name__ == '__main__':
	p = Predictor()

	rows = []

	with nfldb.Tx(_db) as c:
			c.execute('''
				select f.gsis_id
					, f.player_id
					, p.full_name
					, f.points
				from public.fantasy as f
					join public.game as g on f.gsis_id = g.gsis_id
					join public.player as p on f.player_id = p.player_id
				where g.week = 1 and g.season_year = 2014 and f.position = 'QB'
				''')
			rows = c.fetchall()

	arr = []

	for r in rows:
		prediction = p.predict(r['player_id'], r['gsis_id'])
		arr.append([r['full_name'], prediction, r['points']])

	arr.sort(lambda x, y: cmp(abs(x[1] - x[2]), abs(y[1] - y[2])))

	f = open('week_1_predictions.json', 'w')

	for r in arr:
		f.write(json.dumps({'Full Name': r[0], 'Prediction': r[1], 'Actual': r[2], 'Difference': abs(r[2]-r[1])}) + '\n')