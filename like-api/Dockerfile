FROM python:3.12-slim
WORKDIR /app
COPY app.py .
RUN mkdir /data && chown 65534:65534 /data
USER 65534
ENV LIKE_DB=/data/likes.db PORT=8080
VOLUME /data
EXPOSE 8080
CMD ["python", "-u", "app.py"]
