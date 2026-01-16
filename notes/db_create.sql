CREATE TABLE "users" (
  "id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "username" text UNIQUE NOT NULL,
  "password" text NOT NULL
);

CREATE TYPE status AS ENUM ('won', 'lost', 'ongoing');

CREATE TABLE "words" (
  "id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "word" varchar(5) NOT NULL,
  "date" DATE UNIQUE NOT NULL
);

CREATE INDEX "idx_words_word" ON "words" ("word");
CREATE INDEX "idx_words_date" ON "words" ("date");

CREATE TABLE "games" (
  "id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "user_id" uuid NOT NULL,
  "date" DATE NOT NULL,
  "word" varchar(5) NOT NULL,
  "attempts" text[][] NOT NULL DEFAULT ARRAY[]::text[][],
  "remaining_attempts" int NOT NULL DEFAULT 6,
  "game_status" status NOT NULL DEFAULT 'ongoing',
  CONSTRAINT "unique_user_game_per_day" UNIQUE ("user_id", "date")
);

CREATE INDEX "idx_games_date" ON "games" ("date");

ALTER TABLE "games" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");