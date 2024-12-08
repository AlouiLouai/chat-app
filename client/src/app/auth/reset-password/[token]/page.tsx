"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useToast } from "@/hooks/use-toast";
import { AuthService } from "@/services/auth.services";
import { useRouter } from "next/navigation";
import { useParams } from "next/navigation"; // Import useParams
import { Label } from "@radix-ui/react-label";

export default function ResetPasswordPage() {
  const [newPassword, setNewPassword] = useState<string>("");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const router = useRouter();

  const { toast } = useToast();

  // Directly use useParams to get the token
  const { token } = useParams(); // Access token directly from useParams

  useEffect(() => {
    if (!token) {
      setErrorMessage("Invalid or missing token.");
    }
  }, [token]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token) {
      setErrorMessage("No token found.");
      return;
    }
    setErrorMessage(null);
    setLoading(true);

    try {
      // Call the AuthService to reset the password
      await AuthService.resetPassword(token as string, newPassword);

      // Display success toast
      toast({
        title: "Password updated!",
        description: "You can log in with your new password.",
        duration: 5000,
      });

      // Navigate to the login page after success
      router.push("/auth/login"); // Redirect to login page
    } catch (error: any) {
      // Handle error
      setErrorMessage(error.message || "Reset password failed. Please try again.");

      // Display error toast
      toast({
        title: "Reset password failed",
        description: error.message || "Invalid password",
        duration: 5000,
      });
    } finally {
      setLoading(false); // Reset loading state
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Reset Password</CardTitle>
          <CardDescription>Enter your new password</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="newPassword">New Password</Label>
                <Input
                  id="newPassword"
                  type="password"
                  placeholder="*******"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  required
                />
              </div>
              {errorMessage && (
                <p className="text-red-500 text-sm">{errorMessage}</p>
              )}
              <Button type="submit" className="w-full" disabled={loading}>
                {loading ? "Updating..." : "Update"}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
