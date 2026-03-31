import { Blocks } from "lucide-react";
import * as React from "react";
import Link from "next/link";

import { NavBrand } from "./NavBrand";
import { NavLink } from "./NavLink";
import { NavLinkSkeleton } from "./NavSkeleton";

import {
  Sidebar,
  SidebarContent,
  SidebarGroupContent,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenuButton,
  SidebarFooter,
} from "@/components/ui/sidebar";

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar collapsible="offcanvas" {...props}>
      <SidebarHeader>
        <NavBrand />
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Links</SidebarGroupLabel>
          <SidebarGroupContent>
            <React.Suspense fallback={<NavLinkSkeleton />}>
              <NavLink />
            </React.Suspense>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <SidebarMenuButton asChild>
          <Link
            href="https://marketplace.visualstudio.com/items?itemName=snail-unamur.crispy&ssr=false#qna"
            target="_blank"
            rel="noopener noreferrer"
            role="button"
            className="flex justify-center items-center py-6 px-3! text-lg text-foreground! bg-green-500! hover:bg-green-700! rounded-4xl!"
          >
            <Blocks className="h-5! w-5!" />
            <span>Get Vscode Extension</span>
          </Link>
        </SidebarMenuButton>
      </SidebarFooter>
    </Sidebar>
  );
}
