FROM node:15 AS vue
RUN mkdir -p /var/www/
WORKDIR /var/www/
COPY . /var/www/
RUN npm install 
RUN npm run build

FROM nginx:1.19-alpine AS webserver
COPY --from=vue /var/www/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx","-g","daemon off;"]