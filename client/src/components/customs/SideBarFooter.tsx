"use"
import React, { useState } from "react";
import { Home, LogOut, Settings } from "lucide-react";
import { Button } from  "../ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import {
  SidebarMenu,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { DropdownMenuContent, DropdownMenuItem } from "@radix-ui/react-dropdown-menu";

export function AppSidebarFooter({ userProfile, handleLogout, router }: AppSidebarFooterProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleExpansion = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <div className="relative">
          <Button
            variant="ghost"
            className="h-10 w-10 rounded-full"
            onClick={toggleExpansion}
          >
            <Avatar className="h-10 w-10">
              <AvatarImage
                src={userProfile.image_url}
                alt={userProfile.username}
              />
              <AvatarFallback>
                {userProfile.username
                  .split(" ")
                  .map((n) => n[0])
                  .join("")}
              </AvatarFallback>
            </Avatar>
          </Button>
          {isExpanded && (
            <DropdownMenuContent
              side="top"
              align="center"
              className="w-56 bg-white rounded shadow-md mt-2 absolute z-10"
            >
              <DropdownMenuItem onClick={() => router.push("/in/profile")}>
                <Home className="mr-2 h-4 w-4" />
                <span>Profile</span>
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Settings className="mr-2 h-4 w-4" />
                <span>Settings</span>
              </DropdownMenuItem>
              <DropdownMenuItem onClick={handleLogout}>
                <LogOut className="mr-2 h-4 w-4" />
                <span>Sign out</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          )}
        </div>
      </SidebarMenuItem>
    </SidebarMenu>
  );
}
