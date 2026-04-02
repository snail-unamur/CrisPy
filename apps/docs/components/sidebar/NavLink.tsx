"use client";

import { LayoutDashboard, ChevronRight } from "lucide-react";
import Link from "next/link";
import { ruleMap } from "@crispy/rules";

import {
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarMenuSub,
  SidebarMenuSubItem,
  SidebarMenuSubButton,
} from "@/components/ui/sidebar";

import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";

export function NavLink() {
  const groupedRules = Object.entries(ruleMap).reduce(
    (acc, [ruleId, rule]) => {
      if (!acc[rule.category]) {
        acc[rule.category] = [];
      }
      acc[rule.category].push({ id: ruleId, ...rule });
      return acc;
    },
    {} as Record<string, any[]>,
  );

  return (
    <SidebarMenu>
      <SidebarMenuItem className="my-1">
        <SidebarMenuButton asChild>
          <Link href="/" className="text-foreground!">
            <LayoutDashboard size={24} className="me-2" />
            <span>Dashboard</span>
          </Link>
        </SidebarMenuButton>
      </SidebarMenuItem>

      {Object.entries(groupedRules).map(([category, rules]) => (
        <Collapsible key={category} asChild className="group/collapsible">
          <SidebarMenuItem>
            <CollapsibleTrigger asChild>
              <SidebarMenuButton tooltip={category}>
                <span className="capitalize">{category}</span>
                <ChevronRight className="ml-auto transition-transform duration-200 group-data-[state=open]/collapsible:rotate-90" />
              </SidebarMenuButton>
            </CollapsibleTrigger>

            <CollapsibleContent>
              <SidebarMenuSub>
                {rules.map((rule) => (
                  <SidebarMenuSubItem key={rule.id}>
                    <SidebarMenuSubButton asChild>
                      <Link href={rule.docsPath}>
                        <span>
                          {rule.id} — {rule.title}
                        </span>
                      </Link>
                    </SidebarMenuSubButton>
                  </SidebarMenuSubItem>
                ))}
              </SidebarMenuSub>
            </CollapsibleContent>
          </SidebarMenuItem>
        </Collapsible>
      ))}
    </SidebarMenu>
  );
}
