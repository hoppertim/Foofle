-- Table: fantasy

-- DROP TABLE fantasy;

CREATE TABLE fantasy
(
  fantasy_id serial NOT NULL,
  gsis_id gameid NOT NULL,
  team_id character varying(3) NOT NULL,
  player_id character varying(10),
  "position" player_pos NOT NULL DEFAULT 'UNK'::player_pos,
  pass_att integer DEFAULT 0,
  pass_cmp integer DEFAULT 0,
  pass_yds integer DEFAULT 0,
  pass_tds integer DEFAULT 0,
  "int" integer DEFAULT 0,
  rush_att integer DEFAULT 0,
  rush_yds integer DEFAULT 0,
  fumble integer DEFAULT 0,
  targets integer DEFAULT 0,
  rec integer DEFAULT 0,
  rec_yds integer DEFAULT 0,
  yac integer DEFAULT 0,
  ret_yds integer DEFAULT 0,
  td integer DEFAULT 0,
  block_kick integer DEFAULT 0,
  safety integer DEFAULT 0,
  sack integer DEFAULT 0,
  pts_allowed integer DEFAULT 0,
  fg_50 integer DEFAULT 0,
  fg_40 integer DEFAULT 0,
  fg_0 integer DEFAULT 0,
  pat integer DEFAULT 0,
  fg_miss integer DEFAULT 0,
  points real NOT NULL DEFAULT 0,
  CONSTRAINT fantasy_pkey PRIMARY KEY (fantasy_id),
  CONSTRAINT fantasy_fk_game FOREIGN KEY (gsis_id)
      REFERENCES game (gsis_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fantasy_fk_player FOREIGN KEY (player_id)
      REFERENCES player (player_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fantasy_fk_team FOREIGN KEY (team_id)
      REFERENCES team (team_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE fantasy
  OWNER TO nfldb;

-- Index: fantasy_in_pk

-- DROP INDEX fantasy_in_pk;

CREATE UNIQUE INDEX fantasy_in_pk
  ON fantasy
  USING btree
  (fantasy_id);

-- Index: fantasy_in_player_nuc

-- DROP INDEX fantasy_in_player_nuc;

CREATE INDEX fantasy_in_player_nuc
  ON fantasy
  USING btree
  (player_id COLLATE pg_catalog."default");
ALTER TABLE fantasy CLUSTER ON fantasy_in_player_nuc;

-- Index: fki_fantasy_fk_game

-- DROP INDEX fki_fantasy_fk_game;

CREATE INDEX fki_fantasy_fk_game
  ON fantasy
  USING btree
  (gsis_id COLLATE pg_catalog."default");

-- Index: fki_fantasy_fk_player

-- DROP INDEX fki_fantasy_fk_player;

CREATE INDEX fki_fantasy_fk_player
  ON fantasy
  USING btree
  (player_id COLLATE pg_catalog."default");

-- Index: fki_fantasy_fk_team

-- DROP INDEX fki_fantasy_fk_team;

CREATE INDEX fki_fantasy_fk_team
  ON fantasy
  USING btree
  (team_id COLLATE pg_catalog."default");

