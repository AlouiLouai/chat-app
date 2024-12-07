"use client";
import { useEffect, useState } from "react";
import Login from "./auth/login/page";
import Main from "./main/page";

export default function Home() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);

  // Check authentication status on mount (could be from localStorage, cookie, or API)
  useEffect(() => {
    // Example: Check if there's a token or session to identify if the user is authenticated
    const userLoggedIn = localStorage.getItem("access_token"); // Replace with your logic
    if (userLoggedIn) {
      setIsAuthenticated(true); // User is authenticated
    } else {
      setIsAuthenticated(false); // User is not authenticated
    }
  }, []);

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <div className="flex gap-4 items-center flex-col sm:flex-row">
        {isAuthenticated ? <Main /> : <Login />}
        </div>
      </main>
    </div>
  );
}
