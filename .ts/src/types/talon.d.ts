import type { ActionNamespaces } from "./Actions";
import type { Namespace } from "./Namespace";

type MainActions = Pick<ActionNamespaces, "main">;
type ActionsSansMain = Omit<ActionNamespaces, "main">;
type Actions = ActionsSansMain & MainActions[keyof MainActions];

declare module "talon" {
    const actions: Actions;

    class Context {
        matches: string;
        tags: string[];
        settings: Record<string, string | number | boolean>;
        lists: Record<string, Record<string, string> | string[]>;
        action_class(name: Namespace, actions: Partial<ActionNamespaces[Namespace]>): void;
    }

    const settings: {
        get<T extends string | number | boolean>(name: string, defaultValue?: T): T | null;
    };
}
