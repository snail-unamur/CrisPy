import { House, Moon, Sun } from "lucide-react";

import { Separator } from "@/components/ui/separator";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { Search } from "@/components/global";
import Link from "next/link";
import { useTheme } from "@/providers/theme-provider";
import { Button } from "../ui/button";

export function AppHeader() {
  const { theme, setTheme } = useTheme();

  const handleTheme = () => {
    if (theme == "dark") {
      setTheme("light");
    } else {
      setTheme("dark");
    }
  };

  return (
    <div className="sticky top-0 z-50 bg-[#18181b]">
      <header className="bg-background flex h-16 shrink-0 items-center gap-2 border-b transition-[width,height] ease-linear group-has-data-[collapsible=icon]/sidebar-wrapper:h-(--header-height)">
        <div className="flex w-full items-center justify-between gap-1 px-4 lg:gap-2 lg:px-6">
          <div className="flex w-full items-center gap-1">
            <SidebarTrigger className="-ml-1" />
            <Separator
              orientation="vertical"
              className="mx-0.5 md:mx-2 data-[orientation=vertical]:h-4"
            />
            <Link
              href={"/"}
              className="text-base font-medium flex items-center gap-1.5"
            >
              <House className="h-5" /> <span className="text-base">Home</span>
            </Link>
          </div>
          <div className="relative flex gap-1 md:gap-2">
            <Search className="md:w-75 w-fit" />
            <Button
              onClick={handleTheme}
              className="bg-sidebar! hover:bg-sidebar/70! active:bg-sidebar/50! outline-none! border-none!"
            >
              {theme == "dark" ? (
                <Sun className=" text-foreground! w-5! h-5!" />
              ) : (
                <Moon className=" text-foreground! w-5! h-5!" />
              )}
            </Button>
          </div>
        </div>
      </header>
    </div>
  );
}
