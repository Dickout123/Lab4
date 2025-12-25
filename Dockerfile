FROM alpine:latest
RUN apk update && apk upgrade
RUN apk  add python3
WORKDIR /app
COPY ./school_service.py .
CMD ["python3", "school_service.py"]