import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function getOrCreateUserId(): string {
  let id = localStorage.getItem("user_id");
  if (!id) {
    id = crypto.randomUUID(); // o usa alguna lib como uuidv4
    localStorage.setItem("user_id", id);
  }
  return id;
}