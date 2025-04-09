FROM bitnami/spark:3.5 AS base

USER root
RUN install_packages curl
USER 1001

FROM base AS dep

# RUN curl https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.1/hadoop-aws-3.3.1.jar --output /opt/bitnami/spark/jars/hadoop-aws-3.3.1.jar
# RUN curl https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.901/aws-java-sdk-bundle-1.11.901.jar --output /opt/bitnami/spark/jars/aws-java-sdk-bundle-1.11.901.jar
RUN curl https://repo1.maven.org/maven2/com/crealytics/spark-excel_2.12/0.13.1/spark-excel_2.12-0.13.1.jar --output /opt/bitnami/spark/jars/spark-excel_2.12-0.13.1.jar
RUN curl https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.33/mysql-connector-java-8.0.33.jar --output /opt/bitnami/spark/jars/mysql-connector-java-8.0.33.jar
RUN curl https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.5/postgresql-42.7.5.jar --output /opt/bitnami/spark/jars/postgresql-42.7.5.jar
