-- LATEST

update
	features
set
	ma14 = candle_features.ma14,
	ma30 = candle_features.ma30,
	ma90 = candle_features.ma90
from
	(select ch.pair_id, ch.open_time,
		avg(ch.close) over (partition by ch.pair_id order by ch.open_time rows between 13 preceding and current row) as ma14,
		avg(ch.close) over (partition by ch.pair_id order by ch.open_time rows between 29 preceding and current row) as ma30,
		avg(ch.close) over (partition by ch.pair_id order by ch.open_time rows between 89 preceding and current row) as ma90
	from candlestick_15m ch
where pair_id in (-1,-2,-3)
	) candle_features
where candle_features.open_time = features.candle_open_time and candle_features.pair_id = features.pair_id



update
	features
set
	ema_up  = results.ema_up,
	ema_down  = results.ema_down,
	rsi  = results.rsi
from
	(select 
	pair_id, open_time,
	ema_up, ema_down,
	100.0 - (100.0/ (1 + coalesce(ema_up / nullif(ema_down, 0), 0))) as rsi
from (select open_time, pair_id, ema2(up) over (partition by pair_id order by open_time) as ema_up, ema2(down) over (partition by pair_id order by open_time) as ema_down from (select open_time, pair_id, greatest(0, delta) as up, greatest(0,-delta) as down from (select open_time, pair_id, close, close - lag(close,1) over (partition by pair_id order by open_time) as delta from candlestick_15m
where pair_id in (-1,-2,-3)
) delta_results) updown_results) ema_results) results
where results.open_time = features.candle_open_time and results.pair_id = features.pair_id



update
	features
set
	rsi_diff  = res.rsi_diff,
	rsi_ma14  = res.rsi_ma14
from
	(select 
	pair_id, candle_open_time,
	rsi - lag(rsi,1) over (partition by pair_id order by candle_open_time) as rsi_diff,
	avg(rsi) over (partition by pair_id order by candle_open_time rows between 13 preceding and current row) as rsi_ma14
from features
where pair_id in (-1,-2,-3)
) res
where res.candle_open_time = features.candle_open_time and res.pair_id = features.pair_id



update
	features
set
	atr = atr_all_sorted.atr,
	atr_diff = atr_all_sorted.atr_diff,
	atr_ma14 = atr_all_sorted.atr_ma14
from
	(select * from
		(select *, atr-LAG(atr,1) OVER (partition by pair_id ORDER BY open_time) as atr_diff, AVG(catr.atr) OVER(partition by pair_id ORDER BY catr.open_time ROWS BETWEEN 13 PRECEDING AND CURRENT ROW) AS atr_ma14
			from 
				(
					select pair_id, open_time, AVG(ca.tr) OVER(partition by ca.pair_id ORDER BY ca.open_time ROWS BETWEEN 13 PRECEDING AND CURRENT ROW) AS atr
						from (select pair_id, open_time, greatest(high-low, abs(high-LAG(close,1) OVER (partition by cm.pair_id ORDER BY open_time)), abs(low-LAG(close,1) OVER (partition by cm.pair_id ORDER BY open_time))) as tr from candlestick_15m cm
where cm.pair_id in (-1,-2,-3)
						ORDER BY open_time) ca
				) catr
			 order by catr.open_time) atr_all order by open_time desc) atr_all_sorted
where atr_all_sorted.open_time = features.candle_open_time and atr_all_sorted.pair_id = features.pair_id


-- update features set dot, tow, pattern flags
update
	features
set
	dow = patterns.dow,
	tod = patterns.tod,
	trend_up = patterns.trend_up,
	trend_up3 = patterns.trend_up3,
	trend_up14 = patterns.trend_up14,
	trend_up30 = patterns.trend_up30,
	cs_ss = patterns.cs_ss,
	cs_ssr = patterns.cs_ssr,
	cs_hm = patterns.cs_hm,
	cs_hmr = patterns.cs_hmr,
	cs_brh = patterns.cs_brh,
	cs_buh = patterns.cs_buh,
	cs_ebu = patterns.cs_ebu,
	cs_ebr = patterns.cs_ebr
from
	(select
		pair_id, open_time,
		extract(dow FROM ch.open_time) as dow,
		mod(cast(extract(epoch FROM ch.open_time) / 86400 as numeric), 1) as tod,
		ch.close - LAG(ch.close,1) over (partition by pair_id order by ch.open_time) > 0 as trend_up,
		(AVG(ch.close) over (partition by pair_id order by ch.open_time rows between 2 preceding and current row)  - AVG(ch.close) over (partition by pair_id order by ch.open_time rows between 3 preceding and 1 preceding)) > 0 as trend_up3,
		(AVG(ch.close) over (partition by pair_id order by ch.open_time rows between 13 preceding and current row)  - AVG(ch.close) over (partition by pair_id order by ch.open_time rows between 14 preceding and 1 preceding)) > 0 as trend_up14,
		(AVG(ch.close) over (partition by pair_id order by ch.open_time rows between 29 preceding and current row)  - AVG(ch.close) over (partition by pair_id order by ch.open_time rows between 30 preceding and 1 preceding)) > 0 as trend_up30,
		(open <= close) and (low + 0.382*(high-low) >= close) as cs_ss,
		(open > close) and (low + 0.382*(high-low) >= open) as cs_ssR,
		(open >= close) and (high - 0.382*(high-low) <= close) as cs_hm,
		(open < close) and (high - 0.382*(high-low) <= open) as cs_hmR,
		(open > close) and
			(LAG(ch.open,1) over (partition by pair_id order by ch.open_time) < LAG(ch.close,1) over (partition by pair_id order by ch.open_time)) and
			(LAG(ch.close,1) over (partition by pair_id order by ch.open_time) >= open) and
			(LAG(ch.open,1) over (partition by pair_id order by ch.open_time) <= close) and
			(LAG(ch.high,1) over (partition by pair_id order by ch.open_time) >= high) and
			(LAG(ch.high,1) over (partition by pair_id order by ch.open_time) <= low) as cs_brh,
		(open < close) and
			(LAG(ch.open,1) over (partition by pair_id order by ch.open_time) > LAG(ch.close,1) over (partition by pair_id order by ch.open_time)) and
			(LAG(ch.close,1) over (partition by pair_id order by ch.open_time) <= open) and
			(LAG(ch.open,1) over (partition by pair_id order by ch.open_time) > close) and
			(LAG(ch.high,1) over (partition by pair_id order by ch.open_time) >= high) and
			(LAG(ch.high,1) over (partition by pair_id order by ch.open_time) <= low) as cs_buh,
		(open < close) and 
			(LAG(ch.open,1) over (partition by pair_id order by ch.open_time) > LAG(ch.close,1) over (partition by pair_id order by ch.open_time)) and
			(LAG(ch.close,1) over (partition by pair_id order by ch.open_time) >= open) and
			(LAG(ch.open,1) over (partition by pair_id order by ch.open_time) <= close) and
			(LAG(ch.high,1) over (partition by pair_id order by ch.open_time) <= high) and
			(LAG(ch.high,1) over (partition by pair_id order by ch.open_time) >= low) as cs_ebu,
		(open > close) and 
			(LAG(ch.open,1) over (partition by pair_id order by ch.open_time) < LAG(ch.close,1) over (partition by pair_id order by ch.open_time)) and
			(LAG(ch.close,1) over (partition by pair_id order by ch.open_time) <= open) and
			(LAG(ch.open,1) over (partition by pair_id order by ch.open_time) >= close) and
			(LAG(ch.high,1) over (partition by pair_id order by ch.open_time) <= high) and
			(LAG(ch.high,1) over (partition by pair_id order by ch.open_time) >= low) as cs_ebr
	from candlestick_15m ch where close_time is not null
and ch.pair_id in (-1,-2,-3)
	order by open_time desc) patterns
where patterns.open_time = features.candle_open_time and patterns.pair_id = features.pair_id


---- OLDER STUFF
-- manually backfill null entries in features


update
	features
set
	ma14 = candle_features.ma14,
	ma30 = candle_features.ma30,
	ma90 = candle_features.ma90
from
	(select ch.pair_id, ch.open_time,
		avg(ch.close) over (partition by ch.pair_id order by ch.open_time rows between 13 preceding and current row) as ma14,
		avg(ch.close) over (partition by ch.pair_id order by ch.open_time rows between 29 preceding and current row) as ma30,
		avg(ch.close) over (partition by ch.pair_id order by ch.open_time rows between 89 preceding and current row) as ma90
	from candlestick_15m ch) candle_features
where candle_features.open_time = features.candle_open_time and candle_features.pair_id = features.pair_id




-- ATR, atr diff, atr ma14

update
	features
set
	atr = atr_all_sorted.atr,
	atr_diff = atr_all_sorted.atr_diff,
	atr_ma14 = atr_all_sorted.atr_ma14
from
	(select * from
		(select *, atr-LAG(atr,1) OVER (partition by pair_id ORDER BY open_time) as atr_diff, AVG(catr.atr) OVER(partition by pair_id ORDER BY catr.open_time ROWS BETWEEN 13 PRECEDING AND CURRENT ROW) AS atr_ma14
			from 
				(
					select pair_id, open_time, AVG(ca.tr) OVER(partition by ca.pair_id ORDER BY ca.open_time ROWS BETWEEN 13 PRECEDING AND CURRENT ROW) AS atr
						from (select pair_id, open_time, greatest(high-low, abs(high-LAG(close,1) OVER (partition by cm.pair_id ORDER BY open_time)), abs(low-LAG(close,1) OVER (partition by cm.pair_id ORDER BY open_time))) as tr from candlestick_15m cm where cm.pair_id = 0 ORDER BY open_time) ca
				) catr
			 order by catr.open_time) atr_all order by open_time desc) atr_all_sorted
where atr_all_sorted.open_time = features.candle_open_time and atr_all_sorted.pair_id = features.pair_id






-- ema up ema down rsi
update
	features
set
	ema_up  = results.ema_up,
	ema_down  = results.ema_down,
	rsi  = results.rsi
from
	(select 
	pair_id, open_time,
	ema_up, ema_down,
	100.0 - (100.0/ (1 + coalesce(ema_up / nullif(ema_down, 0), 0))) as rsi
from (select open_time, pair_id, ema2(up) over (partition by pair_id order by open_time) as ema_up, ema2(down) over (partition by pair_id order by open_time) as ema_down from (select open_time, pair_id, greatest(0, delta) as up, greatest(0,-delta) as down from (select open_time, pair_id, close, close - lag(close,1) over (partition by pair_id order by open_time) as delta from candlestick_15m) delta_results) updown_results) ema_results) results
where results.open_time = features.candle_open_time and results.pair_id = features.pair_id


update
	features
set
	rsi_diff  = res.rsi_diff,
	rsi_ma14  = res.rsi_ma14
from
	(select 
	pair_id, candle_open_time,
	rsi - lag(rsi,1) over (partition by pair_id order by candle_open_time) as rsi_diff,
	avg(rsi) over (partition by pair_id order by candle_open_time rows between 13 preceding and current row) as rsi_ma14
from features) res
where res.candle_open_time = features.candle_open_time and res.pair_id = features.pair_id





-- update features set dot, tow, pattern flags
update
	features
set
	dow = patterns.dow,
	tod = patterns.tod,
	trend_up = patterns.trend_up,
	trend_up3 = patterns.trend_up3,
	trend_up14 = patterns.trend_up14,
	trend_up30 = patterns.trend_up30,
	cs_ss = patterns.cs_ss,
	cs_ssr = patterns.cs_ssr,
	cs_hm = patterns.cs_hm,
	cs_hmr = patterns.cs_hmr,
	cs_brh = patterns.cs_brh,
	cs_buh = patterns.cs_buh,
	cs_ebu = patterns.cs_ebu,
	cs_ebr = patterns.cs_ebr
from
	(select
		pair_id, open_time,
		extract(dow FROM ch.open_time) as dow,
		mod(cast(extract(epoch FROM ch.open_time) / 86400 as numeric), 1) as tod,
		ch.close - LAG(ch.close,1) over (partition by pair_id order by ch.open_time) > 0 as trend_up,
		(AVG(ch.close) over (partition by pair_id order by ch.open_time rows between 2 preceding and current row)  - AVG(ch.close) over (partition by pair_id order by ch.open_time rows between 3 preceding and 1 preceding)) > 0 as trend_up3,
		(AVG(ch.close) over (partition by pair_id order by ch.open_time rows between 13 preceding and current row)  - AVG(ch.close) over (partition by pair_id order by ch.open_time rows between 14 preceding and 1 preceding)) > 0 as trend_up14,
		(AVG(ch.close) over (partition by pair_id order by ch.open_time rows between 29 preceding and current row)  - AVG(ch.close) over (partition by pair_id order by ch.open_time rows between 30 preceding and 1 preceding)) > 0 as trend_up30,
		(open <= close) and (low + 0.382*(high-low) >= close) as cs_ss,
		(open > close) and (low + 0.382*(high-low) >= open) as cs_ssR,
		(open >= close) and (high - 0.382*(high-low) <= close) as cs_hm,
		(open < close) and (high - 0.382*(high-low) <= open) as cs_hmR,
		(open > close) and
			(LAG(ch.open,1) over (partition by pair_id order by ch.open_time) < LAG(ch.close,1) over (partition by pair_id order by ch.open_time)) and
			(LAG(ch.close,1) over (partition by pair_id order by ch.open_time) >= open) and
			(LAG(ch.open,1) over (partition by pair_id order by ch.open_time) <= close) and
			(LAG(ch.high,1) over (partition by pair_id order by ch.open_time) >= high) and
			(LAG(ch.high,1) over (partition by pair_id order by ch.open_time) <= low) as cs_brh,
		(open < close) and
			(LAG(ch.open,1) over (partition by pair_id order by ch.open_time) > LAG(ch.close,1) over (partition by pair_id order by ch.open_time)) and
			(LAG(ch.close,1) over (partition by pair_id order by ch.open_time) <= open) and
			(LAG(ch.open,1) over (partition by pair_id order by ch.open_time) > close) and
			(LAG(ch.high,1) over (partition by pair_id order by ch.open_time) >= high) and
			(LAG(ch.high,1) over (partition by pair_id order by ch.open_time) <= low) as cs_buh,
		(open < close) and 
			(LAG(ch.open,1) over (partition by pair_id order by ch.open_time) > LAG(ch.close,1) over (partition by pair_id order by ch.open_time)) and
			(LAG(ch.close,1) over (partition by pair_id order by ch.open_time) >= open) and
			(LAG(ch.open,1) over (partition by pair_id order by ch.open_time) <= close) and
			(LAG(ch.high,1) over (partition by pair_id order by ch.open_time) <= high) and
			(LAG(ch.high,1) over (partition by pair_id order by ch.open_time) >= low) as cs_ebu,
		(open > close) and 
			(LAG(ch.open,1) over (partition by pair_id order by ch.open_time) < LAG(ch.close,1) over (partition by pair_id order by ch.open_time)) and
			(LAG(ch.close,1) over (partition by pair_id order by ch.open_time) <= open) and
			(LAG(ch.open,1) over (partition by pair_id order by ch.open_time) >= close) and
			(LAG(ch.high,1) over (partition by pair_id order by ch.open_time) <= high) and
			(LAG(ch.high,1) over (partition by pair_id order by ch.open_time) >= low) as cs_ebr
	from candlestick_15m ch where close_time is not null order by open_time desc) patterns
where patterns.open_time = features.candle_open_time and patterns.pair_id = features.pair_id