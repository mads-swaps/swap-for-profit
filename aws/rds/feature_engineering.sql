update
	features
set
	open_1  = candle_features.open_1,
	high_1  = candle_features.high_1,
	low_1  = candle_features.low_1,
	close_1  = candle_features.close_1,
	open_2  = candle_features.open_2,
	high_2  = candle_features.high_2,
	low_2  = candle_features.low_2,
	close_2  = candle_features.close_2,
	open_3  = candle_features.open_3,
	high_3  = candle_features.high_3,
	low_3  = candle_features.low_3,
	close_3  = candle_features.close_3,
	open_4  = candle_features.open_4,
	high_4  = candle_features.high_4,
	low_4  = candle_features.low_4,
	close_4  = candle_features.close_4,
	open_5  = candle_features.open_5,
	high_5  = candle_features.high_5,
	low_5  = candle_features.low_5,
	close_5  = candle_features.close_5,
	open_6  = candle_features.open_6,
	high_6  = candle_features.high_6,
	low_6  = candle_features.low_6,
	close_6  = candle_features.close_6,
	open_7  = candle_features.open_7,
	high_7  = candle_features.high_7,
	low_7  = candle_features.low_7,
	close_7  = candle_features.close_7,
	open_8  = candle_features.open_8,
	high_8  = candle_features.high_8,
	low_8  = candle_features.low_8,
	close_8  = candle_features.close_8,
	open_9  = candle_features.open_9,
	high_9  = candle_features.high_9,
	low_9  = candle_features.low_9,
	close_9  = candle_features.close_9,
	open_10  = candle_features.open_10,
	high_10  = candle_features.high_10,
	low_10  = candle_features.low_10,
	close_10  = candle_features.close_10,
	open_11  = candle_features.open_11,
	high_11  = candle_features.high_11,
	low_11  = candle_features.low_11,
	close_11  = candle_features.close_11,
	open_12  = candle_features.open_12,
	high_12  = candle_features.high_12,
	low_12  = candle_features.low_12,
	close_12  = candle_features.close_12,
	open_13  = candle_features.open_13,
	high_13  = candle_features.high_13,
	low_13  = candle_features.low_13,
	close_13  = candle_features.close_13,
	open_14  = candle_features.open_14,
	high_14  = candle_features.high_14,
	low_14  = candle_features.low_14,
	close_14  = candle_features.close_14,
	ma14 = candle_features.ma14,
	ma30 = candle_features.ma30,
	ma90 = candle_features.ma90
from
	(select ch.pair_id, ch.open_time,
		lag(ch.open,1) over (partition by ch.pair_id order by ch.open_time) open_1,
		lag(ch.high,1) over (partition by ch.pair_id order by ch.open_time) high_1,
		lag(ch.low,1) over (partition by ch.pair_id order by ch.open_time) low_1,
		lag(ch.close,1) over (partition by ch.pair_id order by ch.open_time) close_1,
		lag(ch.open,2) over (partition by ch.pair_id order by ch.open_time) open_2,
		lag(ch.high,2) over (partition by ch.pair_id order by ch.open_time) high_2,
		lag(ch.low,2) over (partition by ch.pair_id order by ch.open_time) low_2,
		lag(ch.close,2) over (partition by ch.pair_id order by ch.open_time) close_2,
		lag(ch.open,3) over (partition by ch.pair_id order by ch.open_time) open_3,
		lag(ch.high,3) over (partition by ch.pair_id order by ch.open_time) high_3,
		lag(ch.low,3) over (partition by ch.pair_id order by ch.open_time) low_3,
		lag(ch.close,3) over (partition by ch.pair_id order by ch.open_time) close_3,
		lag(ch.open,4) over (partition by ch.pair_id order by ch.open_time) open_4,
		lag(ch.high,4) over (partition by ch.pair_id order by ch.open_time) high_4,
		lag(ch.low,4) over (partition by ch.pair_id order by ch.open_time) low_4,
		lag(ch.close,4) over (partition by ch.pair_id order by ch.open_time) close_4,
		lag(ch.open,5) over (partition by ch.pair_id order by ch.open_time) open_5,
		lag(ch.high,5) over (partition by ch.pair_id order by ch.open_time) high_5,
		lag(ch.low,5) over (partition by ch.pair_id order by ch.open_time) low_5,
		lag(ch.close,5) over (partition by ch.pair_id order by ch.open_time) close_5,
		lag(ch.open,6) over (partition by ch.pair_id order by ch.open_time) open_6,
		lag(ch.high,6) over (partition by ch.pair_id order by ch.open_time) high_6,
		lag(ch.low,6) over (partition by ch.pair_id order by ch.open_time) low_6,
		lag(ch.close,6) over (partition by ch.pair_id order by ch.open_time) close_6,
		lag(ch.open,7) over (partition by ch.pair_id order by ch.open_time) open_7,
		lag(ch.high,7) over (partition by ch.pair_id order by ch.open_time) high_7,
		lag(ch.low,7) over (partition by ch.pair_id order by ch.open_time) low_7,
		lag(ch.close,7) over (partition by ch.pair_id order by ch.open_time) close_7,
		lag(ch.open,8) over (partition by ch.pair_id order by ch.open_time) open_8,
		lag(ch.high,8) over (partition by ch.pair_id order by ch.open_time) high_8,
		lag(ch.low,8) over (partition by ch.pair_id order by ch.open_time) low_8,
		lag(ch.close,8) over (partition by ch.pair_id order by ch.open_time) close_8,
		lag(ch.open,9) over (partition by ch.pair_id order by ch.open_time) open_9,
		lag(ch.high,9) over (partition by ch.pair_id order by ch.open_time) high_9,
		lag(ch.low,9) over (partition by ch.pair_id order by ch.open_time) low_9,
		lag(ch.close,9) over (partition by ch.pair_id order by ch.open_time) close_9,
		lag(ch.open,10) over (partition by ch.pair_id order by ch.open_time) open_10,
		lag(ch.high,10) over (partition by ch.pair_id order by ch.open_time) high_10,
		lag(ch.low,10) over (partition by ch.pair_id order by ch.open_time) low_10,
		lag(ch.close,10) over (partition by ch.pair_id order by ch.open_time) close_10,
		lag(ch.open,11) over (partition by ch.pair_id order by ch.open_time) open_11,
		lag(ch.high,11) over (partition by ch.pair_id order by ch.open_time) high_11,
		lag(ch.low,11) over (partition by ch.pair_id order by ch.open_time) low_11,
		lag(ch.close,11) over (partition by ch.pair_id order by ch.open_time) close_11,
		lag(ch.open,12) over (partition by ch.pair_id order by ch.open_time) open_12,
		lag(ch.high,12) over (partition by ch.pair_id order by ch.open_time) high_12,
		lag(ch.low,12) over (partition by ch.pair_id order by ch.open_time) low_12,
		lag(ch.close,12) over (partition by ch.pair_id order by ch.open_time) close_12,
		lag(ch.open,13) over (partition by ch.pair_id order by ch.open_time) open_13,
		lag(ch.high,13) over (partition by ch.pair_id order by ch.open_time) high_13,
		lag(ch.low,13) over (partition by ch.pair_id order by ch.open_time) low_13,
		lag(ch.close,13) over (partition by ch.pair_id order by ch.open_time) close_13,
		lag(ch.open,14) over (partition by ch.pair_id order by ch.open_time) open_14,
		lag(ch.high,14) over (partition by ch.pair_id order by ch.open_time) high_14,
		lag(ch.low,14) over (partition by ch.pair_id order by ch.open_time) low_14,
		lag(ch.close,14) over (partition by ch.pair_id order by ch.open_time) close_14,
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