FROM openjdk:8-jdk-alpine
ADD target/eureka.jar app.jar
ENV JAVA_OPTS=""
CMD [ "sh", "-c", "java $JAVA_OPTS -jar /app.jar" ]