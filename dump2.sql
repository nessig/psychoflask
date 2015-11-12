--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5beta1
-- Dumped by pg_dump version 9.5beta1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: posts; Type: TABLE; Schema: public; Owner: nessig
--

CREATE TABLE posts (
    id integer NOT NULL,
    title character varying(30) NOT NULL,
    body character varying(400) NOT NULL,
    pub_date timestamp without time zone,
    author_id integer
);


ALTER TABLE posts OWNER TO nessig;

--
-- Name: posts_id_seq; Type: SEQUENCE; Schema: public; Owner: nessig
--

CREATE SEQUENCE posts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE posts_id_seq OWNER TO nessig;

--
-- Name: posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nessig
--

ALTER SEQUENCE posts_id_seq OWNED BY posts.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: nessig
--

ALTER TABLE ONLY posts ALTER COLUMN id SET DEFAULT nextval('posts_id_seq'::regclass);


--
-- Data for Name: posts; Type: TABLE DATA; Schema: public; Owner: nessig
--

COPY posts (id, title, body, pub_date, author_id) FROM stdin;
1	Post 1	Body of post 1	2015-11-11 02:32:39.672677	1
2	Post 2	Body of post 2\r\n	2015-11-11 02:32:45.946066	1
3	Post 3	Body of post 3\r\n	2015-11-11 02:32:51.005393	1
4	Nolan's post 1	This is post 1	2015-11-11 02:33:50.371871	2
5	Nolan's post 2	This is post 2	2015-11-11 02:33:56.027426	2
6	Nolan's post 3	This is post 3	2015-11-11 02:34:02.035949	2
7	post about cheese	I love cheese!!!! Chedder cheese!!!	2015-11-11 05:04:52.168528	2
\.


--
-- Name: posts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nessig
--

SELECT pg_catalog.setval('posts_id_seq', 7, true);


--
-- Name: posts_pkey; Type: CONSTRAINT; Schema: public; Owner: nessig
--

ALTER TABLE ONLY posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (id);


--
-- Name: posts_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nessig
--

ALTER TABLE ONLY posts
    ADD CONSTRAINT posts_author_id_fkey FOREIGN KEY (author_id) REFERENCES users(id);


--
-- PostgreSQL database dump complete
--

