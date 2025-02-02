"use client";

import { Sidebar, SidebarBody, SidebarLink } from "@/components/ui/sidebar";
import { Home, Settings, User, MessageSquare } from "lucide-react";
import { useState } from "react";

export default function DashboardPage() {
  return (
    <>
      <h1 className="text-2xl font-bold mb-4">Welcome to your Dashboard</h1>
      <p className="text-gray-600">
        This is your personal dashboard. More features coming soon!
      </p>
    </>
  );
} 