"use client";

import { Sidebar, SidebarBody, SidebarLink } from "@/components/ui/sidebar";
import { Home, Settings, User, MessageSquare } from "lucide-react";
import { useState } from "react";

const sidebarLinks = [
  {
    label: "Home",
    href: "/dashboard",
    icon: <Home className="w-5 h-5 text-neutral-700" />,
  },
  {
    label: "Chat",
    href: "/dashboard/chat",
    icon: <MessageSquare className="w-5 h-5 text-neutral-700" />,
  },
  {
    label: "Profile",
    href: "/dashboard/profile",
    icon: <User className="w-5 h-5 text-neutral-700" />,
  },
  {
    label: "Settings",
    href: "/dashboard/settings",
    icon: <Settings className="w-5 h-5 text-neutral-700" />,
  },
];

export function DashboardClient({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="flex h-screen bg-white">
      <Sidebar open={sidebarOpen} setOpen={setSidebarOpen}>
        <SidebarBody>
          <div className="flex flex-col gap-4">
            {sidebarLinks.map((link) => (
              <SidebarLink key={link.href} link={link} />
            ))}
          </div>
        </SidebarBody>
      </Sidebar>
      <main className="flex-1 p-8 overflow-auto">
        {children}
      </main>
    </div>
  );
} 