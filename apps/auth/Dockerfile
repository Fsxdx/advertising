FROM advertising_app_base_image
COPY . /apps/auth
RUN pip install --no-cache-dir -r /apps/auth/requirements.txt
ENV DB_HOST=host.docker.internal
EXPOSE 5001
CMD gunicorn --workers=4 --bind 0.0.0.0:5001 apps.auth.app:app