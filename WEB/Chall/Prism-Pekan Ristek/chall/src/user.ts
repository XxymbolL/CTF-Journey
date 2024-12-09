import { Elysia, redirect, t } from "elysia";
import { prisma } from "./db";

export const user = new Elysia()
  .get("/sign-in", () => Bun.file("html/login.html"))
  .post(
    "/sign-in",
    async ({ error, body: { username, password }, cookie: { profile } }) => {
      let user = await prisma.user.findFirst({
        where: {
          username: username,
        },
      });

      const hasher = new Bun.CryptoHasher("sha256");
      hasher.update(password);
      const pw = hasher.digest("hex");
      if (!user)
        user = await prisma.user.create({
          data: {
            username,
            password: pw,
          },
        });

      if (user.password != pw)
        return error(400, {
          success: false,
          message: "Invalid username or password",
        });

      profile.value = {
        id: user.id,
        isAdmin: user.isAdmin,
        username: user.username,
      };

      return redirect("/");
    },
    {
      body: t.Object({
        username: t.String({ minLength: 1 }),
        password: t.String({ minLength: 8 }),
      }),
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
  .get(
    "/admin",
    ({ cookie: { profile } }) => {
      if (!profile.value?.isAdmin) return "Who are you?";
      return "NETSOS{REDACTED}";
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
  .get(
    "/sign-out",
    ({ cookie: { profile } }) => {
      profile.value = undefined;
      return redirect("/");
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
  );
