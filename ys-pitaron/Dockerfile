FROM python:3.12-alpine AS build
WORKDIR /app
ARG DOMAIN=https://example.co.il
ARG GA4_ID=
ARG GTM_ID=
ARG GSC_VERIFY=
ENV DOMAIN=$DOMAIN GA4_ID=$GA4_ID GTM_ID=$GTM_ID GSC_VERIFY=$GSC_VERIFY
COPY src/ ./src/
RUN python src/build.py /out

FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /out /usr/share/nginx/html
EXPOSE 80
HEALTHCHECK CMD wget -qO- http://127.0.0.1/ >/dev/null || exit 1
