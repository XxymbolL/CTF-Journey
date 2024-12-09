import { randomUUIDv7 } from "bun";
import { Elysia } from "elysia";
import { user } from "./user";
import { survey } from "./survey";

const app = new Elysia({
  cookie: {
    secrets: randomUUIDv7(),
    sign: ["profile"],
  },
})
  .use(user)
  .use(survey)
  .listen(3000);

console.log(
  `🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`
);
