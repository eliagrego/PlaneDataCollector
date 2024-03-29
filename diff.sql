SELECT NAME, MIN(TS), COUNT(*)
FROM fieldstat
GROUP BY NAME
HAVING COUNT(*) < (
	SELECT count(*)
	FROM fieldstat
	GROUP BY NAME
	ORDER BY COUNT(*) DESC
	LIMIT 1
) ORDER BY COUNT(*) desc, MIN(TS) DESC, NAME ASC;