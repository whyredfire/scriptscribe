FROM nginxinc/nginx-unprivileged:stable-alpine-slim

COPY --chown=nginx:nginx static /usr/share/nginx/html
RUN mkdir -p /etc/nginx/tmp && chown -R nginx:nginx /etc/nginx/tmp

EXPOSE 8080
