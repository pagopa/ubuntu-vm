# Use the latest Ubuntu image as the base
FROM ubuntu:latest
COPY . .

# Set environment variables for Oracle Instant Client
ENV ORACLE_HOME=/opt/oracle
ENV LD_LIBRARY_PATH=$ORACLE_HOME

# Define Oracle Instant Client download URLs
ENV BASIC_ZIP_URL="https://download.oracle.com/otn_software/linux/instantclient/2350000/instantclient-basic-linux.x64-23.5.0.24.07.zip"
ENV SQLPLUS_ZIP_URL="https://download.oracle.com/otn_software/linux/instantclient/2350000/instantclient-sqlplus-linux.x64-23.5.0.24.07.zip"

# Install dependencies in one RUN statement, clean up apt cache
RUN apt-get update && \
apt-get install -y --no-install-recommends \
    git \
    nodejs \
    vim \
    curl \
    iputils-ping \
    postgresql-client \
    wget \
    libaio1 \
    unzip && \
    rm -rf /var/lib/apt/lists/*

# Download and set up Oracle Instant Client
RUN wget --no-check-certificate "${BASIC_ZIP_URL}" -O /tmp/instantclient-basic.zip && \
    wget --no-check-certificate "${SQLPLUS_ZIP_URL}" -O /tmp/instantclient-sqlplus.zip && \
    mkdir -p ${ORACLE_HOME} && \
    unzip -q /tmp/instantclient-basic.zip -d /tmp/oracle_basic && \
    unzip -q /tmp/instantclient-sqlplus.zip -d /tmp/oracle_sqlplus && \
    mv /tmp/oracle_basic/instantclient_*/* ${ORACLE_HOME}/ && \
    mv /tmp/oracle_sqlplus/instantclient_*/* ${ORACLE_HOME}/ && \
    ln -s ${ORACLE_HOME}/instantclient ${ORACLE_HOME}/instantclient && \
    ln -s ${ORACLE_HOME}/sqlplus /usr/bin/sqlplus && \
    ln -s /usr/lib/*-linux-gnu/libaio.so.1 /usr/lib/libaio.so.1 && \
    rm -rf /tmp/*

# Copy application files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8080

# Set the entrypoint for the container
ENTRYPOINT ["python3", "./status.py"]
