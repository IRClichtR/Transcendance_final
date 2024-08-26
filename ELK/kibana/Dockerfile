# Base image
FROM kibana:8.12.0

# Copy the setup and wait-for-it scripts
COPY setup.sh /usr/local/bin/setup.sh
COPY wait-for-it.sh /usr/share/wait-for-it.sh

# COPY kibana.yml /usr/share/kibana/config
# COPY tls-certificates/ /usr/share/kibana/config

# COPY get_credentials.sh /usr/share/kibana/config/get_credentials

# Making scripts executable
# RUN chmod +x /usr/local/bin/setup.sh /usr/share/wait-for-it.sh

# Expose the necessary port
EXPOSE 5601

# Run the setup script as entrypoint
ENTRYPOINT ["/usr/local/bin/setup.sh"]
# ENTRYPOINT ["/usr/share/kibana/config/get_credentials"]
