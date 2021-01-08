README dedicated to setting up the backend environment :)

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) is used to handle the SQLAlchemy migrations for Flask applications using Alembic

## Database Setup
With Postgres running, restore a database using the tattoo_shop.psql file provided. From the backend folder in terminal run:
```bash
psql tattoo_shop < tattoo_shop.psql
```


## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## API Reference

### Getting Started

BASE URL: The backend is hosted at the default URL, https://bookthattat.herokuapp.com/

### Authorization

The Tattoo Shop API uses the Auth0 ([see docs](https://auth0.com/docs/)) API for authorizing role based authentication. The three roles associated with the Tattoo Shop Api from least priveleged to most priveleged are:

1. Client
    * Endpoint Accessibility
        * GET
            * /api/appointment/appointment_id
2. Artist
    * Endpoint Accessibility
        * GET
            * The tattoo artist has access to all GET endpoints
        * POST
            * /api/clients
            * /api/appointments
        * PATCH
            * /api/clients
            * /api/appointments
3. Manager
    * The tattoo shop manager has access to all API endpointss
    
*No authorization is required for GET /api/artists or /api/artists/artist_id endpoints*

### Errors

Errors are returned as JSON objects in the following format:

```
{
  "error": 404, 
  "message": "Resource Not Found", 
  "success": false
}
```
The API recognizes three error types for failed requests:

* 400
* 401
* 403
* 404
* 422
* 500

## Resources/Endpoints

*Note: In order to use many of the following endpoints, you will need to obtain the necessary json web tokens in accordance with the endpoint's authorization restrictions. See [testing section](#testing) for more details*
#### GET /

*   Returns "Healthy" if the api is up and running properly
*   curl https://bookthattat.herokuapp.com/

```
{
    'Healthy'
}
```

### Artist

This is an object representing a tattoo artist. This API allows you to retrieve a single artist, or a group of all artists in the database. You can also create, update and delete an artist (with the allowed permissions) using the POST, PATCH, and DELETE methods respectively.

##### Attributes

**id** `integer`
> Unique identifier for the object

**email**  `string`
> The tattoo artist's email address

**image_link** `string`
> Link to the primary image of the tattooer

**instagram_link** `string`
> Link to the tattoo artist's instagram

**name** `string`
> The name of the tattoo artist

**phone** `string`
> The artist's phone number

**styles** `string`
> The styles in which the artist specializes in

```
"artist": {
        "email": "lebron_jaimes@aol.com",
        "id": 2,
        "image_link": "https://unsplash.com/photos/zfasedr13",
        "instagram_link": "https://instagram.com/lebronjaimes24",
        "name": "Lebron",
        "phone": "142-323-6123",
        "styles": "Traditional"
    }
```

#### GET /api/aritsts

*   Retrieves all artists in the database
*   Returns an array of artist objects and the total number of artists in the database
`curl https://bookthattat.herokuapp.com/api/artists`

Returns:
```
{
    "artists": [
        {
            "email": "bean@aol.com",
            "id": 1,
            "image_link": "https://unsplash.com/goat",
            "instagram_link": "https://instagram.com/mamba4ever",
            "name": "Kobe",
            "phone": "123-432-4231",
            "styles": "Neo"
        },
        {
            "email": "lebron_jaimes@aol.com",
            "id": 2,
            "image_link": "https://unsplash.com/photos/zfasedr13",
            "instagram_link": "https://instagram.com/lebronjaimes24",
            "name": "Lebron",
            "phone": "142-323-6123",
            "styles": "Traditional"
        }, ...
    ],
    "success": true
    "total_artists": 4
}
```
#### GET /api/artists/<artist_id>

*   Fetches the artist resource matching the artist_id specified in the URI
*   Returns: a single artist object

`curl https://bookthattat.herokuapp.com/api/artists/2`

Returns:
```
{
    "artist": {
        "email": "lebron_jaimes@aol.com",
        "id": 2,
        "image_link": "https://unsplash.com/photos/zfasedr13",
        "instagram_link": "https://instagram.com/lebronjaimes24",
        "name": "Lebron",
        "phone": "142-323-6123",
        "styles": "Traditional"
    },
    "success": true
}
```
#### POST /api/artists

*   Create a new tattoo artist resource
*   Parameters
    *   name **required**
    *   phone
    *   email
    *   instagram_link
    *   styles
    *   image_link

```
curl https://bookthattat.herokuapp.com/api/artists -X POST \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $MANAGER_JWT" \
-d '{ "name": "Tony Montana", "phone": "123-456-7891", "styles": "Neo-Traditional", \
"image_link": "fakepic@unsplash.com", "instagram_link": "fakeig123@instagram.com", \
"email": "TonyMontana@hotmail.com" }'
```

Returns:
```
{
    "artist": {
        "email": "TonyMontana@hotmail.com",
        "id": 5,
        "image_link": "fakepic@unsplash.com",
        "instagram_link": "fakeig123@instagram.com",
        "name": "Tony Montana",
        "phone": "123-456-7891",
        "styles": "Neo-Traditional"
    },
    "success": true,
    "total_artists": 5
}
```
#### PATCH /api/artists/<artist_id>

*   Updates the specified tattoo artist matching the artist_id in the URI by passing in parameters with new values. Any parameters not specified will not be changed.
*   Parameters
    *   name 
    *   phone
    *   email
    *   instagram_link
    *   styles
    *   image_link

```
curl https://bookthattat.herokuapp.com/api/artists/3 -X PATCH \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $MANAGER_JWT" \
-d '{"phone": "901-212-4321", "email": "creative_genius@aol.com"}'
```

Returns
```
{
    "artist": {
        "email": "creative_genius@aol.com",
        "id": 3,
        "image_link": "NULL",
        "instagram_link": "NULL",
        "name": "Dwyane",
        "phone": "901-212-4321",
        "styles": "Japenese"
    },
    "success": true
}
```

#### DELETE /api/artists/<artist_id>

*   Delete an existing artist from the database specified by the artist_id in the URI. This action also deletes any existing appointments the tattoo artist had scheduled

```
curl https://bookthattat.herokuapp.com/api/artists/3 -X DELETE \
-H "Authorization: Bearer $MANAGER_JWT" 
```

Returns:
```
{
    "deleted_artist_id": 5,
    "success": true,
    "total_artists": 4
}
```

### Client

This object represents a client in the tattoo shop's database. The API allows for retrieving individaul as well as all clients in the database; creating a new client; and updating or deleting an existing client.

##### Attributes

**id** `integer`
> Unique identifier for the object

**name** `string`
> The name of the tattoo shop client

**address**  `string`
> The client's home address

**email**  `string`
> The client's email address

**phone** `string`
> The client's phone number

```
{
    "id": 1,
    "name": "Patrick",
    "address": "1234 Cheifs Way",
    "email": "new_goat@gmail.com",
    "phone": "429-321-5023"
}
```

#### GET /api/clients

*   Fetches a paginated list of clients
*   Returns an array of client objects for all clients in the database and the total number of clients

```
curl https://bookthattat.herokuapp.com/api/clients \
-H "Authorization: Bearer $MANAGER_JWT"
```

Returns:
```
{
    "clients": [
        {
            "address": "NULL",
            "email": "NULL",
            "id": 1,
            "name": "Patrick",
            "phone": "NULL"
        },
        {
            "address": "NULL",
            "email": "NULL",
            "id": 2,
            "name": "Deshaun",
            "phone": "NULL"
        },...
    ],
    "success": true,
    "total_clients": 5
}
```
#### GET /api/clients/<client_id>

*   Retrieve the client resource matching the client_id specified in the URI
*   Returns respective client object

```
curl https://bookthattat.herokuapp.com/api/clients/1 \
-H "Authorization: Bearer $MANAGER_JWT"
```

Returns:
```
{
    "client": {
        "id": 1,
        "name": "Patrick",
        "address": "1234 Cheifs Way",
        "email": "new_goat@gmail.com",
        "phone": "429-321-5023"
    },
    "success": true
}
```
#### POST /api/clients

*   Create a new client resource in the database
*   Returns the newly created client object and the total number of clients now in the database

```
curl https://bookthattat.herokuapp.com/api/clients \
-H "Authorization: Bearer $MANAGER_JWT" \
-H "Content-Type: application/json" \
-d '{ "name": "Joe Schmo", "phone": "231-124-1412", "email": "", "address": ""}
```

Returns:
```
{
    "client": {
        "address": "",
        "email": "",
        "id": 6,
        "name": "Joe Schmo",
        "phone": "231-124-1412"
    },
    "success": true,
    "total_clients": 6
}
```
#### PATCH /api/clients/<client_id>

*   Update the existing client specified by the client_id in the URI. Any parameters not specified will not be updated
*   Returns the updated client object

```
curl https://bookthattat.herokuapp.com/api/clients/3 \
-H "Authorization: Bearer $MANAGER_JWT" \
-H "Content-Type: application/json" \
-d '{"phone": "770-231-4234", "email": "simplord12@gmail.com"}
```

Returns:
```
{
    "client": {
        "address": "NULL",
        "email": "simplord12@gmail.com",
        "id": 3,
        "name": "Aaron",
        "phone": "770-231-4234"
    },
    "success": true
}
```
#### DELETE /api/clients/<client_id>

*   Permanently deletes the client resource specified in the URI by the client_id
*   Returns the deleted client's id along with the total number of clients remaining in the database

```
curl curl https://bookthattat.herokuapp.com/api/clients/6 \
-H "Authorization: Bearer $MANAGER_JWT"
```

Returns:
```
{
    "deleted_client_id": 6,
    "success": true,
    "total_clients": 5
}
```


### Appointment

Tattoo artists and clients use the appointment object to set a date and time for a tattoo session. The object contains three attributes: the artist id, client id, and appointment date. This API allows for retrieving, creating, updating, and deleting individual appointments

##### Attributes

**id** `integer`
> Unique identifier for the object

**artist** `integer`
> The id of requested artist

**client** `integer`
> The id of the client getting the tattoo

**appointment_date** `string`
> The date and time of the appointment
> Formatted example: "Mon, 24 Jun 2021 12:00:00 GMT"

```
{
    "id": 1,
    "artist": 1,
    "client": 1,
    "appointment_date": "Sat, 21 Mar 2021 12:00:00 GMT",
}
```
#### GET /api/appointments/<appointment_id>

*   Retrives the appointment resource specified by the appointment_id in the URI
*   Returns the respective appointment object

```
curl https://bookthattat.herokuapp.com/api/appointments/id \
-H 'Authorization: Bearer $MANAGER_JWT'
```

Returns: 
```
{
    "appointment": {
        "appointment_date": "Sat, 21 Mar 2021 12:00:00 GMT",
        "artist": 1,
        "client": 1,
        "id": 1
    },
    "success": true
}
```


#### POST /api/appointments

*   Create a new appointment resource in the database
*   Returns the newly created appointment object and the total number of upcoming appointments

```
curl https://bookthattat.herokuapp.com/api/appointments -X POST \
-H 'Authorization: Bearer $MANAGER_JWT' \
-H 'Content-Type: application/json' \
-d '{"client": 1, "artist": 1, "appointment_date": "Mon, 06 Mar 2021 14:30:00 GMT"}'
```

Returns
```
{
    "appointment": {
        "appointment_date": "Sat, 06 Mar 2021 14:30:00 GMT",
        "artist": 1,
        "client": 1,
        "id": 5
    },
    "success": true,
    "total_upcoming_appointments": 5
}
```


#### PATCH /api/appointments/<appointment_id>

*   Update an existing appointment specified in the URI by the appointment_id. Any parameters not specified will not be changed.
*   Returns the appointment object

```
curl https://bookthattat.herokuapp.com/api/appointments/3 -X PATCH \
-H 'Authorization: Bearer $MANAGER_JWT' \
-H 'Content-Type: application/json' \
-d '{ "appointment_date": "Sat, 06 Jun 2021 14:30:00 GMT" }'
```

Returns:
```
{
    "appointment": {
        "appointment_date": "Sun, 06 Jun 2021 14:30:00 GMT",
        "artist": 3,
        "client": 2,
        "id": 3
    },
    "success": true
}
```


#### DELETE /api/appointments/<appointment_id>

*   Permanently delete an existing appointment resource from the database
*   Returns the id of the deleted appointment along with the total number of upcoming appointments

```
curl https://bookthattat.herokuapp.com/api/appointments/3 -X DELETE \
-H 'Authorization: Bearer $MANAGER_JWT'
```

Returns:
```
{
    "deleted_appointment_id": 3,
    "success": true,
    "total_upcoming_appointments": 4
}
```


## Testing

The Tattoo Shop API uses role based authentication to verify json web tokens passed in by the request header. In order to utilize these endpoints in testing, you will need to set the environment variables for the CLIENT_JWT, ARTIST_JWT, and MANAGER_JWT.

To accomplish this, we will need to log into the application through Auth0 and grab the json web token that is returned in the url. [Click here](https://fsnd-8.us.auth0.com/authorize?audience=https://tattoo-api&response_type=token&client_id=PpM2OEplVJlEyE5xx3vLSb7RmMmQdF1C&redirect_uri=https://localhost:8100/) to log in.

Next, we will set the environment variables for the corresponding role.

```bash
export MANAGER_JWT='returned web token'
export CLIENT_JWT='returned web token'
export ARTIST_JWT='returned web token'
```

To run tests using the test database file provided, with Postgres running, enter the commands:

```bash
psql createdb test_tattoo_shop
psql test_tattoo_shop < test_tattoo_shop.psql
python test_app.py
```