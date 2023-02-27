FROM nginx:1.21-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY ./build/static/ /home/app/web/static/
COPY build /usr/share/nginx/html