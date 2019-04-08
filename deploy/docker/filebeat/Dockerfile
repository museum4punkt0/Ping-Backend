FROM 081960884429.dkr.ecr.eu-central-1.amazonaws.com/base_images:filebeat
COPY filebeat.yml /usr/share/filebeat/filebeat.yml
COPY init.sh /usr/share/filebeat/init.sh
USER root
ENTRYPOINT ["/usr/share/filebeat/init.sh"]
