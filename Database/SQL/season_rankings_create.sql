-- Table: season_rankings

-- DROP TABLE season_rankings;

CREATE TABLE season_rankings
(
  season_ranking_id serial NOT NULL,
  season_year smallint NOT NULL,
  team_id character varying(3) NOT NULL,
  off_pts double precision NOT NULL,
  off_pass_yds double precision,
  off_pass_tds double precision,
  off_rush_yds double precision,
  off_rush_tds double precision,
  off_int double precision,
  off_fumble double precision,
  off_sack double precision,
  def_pts double precision NOT NULL,
  def_pass_yds double precision,
  def_pass_tds double precision,
  def_rush_yds double precision,
  def_rush_tds double precision,
  def_int double precision,
  def_fumble double precision,
  def_sack double precision,
  def_block double precision,
  def_safety double precision,
  def_tds double precision,
  avg boolean,
  CONSTRAINT season_rankings_pkey PRIMARY KEY (season_ranking_id),
  CONSTRAINT team_id FOREIGN KEY (team_id)
      REFERENCES team (team_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE season_rankings
  OWNER TO nfldb;

-- Index: fki_team_id

-- DROP INDEX fki_team_id;

CREATE INDEX fki_team_id
  ON season_rankings
  USING btree
  (team_id COLLATE pg_catalog."default");

-- Index: season_rankings_in_season_year_team_id_nuc

-- DROP INDEX season_rankings_in_season_year_team_id_nuc;

CREATE INDEX season_rankings_in_season_year_team_id_nuc
  ON season_rankings
  USING btree
  (season_year, team_id COLLATE pg_catalog."default");
ALTER TABLE season_rankings CLUSTER ON season_rankings_in_season_year_team_id_nuc;

