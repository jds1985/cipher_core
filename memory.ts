// memory.ts
export interface Memory {
  id: string;
  content: string;
  tags?: string[];
  timestamp: number;
}

let memoryStore: Memory[] = [];

export function storeMemory(memory: Memory) {
  memoryStore.push(memory);
}

export function getMemoriesByTag(tag: string): Memory[] {
  return memoryStore.filter(m => m.tags?.includes(tag));
}
