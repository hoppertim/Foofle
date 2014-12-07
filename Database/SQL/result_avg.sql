SELECT avg(safety) as _____________________avg
FROM public.fantasy
WHERE position = 'DEF'
	AND safety <=1
	AND safety >=0