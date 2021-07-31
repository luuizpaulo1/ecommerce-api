CREATE TABLE IF NOT EXISTS public.clients
(
    id uuid NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    name character varying(255) COLLATE pg_catalog."default",
    birth_date date,
    document character varying(14) COLLATE pg_catalog."default",
    deleted boolean,
    CONSTRAINT clients_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.orders
(
    id uuid NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    client_id uuid,
    status character varying(50) COLLATE pg_catalog."default",
    total_amount integer,
    products jsonb,
    deleted boolean,
    CONSTRAINT orders_pkey PRIMARY KEY (id),
    CONSTRAINT orders_client_id_fkey FOREIGN KEY (client_id)
        REFERENCES public.clients (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS public.products
(
    id character varying(255) COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    name character varying(255) COLLATE pg_catalog."default",
    description character varying(255) COLLATE pg_catalog."default",
    unit_price integer,
    deleted boolean,
    CONSTRAINT products_pkey PRIMARY KEY (id)
);