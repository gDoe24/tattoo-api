README dedicated to setting up the backend environment :)


## Endpoints

### GET /

*   Returns "Healthy" if the api is up and running properly

```
{
    'Healthy'
}
```
### GET /api/aritsts

*   Fetches a dictionary object of all artists in the database
*   Returns: array of artists containing key:value pairs of email, id, image_link, instagram_link,
    name, phone, and artists styles; and the total amount of artists in the database
```
{
    "artists": [
        {
            "email": "NULL",
            "id": 1,
            "image_link": "NULL",
            "instagram_link": "NULL",
            "name": "Kobe",
            "phone": "123-432-4231",
            "styles": "Neo"
        },
        {
            "email": "NULL",
            "id": 2,
            "image_link": "NULL",
            "instagram_link": "NULL",
            "name": "Lebron",
            "phone": "142-323-6123",
            "styles": "Traditional"
        }, ...
    "success": true
    "total_artists": 4
}
```
### GET /api/artists/<artist_id>

*   Fetches a dictionary object of the artist matching the artist id specified in the URI
*   Returns: a single dictionary object containing key:value pairs of email, id, image_link, instagram_link,
    name, phone number, and artist styles

```
{
    "artist": {
        "email": "NULL",
        "id": 2,
        "image_link": "NULL",
        "instagram_link": "NULL",
        "name": "Lebron",
        "phone": "142-323-6123",
        "styles": "Traditional"
    },
    "success": true
}
```
### GET /api/clients

*   Fetches a dictionary object of paginated clients
*   Returns an array for all clients containing a dictionary of client key:value pairs for each 
    client's id, address, email, name, and phone number

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
### GET /api/clients/<client_id>
```
{
    "client": {
        "address": "NULL",
        "email": "NULL",
        "id": 1,
        "name": "Patrick",
        "phone": "NULL"
    },
    "success": true
}
```
### GET /api/appointments/<appointment_id>
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
### POST /api/artists
```
{
    "name": "Tony Montana",
    "phone": "123-456-7891",
    "styles": "Neo-Traditional",
    "image_link": "fakepic@unsplash.com",
    "instagram_link": "fakeig123@instagram.com",
    "email": "TonyMontana@hotmail.com"
}
```
Returns
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
### POST /api/clients
```
{
    "name": "Joe Schmo",
    "phone": "231-124-1412",
    "email": "",
    "address": ""
}
```
Returns
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
### POST /api/appointments
```
{
    "client": 1,
    "artist": 1,
    "appointment_date": "Mon, 06 Mar 2021 14:30:00 GMT"
}
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
### PATCH /api/artists/<artist_id>
```
{
    "phone": "901-212-4321",
    "email": "creative_genius@aol.com"

}
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
### PATCH /api/clients/<client_id>
```
{
    "phone": "770-231-4234",
    "email": "simplord12@gmail.com"
}
```
Returns
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
### PATCH /api/appointments/<appointment_id>
```
{ 
    "appointment_date": "Sat, 06 Jun 2021 14:30:00 GMT"
}
```
Returns
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
### DELETE /api/artists/<artist_id>
```
{
    "deleted_artist_id": 5,
    "success": true,
    "total_artists": 4
}
```
### DELETE /api/clients/<client_id>
```
{
    "deleted_client_id": 6,
    "success": true,
    "total_clients": 5
}
```
### DELETE /api/appointments/<appointment_id>
```
{
    "deleted_appointment_id": 3,
    "success": true,
    "total_upcoming_appointments": 4
}
```
