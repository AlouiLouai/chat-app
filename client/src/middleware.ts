import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(req: NextRequest) {

  const token = req.cookies.get("access_token")?.value;
  if (token) {
    return NextResponse.next();
  }

  if (
    !token &&
    (
      req.nextUrl.pathname === "/" ||
       req.nextUrl.pathname === "/main" ||
      req.nextUrl.pathname === "/profile"
      )
  ) {
    return NextResponse.redirect(new URL("/auth/login", req.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/",
    "/main"
  ],
};
