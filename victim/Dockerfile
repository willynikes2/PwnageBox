# ============================================================================
# Victim Container - Vulnerable vsftpd 2.3.4
# WARNING: This container is INTENTIONALLY VULNERABLE for demonstration
# DO NOT expose to the internet outside of isolated lab environments
# ============================================================================
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies for building vsftpd
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    libpam0g-dev \
    libcap-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Download and compile vulnerable vsftpd 2.3.4
# This version contains CVE-2011-2523 (backdoor on port 6200)
WORKDIR /tmp
RUN wget --no-check-certificate https://security.appspot.com/downloads/vsftpd-2.3.4.tar.gz || \
    wget --no-check-certificate https://github.com/nikdubois/vsftpd-2.3.4-infected/archive/refs/heads/master.tar.gz -O vsftpd-2.3.4.tar.gz

# If the infected version is available, use it; otherwise simulate
RUN tar xzf vsftpd-2.3.4.tar.gz || true

# Create a simulated vulnerable vsftpd service
RUN mkdir -p /var/ftp /var/run/vsftpd/empty /etc/vsftpd
RUN useradd -r -s /sbin/nologin ftp || true

# Create a simple FTP banner simulation script
RUN echo '#!/bin/bash\n\
echo "220 (vsFTPd 2.3.4)"\n\
while read line; do\n\
    case "$line" in\n\
        USER*) echo "331 Please specify the password." ;;\n\
        PASS*) echo "230 Login successful." ;;\n\
        SYST*) echo "215 UNIX Type: L8" ;;\n\
        FEAT*) echo "211-Features:" ; echo " EPRT" ; echo " EPSV" ; echo " MDTM" ; echo " PASV" ; echo " REST STREAM" ; echo " SIZE" ; echo " TVFS" ; echo "211 End" ;;\n\
        PWD*) echo "257 \"/\" is the current directory" ;;\n\
        QUIT*) echo "221 Goodbye." ; exit 0 ;;\n\
        *) echo "500 Unknown command." ;;\n\
    esac\n\
done' > /usr/local/bin/fake_vsftpd.sh && chmod +x /usr/local/bin/fake_vsftpd.sh

# Install netcat for the FTP simulation
RUN apt-get update && apt-get install -y netcat socat && rm -rf /var/lib/apt/lists/*

EXPOSE 21 6200

# Run the simulated vulnerable FTP service
CMD ["sh", "-c", "while true; do socat TCP-LISTEN:21,reuseaddr,fork EXEC:/usr/local/bin/fake_vsftpd.sh; done"]
