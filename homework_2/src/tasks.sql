CREATE TABLE "users" (
  "id" serial PRIMARY KEY,
  "username" varchar(20),
  "email" varchar(50),
  "password" text
);

CREATE TABLE "tasks" (
  "id" serial PRIMARY KEY,
  "name" varchar(35),
  "about" varchar(100),
  "importance" varchar(20),
  "responsible" varchar(20),
  "deadline" date,
  "done" bool
);

ALTER TABLE "tasks" ADD FOREIGN KEY ("responsible") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;