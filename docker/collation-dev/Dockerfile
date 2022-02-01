FROM openjdk:11 AS default
COPY ./collation/collatex-tools-1.8-SNAPSHOT.jar /usr/collatex/
WORKDIR /usr/collatex
CMD java -jar collatex-tools-1.8-SNAPSHOT.jar -http