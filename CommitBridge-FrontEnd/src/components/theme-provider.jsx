"use client";

import { useTheme as NextUseTheme, ThemeProvider as NextThemeProvider } from "next-themes";

export function ThemeProvider({ children, ...props }) {
  return <NextThemeProvider {...props}>{children}</NextThemeProvider>;
}

export const useTheme = NextUseTheme;
