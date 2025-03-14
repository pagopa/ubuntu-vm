# Use the latest Ubuntu image as the base
FROM ubuntu:latest@sha256:72297848456d5d37d1262630108ab308d3e9ec7ed1c3286a32fe09856619a782
COPY . .

# Install dependencies
RUN apt-get update -y
RUN apt-get install -y git
RUN apt-get install -y python3-pip
RUN apt-get install -y python3
RUN apt-get install -y nodejs
RUN apt-get install -y vim
RUN apt-get install -y curl
RUN apt-get install -y iputils-ping
RUN apt-get install -y postgresql-client
RUN apt-get install -y wget
RUN apt-get install -y libaio1t64
RUN apt-get install -y unzip
RUN rm -rf /var/lib/apt/lists/*


# Set environment variables for Oracle Instant Client
ENV ORACLE_HOME=/opt/oracle
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
RUN rm -rf /tmp
RUN ln -s ${ORACLE_HOME}/instantclient ${ORACLE_HOME}/instantclient
RUN ln -s ${ORACLE_HOME}/sqlplus /usr/bin/sqlplus

RUN ln -s /usr/lib/*-linux-gnu/libaio.so.1t64 ${ORACLE_HOME}/libaio.so.1


RUN pip install -r requirements.txt --break-system-packages

EXPOSE 8080

ENTRYPOINT ["python3",  "./status.py"]