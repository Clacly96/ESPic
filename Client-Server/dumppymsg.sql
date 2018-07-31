--
-- PostgreSQL database dump
--

-- Dumped from database version 10.4
-- Dumped by pg_dump version 10.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: messaggi; Type: TABLE; Schema: public; Owner: calcolatori
--

CREATE TABLE public.messaggi (
    mittente character varying(20),
    destinatario character varying(20),
    testo character varying(500),
    letto boolean,
    data timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    id integer NOT NULL
);


ALTER TABLE public.messaggi OWNER TO calcolatori;

--
-- Name: messaggi_id_seq; Type: SEQUENCE; Schema: public; Owner: calcolatori
--

CREATE SEQUENCE public.messaggi_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.messaggi_id_seq OWNER TO calcolatori;

--
-- Name: messaggi_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: calcolatori
--

ALTER SEQUENCE public.messaggi_id_seq OWNED BY public.messaggi.id;


--
-- Name: messaggi id; Type: DEFAULT; Schema: public; Owner: calcolatori
--

ALTER TABLE ONLY public.messaggi ALTER COLUMN id SET DEFAULT nextval('public.messaggi_id_seq'::regclass);S


--
-- Name: messaggi_id_seq; Type: SEQUENCE SET; Schema: public; Owner: calcolatori
--

SELECT pg_catalog.setval('public.messaggi_id_seq', 1, true);


--
-- PostgreSQL database dump complete
--

