FROM advertising_app_base_image:1.0
COPY . /apps/main_app
RUN pip install --no-cache-dir -r /apps/main_app/requirements.txt
ENV AUTH_URL=http://auth_service:5001 \
    DB_HOST=host.docker.internal \
    SECRET_KEY=b!e.*(mi]cQkOR1Wh^oRmzkM#PcL.A[;cfel/)#NF%CAi+?c<;/:sV@*Tua]V&
EXPOSE 5000
CMD gunicorn --workers=4 --bind 0.0.0.0:5000 apps.main_app.app:app