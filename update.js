const fs = require("fs");
const path = require("path");
const childProcess = require("child_process");

function getUserPath() {
  const parentDir = path.dirname(__dirname);
  const pathParts = parentDir.split(path.sep);
  if (pathParts.at(-1) !== "user" || !pathParts.at(-2).endsWith("talon")) {
    throw Error(`Can't find talon user directory from path: ${__dirname}`);
  }
  return parentDir;
}

function gitUpdate(userDir, url, folderName, branch) {
  const repositoryDir = path.join(userDir, folderName);
  if (fs.existsSync(repositoryDir)) {
    console.log(`'${folderName}' already exists`);
  } else {
    childProcess.execSync(`git clone ${url} ${folderName}`, { cwd: userDir });
  }
  childProcess.execSync(`git checkout ${branch}`, { cwd: repositoryDir });
  childProcess.execSync(`git pull`, { cwd: repositoryDir });
  console.log();
}

(() => {
  const userDir = getUserPath();
  console.log(`Talon user directory: ${userDir}\n`);

  gitUpdate(
    userDir,
    "git@github.com:AndreasArvidsson/talon-analyze-phrase.git",
    "analyze-phrase",
    "main"
  );

  gitUpdate(
    userDir,
    "git@github.com:AndreasArvidsson/andreas-talon.git",
    "andreas-talon",
    "master"
  );

  gitUpdate(
    userDir,
    "git@github.com:AndreasArvidsson/talon-vscode-command-client.git",
    "command-client",
    "master"
  );

  gitUpdate(
    userDir,
    "git@github.com:AndreasArvidsson/cursorless-talon.git",
    "cursorless-talon",
    "main"
  );

  gitUpdate(
    userDir,
    "git@github.com:AndreasArvidsson/rango-talon.git",
    "rango-talon",
    "main"
  );
})();
