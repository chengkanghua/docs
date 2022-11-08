FROM openjdk:8-jdk-alpine
COPY target/user-service.jar app.jar
ENV JAVA_OPTS=""
CMD [ "sh", "-c", "java $JAVA_OPTS -jar /app.jar" ]