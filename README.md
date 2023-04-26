# Shortener URL maker 

This project will make any requested url in a shorted one using Django and Postgres for saving the 
# Run the application 

required 
- docker
- docker-compose 

### Steps
- run `docker-compose build`
- run `docker-compose up`
# Endpoints

## /shorten/{url}/
GET
The /shorten/{url}/ endpoint is used to retrieve a shortened version of the given url. The url is passed as a parameter in the path.

The response will be a JSON object with the properties id, url, shortened_url_id, title, and access_count.

## /top-titles/
GET
The /top-titles/ endpoint is used to retrieve the top titles of all the shortened URLs.

The response will be a JSON object with the properties url and title.

## /top-urls/
GET
The /top-urls/ endpoint is used to retrieve the top URLs based on the number of times they have been accessed.

The response will be a JSON object with the properties url and access_count.

## /url/{id}/
GET
The /url/{id}/ endpoint is used to retrieve information about a specific URL based on its id. The id is passed as a parameter in the path.

The response will be a JSON object with the properties id, url,
