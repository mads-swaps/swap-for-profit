CREATE OR REPLACE FUNCTION public.create_feature()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
    begin
	    if old.close_time is null and new.close_time is not null then
			insert into features (pair_id, candle_open_time) values (new.pair_id, new.open_time) on conflict do nothing;
		end if;
		return new;
    end;
$function$
;


CREATE OR REPLACE FUNCTION public.ema2_func(state numeric, inval numeric)
 RETURNS numeric
 LANGUAGE plpgsql
AS $function$
begin
  return case
         when state is null then inval
         else inval/14.0 + state*13.0/14.0
         end;
end
$function$
;

create or replace aggregate ema2(numeric) (sfunc = ema2_func, stype = numeric);




CREATE OR REPLACE FUNCTION public.feature_engineering()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
    begin

	    
with
	ch AS (SELECT * FROM candlestick_15m where pair_id = new.pair_id and open_time <= new.candle_open_time ORDER BY open_time desc limit 90),
	atr_all as (
		with catr as (
			with ca as ( select pair_id, open_time, greatest(high-low, abs(high-LAG(close,1) OVER (ORDER BY open_time)), abs(low-LAG(close,1) OVER (ORDER BY open_time))) as tr from candlestick_15m where pair_id = new.pair_id and open_time <= new.candle_open_time ORDER BY open_time desc limit 29)
			select pair_id, open_time, AVG(ca.tr) OVER(ORDER BY ca.open_time ROWS BETWEEN 13 PRECEDING AND CURRENT ROW) AS atr from ca
		) select *, atr-LAG(atr,1) OVER (ORDER BY open_time) as atr_diff, AVG(catr.atr) OVER(ORDER BY catr.open_time ROWS BETWEEN 13 PRECEDING AND CURRENT ROW) AS atr_ma14 from catr order by catr.open_time desc limit 14),
	rsi_all as (select *,
		rsi - lag(rsi,1) over (partition by pair_id order by open_time) as rsi_diff,
		avg(rsi) over (partition by pair_id order by open_time rows between 13 preceding and current row) as rsi_ma14
		from
		(select
			cm.pair_id, open_time, 
			greatest(0,close - lag(close,1) over (partition by cm.pair_id order by cm.open_time))/14.0 + lag(ema_up,1) over (partition by cm.pair_id order by cm.open_time)*13.0/14.0 as ema_up,
			greatest(0,lag(close,1) over (partition by cm.pair_id order by cm.open_time) - close)/14.0 + lag(ema_down,1) over (partition by cm.pair_id order by cm.open_time)*13.0/14.0 as ema_down,
			100.0 - (100.0/ (1 + ((greatest(0,close - lag(close,1) over (partition by cm.pair_id order by cm.open_time))/14.0 + lag(ema_up,1) over (partition by cm.pair_id order by cm.open_time)*13.0/14.0) / (greatest(0,lag(close,1) over (partition by cm.pair_id order by cm.open_time) - close)/14.0 + lag(ema_down,1) over (partition by cm.pair_id order by cm.open_time)*13.0/14.0)))) as rsi
		from 
			candlestick_15m cm 
		inner join (select * from features where features.pair_id = new.pair_id and features.candle_open_time <= new.candle_open_time order by features.candle_open_time desc limit 15) f on f.pair_id = cm.pair_id and f.candle_open_time = cm.open_time) ema_rsi_results  order by open_time desc limit 1)
select
	LAG(ch.open,1) OVER (ORDER BY ch.open_time) open_1,
	LAG(ch.high,1) OVER (ORDER BY ch.open_time) high_1,
	LAG(ch.low,1) OVER (ORDER BY ch.open_time) low_1,
	LAG(ch.close,1) OVER (ORDER BY ch.open_time) close_1,
	LAG(ch.open,2) OVER (ORDER BY ch.open_time) open_2,
	LAG(ch.high,2) OVER (ORDER BY ch.open_time) high_2,
	LAG(ch.low,2) OVER (ORDER BY ch.open_time) low_2,
	LAG(ch.close,2) OVER (ORDER BY ch.open_time) close_2,
	LAG(ch.open,3) OVER (ORDER BY ch.open_time) open_3,
	LAG(ch.high,3) OVER (ORDER BY ch.open_time) high_3,
	LAG(ch.low,3) OVER (ORDER BY ch.open_time) low_3,
	LAG(ch.close,3) OVER (ORDER BY ch.open_time) close_3,
	LAG(ch.open,4) OVER (ORDER BY ch.open_time) open_4,
	LAG(ch.high,4) OVER (ORDER BY ch.open_time) high_4,
	LAG(ch.low,4) OVER (ORDER BY ch.open_time) low_4,
	LAG(ch.close,4) OVER (ORDER BY ch.open_time) close_4,
	LAG(ch.open,5) OVER (ORDER BY ch.open_time) open_5,
	LAG(ch.high,5) OVER (ORDER BY ch.open_time) high_5,
	LAG(ch.low,5) OVER (ORDER BY ch.open_time) low_5,
	LAG(ch.close,5) OVER (ORDER BY ch.open_time) close_5,
	LAG(ch.open,6) OVER (ORDER BY ch.open_time) open_6,
	LAG(ch.high,6) OVER (ORDER BY ch.open_time) high_6,
	LAG(ch.low,6) OVER (ORDER BY ch.open_time) low_6,
	LAG(ch.close,6) OVER (ORDER BY ch.open_time) close_6,
	LAG(ch.open,7) OVER (ORDER BY ch.open_time) open_7,
	LAG(ch.high,7) OVER (ORDER BY ch.open_time) high_7,
	LAG(ch.low,7) OVER (ORDER BY ch.open_time) low_7,
	LAG(ch.close,7) OVER (ORDER BY ch.open_time) close_7,
	LAG(ch.open,8) OVER (ORDER BY ch.open_time) open_8,
	LAG(ch.high,8) OVER (ORDER BY ch.open_time) high_8,
	LAG(ch.low,8) OVER (ORDER BY ch.open_time) low_8,
	LAG(ch.close,8) OVER (ORDER BY ch.open_time) close_8,
	LAG(ch.open,9) OVER (ORDER BY ch.open_time) open_9,
	LAG(ch.high,9) OVER (ORDER BY ch.open_time) high_9,
	LAG(ch.low,9) OVER (ORDER BY ch.open_time) low_9,
	LAG(ch.close,9) OVER (ORDER BY ch.open_time) close_9,
	LAG(ch.open,10) OVER (ORDER BY ch.open_time) open_10,
	LAG(ch.high,10) OVER (ORDER BY ch.open_time) high_10,
	LAG(ch.low,10) OVER (ORDER BY ch.open_time) low_10,
	LAG(ch.close,10) OVER (ORDER BY ch.open_time) close_10,
	LAG(ch.open,11) OVER (ORDER BY ch.open_time) open_11,
	LAG(ch.high,11) OVER (ORDER BY ch.open_time) high_11,
	LAG(ch.low,11) OVER (ORDER BY ch.open_time) low_11,
	LAG(ch.close,11) OVER (ORDER BY ch.open_time) close_11,
	LAG(ch.open,12) OVER (ORDER BY ch.open_time) open_12,
	LAG(ch.high,12) OVER (ORDER BY ch.open_time) high_12,
	LAG(ch.low,12) OVER (ORDER BY ch.open_time) low_12,
	LAG(ch.close,12) OVER (ORDER BY ch.open_time) close_12,
	LAG(ch.open,13) OVER (ORDER BY ch.open_time) open_13,
	LAG(ch.high,13) OVER (ORDER BY ch.open_time) high_13,
	LAG(ch.low,13) OVER (ORDER BY ch.open_time) low_13,
	LAG(ch.close,13) OVER (ORDER BY ch.open_time) close_13,
	LAG(ch.open,14) OVER (ORDER BY ch.open_time) open_14,
	LAG(ch.high,14) OVER (ORDER BY ch.open_time) high_14,
	LAG(ch.low,14) OVER (ORDER BY ch.open_time) low_14,
	LAG(ch.close,14) OVER (ORDER BY ch.open_time) close_14,
	AVG(ch.close) OVER(ORDER BY ch.open_time ROWS BETWEEN 13 PRECEDING AND CURRENT ROW) AS ma14,
	AVG(ch.close) OVER(ORDER BY ch.open_time ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS ma30,
	AVG(ch.close) OVER(ORDER BY ch.open_time ROWS BETWEEN 89 PRECEDING AND CURRENT ROW) AS ma90,
	atr_all.atr,
	atr_all.atr_diff,
	atr_all.atr_ma14,
	rsi_all.ema_up,
	rsi_all.ema_down,
	rsi_all.rsi,
	rsi_all.rsi_diff,
	rsi_all.rsi_ma14
from ch inner join atr_all on ch.pair_id = atr_all.pair_id inner join rsi_all on ch.pair_id = rsi_all.pair_id
into
	new.open_1, new.high_1, new.low_1, new.close_1, new.open_2, new.high_2, new.low_2, new.close_2, new.open_3, new.high_3, new.low_3, new.close_3, new.open_4, new.high_4, new.low_4, new.close_4,
	new.open_5, new.high_5, new.low_5, new.close_5, new.open_6, new.high_6, new.low_6, new.close_6, new.open_7, new.high_7, new.low_7, new.close_7, new.open_8, new.high_8, new.low_8, new.close_8,
	new.open_9, new.high_9, new.low_9, new.close_9, new.open_10, new.high_10, new.low_10, new.close_10, new.open_11, new.high_11, new.low_11, new.close_11, new.open_12, new.high_12, new.low_12, new.close_12,
	new.open_13, new.high_13, new.low_13, new.close_13, new.open_14, new.high_14, new.low_14, new.close_14,
	new.ma14, new.ma30, new.ma90,
	new.atr, new.atr_diff, new.atr_ma14,
	new.ema_up, new.ema_down, new.rsi, new.rsi_diff, new.rsi_ma14
order by ch.open_time desc
limit 1;

		return new;
    end;
$function$
;




CREATE OR REPLACE FUNCTION public.trigger_set_timestamp()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$function$
;

