tag: user.maven
-

maven:                      "mvn "
maven version:              "mvn -v\n"
maven clean:                "mvn clean\n"
maven install:              "mvn install\n"
maven package:              "mvn package\n"
maven clean install:        "mvn clean install\n"
maven clean package:        "mvn clean package\n"
maven install parallel:     "mvn -T 1C install\n"
maven deploy:               "mvn clean install -P deploy "
maven dependency tree:      "mvn dependency:tree\n"

maven (outdated | dependency updates):
    "mvn versions:display-dependency-updates -N"
