CREATE TABLE IF NOT EXISTS public.docs
(
    title text NOT NULL,
    dataset text NOT NULL,
    id bigserial NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE public.docs
    OWNER to postgres;

CREATE TABLE IF NOT EXISTS public.token_tags
(
    document_id integer,
    sentence_id integer,
    text text,
    lemma text,
    upos text,
    xpos text,
    feats text,
    head integer,
    deprel text,
    start_char integer,
    end_char integer,
    ner text,
    model text
);

ALTER TABLE public.token_tags
    OWNER to postgres;


CREATE TABLE IF NOT EXISTS public.embedding
(
    abstraction_level integer,
    document_id integer,
    sentence_id integer,
    token_id integer,
    model text,
    tensor integer[]
);

ALTER TABLE public.embedding
    OWNER to postgres;