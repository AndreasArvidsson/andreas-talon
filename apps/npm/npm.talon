tag: user.npm
-

node:                       "node "
node version:               "node -v\n"

npm:                        "npm "
npm version:                "npm -v\n"
npm init:                   "npm init"
npm install:                "npm install "
npm install global:         "npm install -g "
npm uninstall:              "npm uninstall "
npm uninstall global:       "npm uninstall -g "
npm link:                   "npm link "
npm list:                   "npm list\n"
npm list global:            "npm list -g\n"
npm outdated:               "npm outdated\n"
npm update:                 "npm update --save\n"
npm prune:                  "npm prune\n"
npm publish [dry]:          "npm publish --dry-run"

npm clean:                  "npm run clean\n"
npm start:                  "npm start\n"
npm test:                   "npm test\n"
npm run:                    "npm run "
npm run <user.text>$:       "npm run {text}"
npm run build:              "npm run build\n"

# pnpm
pnpm:                       "pnpm "
pnpm version:               "pnpm -v\n"
pnpm init:                  "pnpm init"
pnpm install:               "pnpm install "
pnpm compile:               "pnpm compile "

# Know run scripts
npm run (mongodb | mongo db | mongo):
    "npm run mongodb\n"
npm run (keycloak | key cloak):
    "npm run keycloak\n"
npm run (wildfly | wild fly):
    "npm run wildfly\n"
npm run gss [<user.word>]:
    "npm run startLocal gss-{word or ''}"
