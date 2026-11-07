export interface EncyclopediaBuild { files: Map<string, string>; errors: string[]; warnings: string[]; stats: Record<string, number> }
export function compileEncyclopedia(): EncyclopediaBuild;
export function writeEncyclopedia(): EncyclopediaBuild;
export function entityPageId(key: string): string;
export function personPageId(person: string): string;
