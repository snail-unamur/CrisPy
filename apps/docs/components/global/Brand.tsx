"use client";

import Link from "next/link";
import logoWithe from "@/assets/logo-white.png";
import logoBlack from "@/assets/logo-black.png";
import Image from "next/image";
import { useTheme } from "@/providers/theme-provider";
export function Brand() {
  const { theme } = useTheme();

  return (
    <Link href="/" className=" flex items-center gap-1.5">
      <Image
        src={theme == "dark" ? logoWithe : logoBlack}
        alt="logo-image"
        className="size-8!"
      />
      <span className="text-base font-semibold">CrisPy</span>
    </Link>
  );
}
