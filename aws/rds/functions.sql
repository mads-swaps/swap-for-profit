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
	rsi_all.rsi_ma14,
		extract(dow FROM ch.open_time) as dow,
	mod(cast(extract(epoch FROM ch.open_time) / 86400 as numeric), 1) as tod,
	ch.close - LAG(ch.close,1) over (partition by ch.pair_id order by ch.open_time) > 0 as trend_up,
	(AVG(ch.close) over (partition by ch.pair_id order by ch.open_time rows between 2 preceding and current row)  - AVG(ch.close) over (partition by ch.pair_id order by ch.open_time rows between 3 preceding and 1 preceding)) > 0 as trend_up3,
	(AVG(ch.close) over (partition by ch.pair_id order by ch.open_time rows between 13 preceding and current row)  - AVG(ch.close) over (partition by ch.pair_id order by ch.open_time rows between 14 preceding and 1 preceding)) > 0 as trend_up14,
	(AVG(ch.close) over (partition by ch.pair_id order by ch.open_time rows between 29 preceding and current row)  - AVG(ch.close) over (partition by ch.pair_id order by ch.open_time rows between 30 preceding and 1 preceding)) > 0 as trend_up30,
	(ch.open <= ch.close) and (ch.low + 0.382*(ch.high-ch.low) >= ch.close) as cs_ss,
	(ch.open > ch.close) and (ch.low + 0.382*(ch.high-ch.low) >= ch.open) as cs_ssR,
	(ch.open >= ch.close) and (ch.high - 0.382*(ch.high-ch.low) <= ch.close) as cs_hm,
	(ch.open < ch.close) and (ch.high - 0.382*(ch.high-ch.low) <= ch.open) as cs_hmR,
	(ch.open > ch.close) and
		(LAG(ch.open,1) over (partition by ch.pair_id order by ch.open_time) < LAG(ch.close,1) over (partition by ch.pair_id order by ch.open_time)) and
		(LAG(ch.close,1) over (partition by ch.pair_id order by ch.open_time) >= ch.open) and
		(LAG(ch.open,1) over (partition by ch.pair_id order by ch.open_time) <= ch.close) and
		(LAG(ch.high,1) over (partition by ch.pair_id order by ch.open_time) >= ch.high) and
		(LAG(ch.high,1) over (partition by ch.pair_id order by ch.open_time) <= ch.low) as cs_brh,
	(ch.open < ch.close) and
		(LAG(ch.open,1) over (partition by ch.pair_id order by ch.open_time) > LAG(ch.close,1) over (partition by ch.pair_id order by ch.open_time)) and
		(LAG(ch.close,1) over (partition by ch.pair_id order by ch.open_time) <= ch.open) and
		(LAG(ch.open,1) over (partition by ch.pair_id order by ch.open_time) > ch.close) and
		(LAG(ch.high,1) over (partition by ch.pair_id order by ch.open_time) >= ch.high) and
		(LAG(ch.high,1) over (partition by ch.pair_id order by ch.open_time) <= ch.low) as cs_buh,
	(ch.open < ch.close) and 
		(LAG(ch.open,1) over (partition by ch.pair_id order by ch.open_time) > LAG(ch.close,1) over (partition by ch.pair_id order by ch.open_time)) and
		(LAG(ch.close,1) over (partition by ch.pair_id order by ch.open_time) >= ch.open) and
		(LAG(ch.open,1) over (partition by ch.pair_id order by ch.open_time) <= ch.close) and
		(LAG(ch.high,1) over (partition by ch.pair_id order by ch.open_time) <= ch.high) and
		(LAG(ch.high,1) over (partition by ch.pair_id order by ch.open_time) >= ch.low) as cs_ebu,
	(ch.open > ch.close) and 
		(LAG(ch.open,1) over (partition by ch.pair_id order by ch.open_time) < LAG(ch.close,1) over (partition by ch.pair_id order by ch.open_time)) and
		(LAG(ch.close,1) over (partition by ch.pair_id order by ch.open_time) <= ch.open) and
		(LAG(ch.open,1) over (partition by ch.pair_id order by ch.open_time) >= ch.close) and
		(LAG(ch.high,1) over (partition by ch.pair_id order by ch.open_time) <= ch.high) and
		(LAG(ch.high,1) over (partition by ch.pair_id order by ch.open_time) >= ch.low) as cs_ebr
from ch inner join atr_all on ch.pair_id = atr_all.pair_id inner join rsi_all on ch.pair_id = rsi_all.pair_id
into
	new.ma14, new.ma30, new.ma90,
	new.atr, new.atr_diff, new.atr_ma14,
	new.ema_up, new.ema_down, new.rsi, new.rsi_diff, new.rsi_ma14,
	new.dow, new.tod,
	new.trend_up, new.trend_up3, new.trend_up14, new.trend_up30,
	new.cs_ss, new.cs_ssR, new.cs_hm, new.cs_hmR,
	new.cs_brh, new.cs_buh, new.cs_ebu, new.cs_ebr
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

