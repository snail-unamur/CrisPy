"use client";

import Link from "next/link";
import logo from "@/assets/logo.png";
import logoB from "@/assets/logo-white.png";
import Image from "next/image";
import { useTheme } from "@/providers/theme-provider";
export function Brand() {
  const { theme } = useTheme();

  return (
    <Link href="/app" className=" flex items-center gap-1.5">
      <Image
        src={theme == "dark" ? logo : logoB}
        alt="logo-image"
        className="size-8!"
      />
      <span className="text-base font-semibold">PyQuit</span>
    </Link>
  );
}
