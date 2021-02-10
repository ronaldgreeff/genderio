FROM nginx:1.17-alpine

# # FROM nginx:1.15.5s
# # RUN rm /etc/nginx/nginx.conf
# RUN rm /etc/nginx/conf.d/default.conf
# COPY nginx.conf /etc/nginx/
#
# # RUN rm /etc/nginx/conf.d/.conf
# COPY my_web_app.conf /etc/nginx/conf.d/


RUN rm /etc/nginx/nginx.conf

#Put our custom nginx config in its place
COPY nginx.conf /etc/nginx/

#Remove any existing site configs
RUN rm /etc/nginx/conf.d/*.conf

#Put our website specific config
COPY instagender.conf /etc/nginx/conf.d/
