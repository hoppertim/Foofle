-- Table: fantasy_prev

-- DROP TABLE fantasy_prev;

CREATE TABLE fantasy_prev
(
  fantasy_id serial NOT NULL,
  gsis_id gameid NOT NULL,
  team_id character varying(3) NOT NULL,
  player_id character varying(10),
  prev_amount character varying(10),
  "position" player_pos NOT NULL DEFAULT 'UNK'::player_pos,
  pass_att real DEFAULT 0,
  pass_cmp real DEFAULT 0,
  pass_yds real DEFAULT 0,
  pass_tds real DEFAULT 0,
  "int" real DEFAULT 0,
  rush_att real DEFAULT 0,
  rush_yds real DEFAULT 0,
  fumble real DEFAULT 0,
  targets real DEFAULT 0,
  rec real DEFAULT 0,
  rec_yds real DEFAULT 0,
  yac real DEFAULT 0,
  ret_yds real DEFAULT 0,
  td real DEFAULT 0,
  block_kick real DEFAULT 0,
  safety real DEFAULT 0,
  sack real DEFAULT 0,
  pts_allowed real DEFAULT 0,
  fg_50 real DEFAULT 0,
  fg_40 real DEFAULT 0,
  fg_0 real DEFAULT 0,
  pat real DEFAULT 0,
  fg_miss real DEFAULT 0,
  points real NOT NULL DEFAULT 0,
  CONSTRAINT fantasy_prev_pkey PRIMARY KEY (fantasy_id),
  CONSTRAINT fantasy_prev_fk_game FOREIGN KEY (gsis_id)
      REFERENCES game (gsis_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fantasy_prev_fk_player FOREIGN KEY (player_id)
      REFERENCES player (player_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fantasy_prev_fk_team FOREIGN KEY (team_id)
      REFERENCES team (team_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE fantasy_prev
  OWNER TO nfldb;

-- Index: fantasy_prev_in_pk

-- DROP INDEX fantasy_prev_in_pk;

CREATE UNIQUE INDEX fantasy_prev_in_pk
  ON fantasy_prev
  USING btree
  (fantasy_id);

-- Index: fantasy_prev_in_player_nuc

-- DROP INDEX fantasy_prev_in_player_nuc;

CREATE INDEX fantasy_prev_in_player_nuc
  ON fantasy_prev
  USING btree
  (player_id COLLATE pg_catalog."default");
ALTER TABLE fantasy_prev CLUSTER ON fantasy_prev_in_player_nuc;

-- Index: fki_fantasy_prev_fk_game

-- DROP INDEX fki_fantasy_prev_fk_game;

CREATE INDEX fki_fantasy_prev_fk_game
  ON fantasy_prev
  USING btree
  (gsis_id COLLATE pg_catalog."default");

-- Index: fki_fantasy_prev_fk_player

-- DROP INDEX fki_fantasy_prev_fk_player;

CREATE INDEX fki_fantasy_prev_fk_player
  ON fantasy_prev
  USING btree
  (player_id COLLATE pg_catalog."default");

-- Index: fki_fantasy_prev_fk_team

-- DROP INDEX fki_fantasy_prev_fk_team;

CREATE INDEX fki_fantasy_prev_fk_team
  ON fantasy_prev
  USING btree
  (team_id COLLATE pg_catalog."default");

