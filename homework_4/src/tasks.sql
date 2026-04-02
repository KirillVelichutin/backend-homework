CREATE TABLE "users" (
  "id" serial PRIMARY KEY,
  "username" varchar(20) UNIQUE NOT NULL,
  "email" varchar(50) UNIQUE NOT NULL,
  "hashed_password" text NOT NULL
);

CREATE TABLE "tasks" (
  "id" serial PRIMARY KEY,
  "name" varchar(35) NOT NULL,
  "about" varchar(100),
  "importance" varchar(20) NOT NULL,
  "author_id" integer NOT NULL,
  "responsible_id" integer NOT NULL,
  "deadline" date NOT NULL,
  "is_done" boolean NOT NULL DEFAULT FALSE
);

CREATE TABLE "comments" (
  "id" serial PRIMARY KEY,
  "task_id" integer NOT NULL,
  "author_id" integer NOT NULL,
  "text" varchar(300) NOT NULL,
  "created_at" timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE "tasks" ADD FOREIGN KEY ("author_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "tasks" ADD FOREIGN KEY ("responsible_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "comments" ADD FOREIGN KEY ("task_id") REFERENCES "tasks" ("id") ON DELETE CASCADE DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "comments" ADD FOREIGN KEY ("author_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;
