"use client";

import { useState, useEffect } from "react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ProfileService } from "@/services/profile.services"; // Adjust the import path based on your project structure
import { toast } from "@/hooks/use-toast";
import { useRouter } from "next/navigation";

export default function ProfilePage() {
  const router = useRouter();
  const [user, setUser] = useState({
    name: "",
    email: "",
    avatarUrl: "",
  });
  const [file, setFile] = useState<File | undefined>();

  // Fetch profile data on component mount
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const { profile } = await ProfileService.getProfile();
        setUser({
          name: profile.username,
          email: profile.email,
          avatarUrl: profile.image_url,
        });
      } catch (error) {
        console.error("Error fetching profile:", error);
      }
    };

    fetchProfile();
  }, []);

  const handleImageUpdate = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setFile(file);
      const reader = new FileReader();

      // Preview the avatar image
      reader.onload = () => {
        setUser((prev) => ({
          ...prev,
          avatarUrl: reader.result as string,
        }));
      };

      reader.readAsDataURL(file);
    }
  };

  const handleProfileUpdate = async () => {
    try {
      const updateData = {
        name: user.name,
        email: user.email,
      };

      const result = await ProfileService.updateProfile(updateData, file);
      if (result.success) {
        toast({
          title: "Profile updated successfully!",
          description: "Redirecting to main...",
          duration: 5000, // 5 seconds duration
        });
        router.push("/main");
      } else {
        alert(`Failed to update profile: ${result.message}`);
      }
    } catch (error) {
      console.error("Error updating profile:", error);
      alert("An error occurred while updating the profile.");
    }
  };

  const handleReturnToMain = () => {
    router.push("/main");
  };

  return (
    <div className="container mx-auto py-10">
      <Card className="max-w-md mx-auto">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center">
            User Profile
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col items-center space-y-6">
            <div className="relative">
              <Avatar className="h-32 w-32">
                <AvatarImage src={user.avatarUrl} alt={user.name} />
                <AvatarFallback>
                  {user.name
                    .split(" ")
                    .map((n) => n[0])
                    .join("")}
                </AvatarFallback>
              </Avatar>
              <label
                htmlFor="upload-avatar"
                className="absolute bottom-0 right-0 h-8 w-8 p-0 rounded-full bg-background border shadow-md cursor-pointer flex items-center justify-center"
              >
                <span className="sr-only">Update Image</span>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-4 w-4 text-muted-foreground"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M15.232 5.232a3 3 0 114.243 4.243l-9 9a3 3 0 01-1.414.757l-3 0.5a.75.75 0 01-.854-.854l.5-3a3 3 0 01.757-1.414l9-9z"
                  />
                </svg>
              </label>
              <input
                id="upload-avatar"
                type="file"
                accept="image/*"
                onChange={handleImageUpdate}
                className="hidden"
              />
            </div>
            <div className="w-full space-y-4">
              <div className="space-y-2">
                <Label htmlFor="username">Username</Label>
                <Input
                  id="username"
                  value={user.name}
                  onChange={(e) =>
                    setUser((prev) => ({ ...prev, name: e.target.value }))
                  }
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  value={user.email}
                  onChange={(e) =>
                    setUser((prev) => ({ ...prev, email: e.target.value }))
                  }
                />
              </div>
              <Button className="w-full" onClick={handleProfileUpdate}>
                Update Profile
              </Button>
              <Button
                variant="outline"
                className="w-full"
                onClick={handleReturnToMain}
              >
                Return to Main
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
