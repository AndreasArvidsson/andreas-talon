tag: user.npm
-

node:                       "node "
node version:               "node -v\n"

npm:                        "npm "
npm {user.npm_command}:     "npm {npm_command}"
npm run <user.prose>$:      "npm run {prose}"

pnpm:                       "pnpm "
pnpm {user.pnpm_command}:   "pnpm {pnpm_command}"
pnpm run <user.prose>$:     "pnpm run {prose}"

# Know run scripts
npm run (mongodb | mongo db | mongo):
    "npm run mongodb\n"
npm run (keycloak | key cloak):
    "npm run keycloak\n"
npm run (wildfly | wild fly | wide fly):
    "npm run wildfly\n"
npm run (gss | ge es es) {user.gss_module}:
    "npm run startLocal gss-{gss_module}\n"
npm run (gss | ge es es):
    "npm run startLocal gss-"
