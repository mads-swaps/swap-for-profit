CREATE TABLE public.pairs (
	id int2 NOT NULL,
	symbol varchar NOT NULL,
	coin1 varchar NOT NULL,
	coin2 varchar NOT NULL,
	CONSTRAINT pairs_pk PRIMARY KEY (id)
);

CREATE TABLE public.candlestick_15m (
	pair_id int2 NOT NULL,
	open_time timestamp NOT NULL,
	"open" numeric(20, 8) NOT NULL,
	high numeric(20, 8) NOT NULL,
	low numeric(20, 8) NOT NULL,
	"close" numeric(20, 8) NOT NULL,
	volume numeric(20, 8) NOT NULL,
	close_time timestamp NOT NULL,
	quote_asset_volume numeric(20, 8) NOT NULL,
	number_of_trades int4 NOT NULL,
	taker_buy_base_asset_volume numeric(20, 8) NOT NULL,
	taker_buy_quote_asset_volume numeric(20, 8) NOT NULL,
	created_at timestamptz NOT NULL DEFAULT now(),
	CONSTRAINT candlestick_15m_pair_open_time_key UNIQUE (pair_id, open_time),
	CONSTRAINT candlestick_15m_fk FOREIGN KEY (pair_id) REFERENCES public.pairs(id)
);
CREATE UNIQUE INDEX candlestick_15m_pair_id_idx ON public.candlestick_15m USING btree (pair_id, open_time);
