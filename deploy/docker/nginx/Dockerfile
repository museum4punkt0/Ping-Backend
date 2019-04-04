FROM 081960884429.dkr.ecr.eu-central-1.amazonaws.com/base_images:nginx
ADD default.conf /etc/nginx/conf.d/default.conf
VOLUME ["/app"]
ENTRYPOINT ["nginx", "-g", "daemon off;"]
