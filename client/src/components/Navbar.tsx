"use client";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { User, Settings, LogOut } from "lucide-react";
import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";
import Cookie from "js-cookie";
import { ProfileService } from "@/services/profile.services";
import { AuthService } from "@/services/auth.services";

export function Navbar() {
  const router = useRouter();
  const [userProfile, setUserProfile] = useState<{ username: string; email: string; image_url: string }>({
    username: "",
    email: "",
    image_url: "",
  });

  // Fetch profile data when the component mounts
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const { profile } = await ProfileService.getProfile();
        setUserProfile({
          username: profile.username,
          email: profile.email,
          image_url: profile.image_url, // Set a default image if none exists
        });

        console.log('UserProfile : ',userProfile)

      } catch (error) {
        console.error("Error fetching profile:", error);
      }
    };

    fetchProfile();
  }, []);

  // Logout handler
  const handleLogout = async () => {
    try {
      const refreshToken = Cookie.get("refresh_token");

      if (!refreshToken) {
        throw new Error("Refresh token not found");
      }

      await AuthService.logout(refreshToken); // Call logout service
      Cookie.remove("access_token"); // Remove cookies
      Cookie.remove("refresh_token");
      router.push("/auth/login"); // Redirect to login
    } catch (error: any) {
      console.error("Logout failed:", error.message);
      alert("Failed to log out. Please try again.");
    }
  };

  return (
    <nav className="flex items-center justify-between p-4 bg-background border-b">
      <div className="flex-1">
        {/* Add other navbar content here if needed */}
      </div>
      <div className="flex items-center">
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="relative h-10 w-10 rounded-full">
              <Avatar className="h-10 w-10">
                <AvatarImage src={userProfile.image_url} alt={userProfile.username} />
                <AvatarFallback>{userProfile.username.split(" ").map((n) => n[0]).join("")}</AvatarFallback>
              </Avatar>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="w-56" align="end" forceMount>
            <DropdownMenuLabel className="font-normal">
              <div className="flex flex-col space-y-1">
                <p className="text-sm font-medium leading-none">{userProfile.username}</p>
                <p className="text-xs leading-none text-muted-foreground">{userProfile.email}</p>
              </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={() => router.push("/in/profile")}>
              <User className="mr-2 h-4 w-4" />
              <span>Profile</span>
            </DropdownMenuItem>
            <DropdownMenuItem>
              <Settings className="mr-2 h-4 w-4" />
              <span>Settings</span>
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={handleLogout}>
              <LogOut className="mr-2 h-4 w-4" />
              <span>Log out</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </nav>
  );
}
