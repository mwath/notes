export function loadFromLocal<T>(key: string): T | undefined {
  const data = localStorage.getItem(key);
  if (data) {
    return JSON.parse(data) as T;
  }
}

export function saveToLocal(key: string, value: any): void {
  if (value === undefined) {
    localStorage.removeItem(key);
  } else {
    localStorage.setItem(key, JSON.stringify(value));
  }
}
