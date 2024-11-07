# Use the latest Ubuntu image as the base
FROM ubuntu:latest
COPY . .

RUN apt-get update -y
RUN apt-get install -y git pip python3 nodejs vim curl iputils-ping postgresql-client

RUN pip install -r requirements.txt --break-system-packages

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    libaio-dev \
    libaio1 \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Oracle Instant Client
ENV ORACLE_HOME=/opt/oracle/
ENV LD_LIBRARY_PATH=$ORACLE_HOME

# Define the Oracle Instant Client download URLs
ENV BASIC_ZIP_URL="https://download.oracle.com/otn_software/linux/instantclient/2350000/instantclient-basic-linux.x64-23.5.0.24.07.zip"
ENV SQLPLUS_ZIP_URL="https://download.oracle.com/otn_software/linux/instantclient/2350000/instantclient-sqlplus-linux.x64-23.5.0.24.07.zip"

# Download Oracle Instant Client files
RUN wget --no-check-certificate "${BASIC_ZIP_URL}" -O /tmp/instantclient-basic.zip && \
    wget --no-check-certificate "${SQLPLUS_ZIP_URL}" -O /tmp/instantclient-sqlplus.zip

# Unzip and set up Oracle Instant Client
RUN mkdir -p ${ORACLE_HOME}
RUN unzip "/tmp/instantclient-basic.zip" -d /tmp/oracle_basic
RUN unzip "/tmp/instantclient-sqlplus.zip" -d /tmp/oracle_sqlplus
RUN mv /tmp/oracle_basic/instantclient_*/* ${ORACLE_HOME}/
RUN mv /tmp/oracle_sqlplus/instantclient_*/* ${ORACLE_HOME}/
RUN #    rm -rf /tmp
RUN ln -s ${ORACLE_HOME}/instantclient ${ORACLE_HOME}/instantclient
RUN ln -s ${ORACLE_HOME}/sqlplus /usr/bin/sqlplus

# Test SQL*Plus installation
#RUN sqlplus -version

EXPOSE 8080

ENTRYPOINT ["python3",  "./status.py"]
