select count
	, round(cast(pts_allowed as numeric),1)
FROM
(
	select row_number() over (order by pts_allowed)as count
		, *
	from public.fantasy
	where position = 'DEF'
) as t0
where t0.count = 1 or t0.count %  306 = 0 or count = 3054