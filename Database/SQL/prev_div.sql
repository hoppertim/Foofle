select
	round(cast(min + step * 1.0 as numeric), 2)
	, round(cast(min + step * 2.0 as numeric), 2)
	, round(cast(min + step * 3.0 as numeric), 2)
	, round(cast(min + step * 4.0 as numeric), 2)
	, round(cast(min + step * 5.0 as numeric), 2)
	, round(cast(min + step * 6.0 as numeric), 2)
	, round(cast(min + step * 7.0 as numeric), 2)
	, round(cast(min + step * 8.0 as numeric), 2)
	, round(cast(min + step * 9.0 as numeric), 2)
	, round(cast(min + step * 10.0 as numeric), 2)
from
(
	select min(safety) as min
		, max(safety) as max
		, (max(safety) - min(safety)) / 10 as step
	from public.fantasy_prev
	where position = 'DEF'
		and prev_amount = 'prev5'
) t0