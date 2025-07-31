FROM caddy:alpine

COPY Caddyfile /etc/caddy/Caddyfile
COPY static /var/www/html

CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile", "--adapter", "caddyfile"]