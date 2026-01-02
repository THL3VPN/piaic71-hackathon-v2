// [Task]: T003 [From]: specs/017-add-chat-widget/spec.md
import { getToken } from "./auth";

export function getLauncherLabel(isOpen: boolean): string {
  return isOpen ? "Close chat" : "Open chat";
}

export function getLauncherIcon(isOpen: boolean): string {
  return isOpen ? "×" : "💬";
}

export function isWidgetAvailable(): boolean {
  return Boolean(getToken());
}
