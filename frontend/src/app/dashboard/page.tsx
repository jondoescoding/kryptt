import { Sidebar, SidebarBody, SidebarLink } from "@/components/ui/sidebar";
import { Home, Settings, User } from "lucide-react";

export default function DashboardPage() {
  const sidebarLinks = [
    {
      label: "Home",
      href: "/dashboard",
      icon: <Home className="w-5 h-5 text-neutral-700" />,
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

  return (
    <div className="flex h-screen bg-white">
      <Sidebar>
        <SidebarBody>
          <div className="flex flex-col gap-4">
            {sidebarLinks.map((link) => (
              <SidebarLink key={link.href} link={link} />
            ))}
          </div>
        </SidebarBody>
      </Sidebar>
      <main className="flex-1 p-8">
        <h1 className="text-2xl font-bold mb-4">Welcome to your Dashboard</h1>
        <p className="text-gray-600">
          This is your personal dashboard. More features coming soon!
        </p>
      </main>
    </div>
  );
} 