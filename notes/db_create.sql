CREATE TABLE "users" (
  "id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "email" text UNIQUE NOT NULL,
  "password" text NOT NULL
);

CREATE TYPE status AS ENUM ('won', 'lost', 'ongoing');

CREATE TABLE "games" (
  "id" uuid PRIMARY KEY DEFAULT (gen_random_uuid()),
  "user_id" uuid,
  "word" varchar(5) NOT NULL,
  "attempts" text[6][2] NOT NULL DEFAULT ARRAY[]::text[6][2],
  "remaining_attempts" int NOT NULL DEFAULT 6,
  "game_status" status NOT NULL DEFAULT ('ongoing')
);

CREATE TABLE "words" (
  "word" varchar(5) PRIMARY KEY
);

ALTER TABLE "games" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "games" ADD FOREIGN KEY ("word") REFERENCES "words" ("word");