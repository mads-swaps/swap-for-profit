-- public.pairs definition

-- Drop table

-- DROP TABLE public.pairs;

CREATE TABLE public.pairs (
	id int2 NOT NULL,
	symbol varchar NOT NULL,
	coin1 varchar NOT NULL,
	coin2 varchar NOT NULL,
	CONSTRAINT pairs_pk PRIMARY KEY (id)
);




-- public.candlestick_15m definition

-- Drop table

-- DROP TABLE public.candlestick_15m;

CREATE TABLE public.candlestick_15m (
	pair_id int2 NOT NULL,
	open_time timestamp NOT NULL,
	"open" numeric(20, 8) NOT NULL,
	high numeric(20, 8) NOT NULL,
	low numeric(20, 8) NOT NULL,
	"close" numeric(20, 8) NOT NULL,
	volume numeric(20, 8) NOT NULL,
	close_time timestamp NULL,
	quote_asset_volume numeric(20, 8) NOT NULL,
	number_of_trades int4 NOT NULL,
	taker_buy_base_asset_volume numeric(20, 8) NOT NULL,
	taker_buy_quote_asset_volume numeric(20, 8) NOT NULL,
	created_at timestamptz NOT NULL DEFAULT now(),
	updated_at timestamptz NOT NULL DEFAULT now(),
	CONSTRAINT candlestick_15m_pair_open_time_key UNIQUE (pair_id, open_time)
);

-- Table Triggers

create trigger set_timestamp before
update
    on
    public.candlestick_15m for each row execute function trigger_set_timestamp();
create trigger create_feature after
insert
    or
update
    on
    public.candlestick_15m for each row execute function create_feature();


-- public.candlestick_15m foreign keys

ALTER TABLE public.candlestick_15m ADD CONSTRAINT candlestick_15m_fk FOREIGN KEY (pair_id) REFERENCES public.pairs(id);









-- public.features definition

-- Drop table

-- DROP TABLE public.features;

CREATE UNLOGGED TABLE public.features (
	pair_id int2 NOT NULL,
	candle_open_time timestamp NOT NULL,
	open_1 numeric(20, 8) NULL,
	high_1 numeric(20, 8) NULL,
	low_1 numeric(20, 8) NULL,
	close_1 numeric(20, 8) NULL,
	open_2 numeric(20, 8) NULL,
	high_2 numeric(20, 8) NULL,
	low_2 numeric(20, 8) NULL,
	close_2 numeric(20, 8) NULL,
	open_3 numeric(20, 8) NULL,
	high_3 numeric(20, 8) NULL,
	low_3 numeric(20, 8) NULL,
	close_3 numeric(20, 8) NULL,
	ma14 numeric(20, 8) NULL,
	ma30 numeric(20, 8) NULL,
	ma90 numeric(20, 8) NULL,
	atr numeric(40, 28) NULL,
	atr_diff numeric(40, 28) NULL,
	atr_ma14 numeric(40, 28) NULL,
	open_4 numeric(20, 8) NULL,
	high_4 numeric(20, 8) NULL,
	low_4 numeric(20, 8) NULL,
	close_4 numeric(20, 8) NULL,
	open_5 numeric(20, 8) NULL,
	high_5 numeric(20, 8) NULL,
	low_5 numeric(20, 8) NULL,
	close_5 numeric(20, 8) NULL,
	open_6 numeric(20, 8) NULL,
	high_6 numeric(20, 8) NULL,
	low_6 numeric(20, 8) NULL,
	close_6 numeric(20, 8) NULL,
	open_7 numeric(20, 8) NULL,
	high_7 numeric(20, 8) NULL,
	low_7 numeric(20, 8) NULL,
	close_7 numeric(20, 8) NULL,
	open_8 numeric(20, 8) NULL,
	high_8 numeric(20, 8) NULL,
	low_8 numeric(20, 8) NULL,
	close_8 numeric(20, 8) NULL,
	open_9 numeric(20, 8) NULL,
	high_9 numeric(20, 8) NULL,
	low_9 numeric(20, 8) NULL,
	close_9 numeric(20, 8) NULL,
	open_10 numeric(20, 8) NULL,
	high_10 numeric(20, 8) NULL,
	low_10 numeric(20, 8) NULL,
	close_10 numeric(20, 8) NULL,
	open_11 numeric(20, 8) NULL,
	high_11 numeric(20, 8) NULL,
	low_11 numeric(20, 8) NULL,
	close_11 numeric(20, 8) NULL,
	open_12 numeric(20, 8) NULL,
	high_12 numeric(20, 8) NULL,
	low_12 numeric(20, 8) NULL,
	close_12 numeric(20, 8) NULL,
	open_13 numeric(20, 8) NULL,
	high_13 numeric(20, 8) NULL,
	low_13 numeric(20, 8) NULL,
	close_13 numeric(20, 8) NULL,
	open_14 numeric(20, 8) NULL,
	high_14 numeric(20, 8) NULL,
	low_14 numeric(20, 8) NULL,
	close_14 numeric(20, 8) NULL,
	ema_up numeric(40, 28) NULL,
	ema_down numeric(40, 28) NULL,
	rsi numeric(40, 28) NULL,
	rsi_diff numeric(40, 28) NULL,
	rsi_ma14 numeric(40, 28) NULL,
	CONSTRAINT features_pair_open_time_key UNIQUE (pair_id, candle_open_time)
);

-- Table Triggers

create trigger feature_engineering before
insert
    on
    public.features for each row execute function feature_engineering();


-- public.features foreign keys

ALTER TABLE public.features ADD CONSTRAINT features_fk FOREIGN KEY (pair_id) REFERENCES public.pairs(id);