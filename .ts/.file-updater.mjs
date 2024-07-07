import { updater } from "file-updater";
import { updateEslintrc, updatePrettierrc, updateEsbuild, updateTsconfig } from "ts-archetype";

const config = {
    projectType: "nodeApp",
};

export default async (workspaceDir) => {
    await updater({
        ".eslintrc.json": updateEslintrc(config),
        ".prettierrc.json": updatePrettierrc(config),
        "esbuild.ts": updateEsbuild(config),
        "tsconfig.json": updateTsconfig(config),
    });
};
