"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useToast } from "@/hooks/use-toast";
import { Label } from "@/components/ui/label";
import { AuthService } from "@/services/auth.services";
import { useRouter, useSearchParams } from "next/navigation";

export default function ResetPasswordPage() {
  const [newPassword, setNewPassword] = useState<string>("");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const router = useRouter();
  const { toast } = useToast(); 

  // Access the URL query parameters (where the token is passed)
  const searchParams = useSearchParams();
  const token = searchParams.get('token'); // Token will be extracted from the URL

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
      // Call the AuthService forgot-password function
        await AuthService.resetPassword(token, newPassword);

      // Display success toast
      toast({
        title: "Password updated!",
        description: "you can login with you new password",
        duration: 5000,  // 5 seconds duration
      });

      // Navigate to the protected dashboard page
      router.push("/auth/login"); // Redirect to the dashboard
    } catch (error: any) {
      // Handle login failure
      setErrorMessage(error.message || "Reset password failed. Please try again.");

      // Display error toast
      toast({
        title: "Reset password Failed",
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
          <CardTitle>Reset password ?</CardTitle>
          <CardDescription>Enter your new password</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">New Password</Label>
                <Input
                  id="newPassword"
                  type="password"
                  placeholder="*******"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  required
                />
              </div>
              {errorMessage && <p className="text-red-500 text-sm">{errorMessage}</p>}
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
