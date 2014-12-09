CREATE TABLE player_projections
(
  player_id character varying(10) NOT NULL,
  team_id character varying(3) NOT NULL,
  gsis_id character varying(10) NOT NULL,
  points double precision DEFAULT 0,
  CONSTRAINT player_id_pk PRIMARY KEY (player_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE player_projections
  OWNER TO nfldb;
