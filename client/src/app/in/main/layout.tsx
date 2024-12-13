import { cookies } from "next/headers"
import { AppSidebar } from "@/components/app-sidebar";
import { Navbar } from "@/components/Navbar";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";

export default async function InLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const cookieStore = await cookies()
  const defaultOpen = cookieStore.get("sidebar:state")?.value === "true"
  return (
    <section className="flex h-screen">
        <div className="flex flex-col w-full">
          <Navbar /> {/* Navbar at the top */}
          <main className="flex-1 overflow-hidden">{children}</main>
        </div>
    </section>
  );
}
