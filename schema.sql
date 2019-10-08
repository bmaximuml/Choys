--
-- PostgreSQL database dump
--

-- Dumped from database version 11.5 (Ubuntu 11.5-0ubuntu0.19.04.1)
-- Dumped by pg_dump version 11.5 (Ubuntu 11.5-0ubuntu0.19.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY "public"."scores" DROP CONSTRAINT IF EXISTS "scores_location_name_fkey";
ALTER TABLE IF EXISTS ONLY "public"."rental_data" DROP CONSTRAINT IF EXISTS "rental_data_location_name_fkey";
ALTER TABLE IF EXISTS ONLY "public"."distance_matrix_data" DROP CONSTRAINT IF EXISTS "distance_matrix_data_location_name_fkey";
ALTER TABLE IF EXISTS ONLY "public"."scores" DROP CONSTRAINT IF EXISTS "scores_pkey";
ALTER TABLE IF EXISTS ONLY "public"."rental_data" DROP CONSTRAINT IF EXISTS "rental_data_pkey";
ALTER TABLE IF EXISTS ONLY "public"."locations" DROP CONSTRAINT IF EXISTS "locations_pkey";
ALTER TABLE IF EXISTS ONLY "public"."location" DROP CONSTRAINT IF EXISTS "location_pkey";
ALTER TABLE IF EXISTS ONLY "public"."distance_matrix_data" DROP CONSTRAINT IF EXISTS "distance_matrix_data_pkey";
ALTER TABLE IF EXISTS "public"."locations" ALTER COLUMN "id" DROP DEFAULT;
DROP TABLE IF EXISTS "public"."scores";
DROP TABLE IF EXISTS "public"."rental_data";
DROP SEQUENCE IF EXISTS "public"."locations_id_seq";
DROP TABLE IF EXISTS "public"."locations";
DROP TABLE IF EXISTS "public"."location";
DROP TABLE IF EXISTS "public"."distance_matrix_data";
SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: distance_matrix_data; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."distance_matrix_data" (
    "distance_to_london" integer,
    "duration_to_london" integer,
    "distance_to_london_text" character varying(100),
    "duration_to_london_text" character varying(100),
    "datetime" timestamp without time zone NOT NULL,
    "location_name" character varying(500) NOT NULL
);


--
-- Name: location; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."location" (
    "name" character varying(500) NOT NULL
);


--
-- Name: locations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."locations" (
    "id" integer NOT NULL,
    "location_name" character varying(500),
    "total_properties" integer NOT NULL,
    "average_rent" integer,
    "rent_under_250" integer NOT NULL,
    "rent_250_to_500" integer NOT NULL,
    "distance_to_london" integer,
    "duration_to_london" integer,
    "newest" boolean NOT NULL
);


--
-- Name: locations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."locations_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: locations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."locations_id_seq" OWNED BY "public"."locations"."id";


--
-- Name: rental_data; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."rental_data" (
    "total_properties" integer NOT NULL,
    "average_rent" integer,
    "rent_under_250" integer NOT NULL,
    "rent_250_to_500" integer NOT NULL,
    "datetime" timestamp without time zone NOT NULL,
    "location_name" character varying(500) NOT NULL
);


--
-- Name: scores; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."scores" (
    "score" double precision NOT NULL,
    "datetime" timestamp without time zone NOT NULL,
    "location_name" character varying(500) NOT NULL
);


--
-- Name: locations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."locations" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."locations_id_seq"'::"regclass");


--
-- Name: distance_matrix_data distance_matrix_data_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."distance_matrix_data"
    ADD CONSTRAINT "distance_matrix_data_pkey" PRIMARY KEY ("datetime", "location_name");


--
-- Name: location location_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."location"
    ADD CONSTRAINT "location_pkey" PRIMARY KEY ("name");


--
-- Name: locations locations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."locations"
    ADD CONSTRAINT "locations_pkey" PRIMARY KEY ("id");


--
-- Name: rental_data rental_data_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."rental_data"
    ADD CONSTRAINT "rental_data_pkey" PRIMARY KEY ("datetime", "location_name");


--
-- Name: scores scores_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."scores"
    ADD CONSTRAINT "scores_pkey" PRIMARY KEY ("datetime", "location_name");


--
-- Name: distance_matrix_data distance_matrix_data_location_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."distance_matrix_data"
    ADD CONSTRAINT "distance_matrix_data_location_name_fkey" FOREIGN KEY ("location_name") REFERENCES "public"."location"("name");


--
-- Name: rental_data rental_data_location_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."rental_data"
    ADD CONSTRAINT "rental_data_location_name_fkey" FOREIGN KEY ("location_name") REFERENCES "public"."location"("name");


--
-- Name: scores scores_location_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."scores"
    ADD CONSTRAINT "scores_location_name_fkey" FOREIGN KEY ("location_name") REFERENCES "public"."location"("name");


--
-- PostgreSQL database dump complete
--

