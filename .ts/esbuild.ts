import esbuild from "esbuild";

const options: esbuild.BuildOptions = {
    entryPoints: ["src/index.ts"],
    outfile: "../talon.js",
    platform: "neutral",
    packages: "external",
    bundle: true,
};

async function build() {
    await esbuild.build({
        ...options,
        // minify: true,
    });
}

async function watch() {
    const ctx = await esbuild.context(options);
    await ctx.watch();
}

(async () => {
    if (process.argv.includes("--watch")) {
        await watch();
    } else {
        await build();
    }
})();
