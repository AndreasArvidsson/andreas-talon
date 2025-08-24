tag: user.maven
-

maven:                      "mvn "
maven version:              "mvn -v\n"
maven clean:                "mvn clean\n"

maven install:              "mvn -T 1C install\n"
maven package:              "mvn -T 1C package\n"
maven deploy:               "mvn -T 1C package -P deploy "

maven package slow:         "mvn package\n"
maven install slow:         "mvn install\n"
maven deploy slow:          "mvn package -P deploy "

maven clean package:        "mvn clean package\n"
maven clean install:        "mvn clean install\n"
maven clean deploy:         "mvn clean -T 1C package -P deploy "

maven dependency list:      "mvn dependency:list\n"
maven dependency tree:      "mvn dependency:tree\n"

maven (outdated | dependency updates):
    "mvn versions:display-dependency-updates -N\n"

maven (outdated plugin | plugin updates):
    "mvn versions:display-plugin-updates -N\n"
