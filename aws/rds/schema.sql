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
	column1 int4 NULL,
	CONSTRAINT candlestick_15m_pair_open_time_key UNIQUE (pair_id, open_time),
	CONSTRAINT candlestick_15m_pk PRIMARY KEY (pair_id, open_time),
	CONSTRAINT candlestick_15m_fk FOREIGN KEY (pair_id) REFERENCES public.pairs(id)
);
CREATE INDEX candlestick_15m_open_time_idx ON public.candlestick_15m USING btree (open_time);

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




-- Drop table

-- DROP TABLE public.features;

CREATE UNLOGGED TABLE public.features (
	pair_id int2 NOT NULL,
	candle_open_time timestamp NOT NULL,
	ma14 numeric(20, 8) NULL,
	ma30 numeric(20, 8) NULL,
	ma90 numeric(20, 8) NULL,
	atr numeric(40, 28) NULL,
	atr_diff numeric(40, 28) NULL,
	atr_ma14 numeric(40, 28) NULL,
	ema_up numeric(40, 28) NULL,
	ema_down numeric(40, 28) NULL,
	rsi numeric(40, 28) NULL,
	rsi_diff numeric(40, 28) NULL,
	rsi_ma14 numeric(40, 28) NULL,
	trend_up bool NULL,
	trend_up3 bool NULL,
	trend_up14 bool NULL,
	trend_up30 bool NULL,
	cs_ss bool NULL,
	cs_ssr bool NULL,
	cs_hm bool NULL,
	cs_hmr bool NULL,
	cs_brh bool NULL,
	cs_buh bool NULL,
	cs_ebu bool NULL,
	cs_ebr bool NULL,
	dow int2 NULL,
	tod numeric(9, 8) NULL,
	sup14 numeric(20, 8) NULL,
	sup30 numeric(20, 8) NULL,
	sup90 numeric(20, 8) NULL,
	res14 numeric(20, 8) NULL,
	res30 numeric(20, 8) NULL,
	res90 numeric(20, 8) NULL,
	CONSTRAINT features_pair_open_time_key UNIQUE (pair_id, candle_open_time),
	CONSTRAINT features_pk PRIMARY KEY (pair_id, candle_open_time),
	CONSTRAINT features_fk FOREIGN KEY (pair_id) REFERENCES public.pairs(id)
);
CREATE INDEX features_candle_open_time_idx ON public.features USING btree (candle_open_time);

-- Table Triggers

create trigger feature_engineering before
insert
    on
    public.features for each row execute function feature_engineering();






-- Drop table

-- DROP TABLE public.environment;

CREATE TABLE public.environment (
	id int4 NOT NULL DEFAULT nextval('simulation_configs_id_seq'::regclass),
	starting_timestamp timestamp NOT NULL,
	starting_funds numeric(20, 8) NOT NULL,
	trading_fees_percent numeric(20, 8) NOT NULL,
	trading_fees_buy numeric(20, 8) NOT NULL,
	trading_fees_sell numeric(20, 8) NOT NULL,
	"name" varchar NOT NULL,
	pair_id int2 NOT NULL,
	CONSTRAINT simulation_configs_pkey PRIMARY KEY (id),
	CONSTRAINT environment_fk FOREIGN KEY (pair_id) REFERENCES public.pairs(id)
);
CREATE INDEX simulation_configs_id_idx ON public.environment USING btree (id);






-- Drop table

-- DROP TABLE public.strategy;

CREATE TABLE public.strategy (
	id serial NOT NULL,
	strategy_name varchar(200) NOT NULL,
	model varchar(200) NOT NULL,
	max_batch_size int4 NOT NULL,
	extra_rows int4 NOT NULL,
	parameters jsonb NULL,
	CONSTRAINT strategy_pkey PRIMARY KEY (id)
);






-- Drop table

-- DROP TABLE public.simulation;

CREATE TABLE public.simulation (
	id serial NOT NULL,
	strategy_id int4 NOT NULL,
	environment_id int4 NOT NULL,
	info_dict jsonb NULL DEFAULT '{}'::jsonb,
	CONSTRAINT simulation_pkey PRIMARY KEY (id),
	CONSTRAINT simulation_un UNIQUE (strategy_id, environment_id),
	CONSTRAINT simulation_fk FOREIGN KEY (strategy_id) REFERENCES public.strategy(id),
	CONSTRAINT simulation_fk_1 FOREIGN KEY (environment_id) REFERENCES public.environment(id)
);





-- Drop table

-- DROP TABLE public.simulation_record;

CREATE TABLE public.simulation_record (
	simulation_id int4 NOT NULL,
	open_time timestamp NOT NULL,
	trade_action varchar(4) NOT NULL,
	execute_price numeric(20, 8) NOT NULL,
	fund1 numeric(40, 28) NOT NULL,
	fund2 numeric(40, 28) NOT NULL,
	total_value numeric(40, 28) NOT NULL,
	CONSTRAINT simulation_record_un UNIQUE (simulation_id, open_time),
	CONSTRAINT simulation_record_fk FOREIGN KEY (simulation_id) REFERENCES public.simulation(id)
);
CREATE INDEX simulation_record_open_time_idx ON public.simulation_record USING btree (open_time);
CREATE UNIQUE INDEX simulation_record_simulation_id_idx ON public.simulation_record USING btree (simulation_id, open_time);
CREATE INDEX simulation_record_trade_action_idx ON public.simulation_record USING btree (trade_action);






