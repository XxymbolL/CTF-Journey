import Elysia, { redirect, t } from "elysia";
import { prisma } from "./db";
import html from "@elysiajs/html";

const index = await Bun.file("html/index.html").text();

export const survey = new Elysia()
  .use(html())
  .get(
    "/",
    ({ cookie }) => {
      if (!cookie.profile.value) return redirect("/sign-in");
      return index.replace("{{USERNAME}}", cookie.profile.value.username);
    },
    {
      cookie: t.Cookie({
        profile: t.Optional(
          t.Object({
            id: t.Numeric(),
            username: t.String(),
            isAdmin: t.Boolean(),
          })
        ),
      }),
    }
  )
  .post(
    "/",
    async ({ cookie: { profile }, body }) => {
      console.log({
        user: {
          connect: {
            id: profile.value.id,
          },
        },
        ...body,
      });
      await prisma.survey.create({
        data: {
          user: {
            connect: {
              id: profile.value.id,
            },
          },
          ...body,
        },
      });

      return "Done";
    },
    {
      body: t.Object(
        {
          result: t.Numeric(),
        },
        { additionalProperties: true }
      ),
      cookie: t.Cookie({
        profile: t.Object({
          id: t.Numeric(),
          username: t.String(),
          isAdmin: t.Boolean(),
        }),
      }),
    }
  );
