FROM advertising_app_base_image:1.0
COPY . /apps/auth
RUN pip install --no-cache-dir -r /apps/auth/requirements.txt
ENV DB_HOST=host.docker.internal \
    SECRET_KEY=b!e.*(mi]cQkOR1Wh^oRmzkM#PcL.A[;cfel/)#NF%CAi+?c<;/:sV@*Tua]V&
EXPOSE 5001
CMD gunicorn --workers=4 --bind 0.0.0.0:5001 apps.auth.app:app