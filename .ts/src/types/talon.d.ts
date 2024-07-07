import type { Actions } from "./Actions";
import type { Namespace } from "./Namespace";

declare module "talon" {
    const actions: Actions;

    class Context {
        matches: string;
        tags: string[];
        settings: Record<string, string | number | boolean>;
        lists: Record<string, Record<string, string> | string[]>;
        action_class(name: Namespace, actions: Partial<Actions>): void;
    }

    const settings: {
        get<T extends string | number | boolean>(name: string, defaultValue?: T): T | null;
    };
}
