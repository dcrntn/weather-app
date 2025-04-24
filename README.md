# Weather checker app
This application will check the weather for the next 7 day, based on a ZIP and COUNTRY code. Gets the avarage sunshine in seconds and the avarage rain in mm. If the sunshine or the rain isn't over the tresholds 20000 seconds, 20 mm it will set the needs light or needs water columns. This way a remote watering or any home automation system can act upon this information. Starting grass watering or setting the shades for the day etc..

## Backend
The backend is separated into 3 parts, fetching the data from diff. API-s. Processing the data and into a frontend api, which sole purpose is to communicate with the fronted. 

## Frontend
Is written in vue, since it's powerful enough for this application. After starting with docker compose the frontend is available on http://localhost/ (if the nginx's port in the compose.yml file is set to 80)

## Database
For db the app uses prostgreSQL since NoSQL dbs wouldn't be reasonable.

## Nginx
It's probabbly not needed, but this way the lkrts can be emitted if testing from outside of docker.

## Note
The application can be run with docker compose

```
docker compose up
```
Or podman compose
```
podman compose up
```

Also please note, podman doesn't run as root by default, so testing on local will require running it as root OR a port change in the compose file for example to 8080 with docker compose this shouldn't be a problem.
```
nginx:
    image: docker.io/library/nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "8080:80"
    depends_on:
      - frontend
    networks:
      - my_network
```