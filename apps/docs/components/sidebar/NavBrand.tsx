import { Brand } from "@/components/global";

import {
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
} from "@/components/ui/sidebar";

export function NavBrand() {
  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <SidebarMenuButton
          asChild
          className="data-[slot=sidebar-menu-button]:p-1.5!"
        >
          <Brand />
        </SidebarMenuButton>
      </SidebarMenuItem>
    </SidebarMenu>
  );
}
