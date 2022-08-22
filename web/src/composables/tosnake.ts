export function tosnake(name: string): string {
  return name.replace(/(?<=.)[A-Z]/g, (c) => "_" + c).toLowerCase();
}
