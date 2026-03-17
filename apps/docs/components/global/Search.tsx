"use client";

import { BookOpen, ChevronsUpDown } from "lucide-react";
import { useState, useMemo } from "react";
import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { ruleMap } from "@pyquit/rules";
import { cn } from "@/lib/utils";

const rulesArray = Object.entries(ruleMap).map(([id, rule]) => ({
  id,
  ...rule,
}));

export function Search({
  className,
  label = "in the docs",
}: {
  className?: string;
  label?: string;
}) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const router = useRouter();

  const filteredResults = useMemo(() => {
    const search = query.toLowerCase().trim();
    if (search.length === 0) return [];

    return rulesArray
      .filter(
        (rule) =>
          rule.id.toLowerCase().includes(search) ||
          rule.title.toLowerCase().includes(search),
      )
      .slice(0, 10);
  }, [query]);

  return (
    <Popover open={open} onOpenChange={setOpen} modal={true}>
      <div className={cn(className)}>
        <PopoverTrigger asChild>
          <Button
            variant="outline"
            role="combobox"
            aria-expanded={open}
            className="w-full justify-between bg-sidebar border-white/10 text-foreground hover:bg-sidebar/5"
          >
            {`Search ${label}...`}
            <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </PopoverTrigger>
        <PopoverContent
          className="w-(--radix-popover-trigger-width) z-100 p-0 border-white/10 bg-[#161618]"
          style={{ pointerEvents: "auto" }}
        >
          <Command shouldFilter={false}>
            <CommandInput
              placeholder={`search ${label} ...`}
              onValueChange={setQuery}
              className="text-white"
            />
            <CommandList className="max-h-75">
              {query.length > 0 && filteredResults.length === 0 && (
                <CommandEmpty className="py-6 text-center text-sm text-muted-foreground">
                  No rules found for "{query}".
                </CommandEmpty>
              )}

              {filteredResults.length > 0 && (
                <CommandGroup heading="Available Rules">
                  {filteredResults.map((rule) => (
                    <CommandItem
                      key={rule.id}
                      value={rule.id.toLowerCase()}
                      onSelect={() => {
                        const target = rule.docsPath.toLowerCase();
                        router.push(target);
                        setOpen(false);
                      }}
                      className="cursor-pointer"
                    >
                      <div className="flex w-full items-center gap-2 px-3 py-2 text-white">
                        <BookOpen className="h-4 w-4 text-blue-400" />
                        <div className="flex flex-col">
                          <span className="font-medium">{rule.id}</span>
                          <span className="text-xs text-muted-foreground">
                            {rule.title}
                          </span>
                        </div>
                      </div>
                    </CommandItem>
                  ))}
                </CommandGroup>
              )}
            </CommandList>

            <CommandSeparator className="bg-white/10" />
            <div className="flex items-center justify-between px-3 py-2 text-[10px] text-muted-foreground bg-white/5">
              <div className="flex gap-2">
                <span>
                  <kbd className="rounded bg-muted px-1.5 py-0.5">↑↓</kbd>{" "}
                  Navigate
                </span>
                <span>
                  <kbd className="rounded bg-muted px-1.5 py-0.5">↵</kbd> Select
                </span>
              </div>
              <span className="font-semibold text-blue-400">PyQuit Rules</span>
            </div>
          </Command>
        </PopoverContent>
      </div>
    </Popover>
  );
}
