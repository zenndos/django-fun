# Type based creator

A django application which creates dynamic tables/models.

One particular cool feature of this application is that it preserves the ability to access the models even after application restart. I've spent several hours figuring out this feature alone. Django normally loads it's models to the registry from the source code, so upon restart the information about dynamic models is usally lost. I use a small dirty trick to bypass that limitation - I regenrate the models on the fly by quering the fields/columns. This allows me to preserve the models even if the application is restarted.

# How to run things

To run this locally you will need poetry. 

Simply execute:
```bash
curl -sSL https://install.python-poetry.org | python - --version "1.4.2"
```
Once the poetry is installed you can install the application with:
```bash
make setup
```

You can run tests with:
```bash
make test
```

And you can start the application for manual testing with:
```bash
make server
```

## API endpoints and how to make requests
### Table Enpoint

**POST** http://localhost:8005/table - create dynamic model.



*The request body should be in format {name:type}:*

```json
{
    "field_1": "number",
    "field_2": "boolean"
}
```
Accepted types: 
 - number
 - boolean
 - string

*Example cURL:*

```bash
curl --request POST \
  --url http://localhost:8005/table \
  --header 'Content-Type: application/json' \
  --data '{
  "field_1": "number",
  "some_field": "boolean"
}'
```

---
**GET** http://localhost:8005/table/{id} - get dynamic model.

*Example cURL:*

```bash
curl --request GET \
  --url http://localhost:8005/table/1 \
  --header 'Content-Type: application/json'
```

**PUT** http://localhost:8005/table/{id} - update dynamic model. Sets new fields to the model and updates the types of the existing fields if provided in payload.

*Example cURL:*

```bash
curl --request PUT \
  --url http://localhost:8005/table/1 \
  --header 'Content-Type: application/json' \
  --data '{
  "field_1": "boolean",
  "some_field": "string",
  "new_field": "number"
}'
```

### Cool Table Endnpoint
Cool table is pretty similar with the key difference that the expected format of the request is: {title:value}

Title can be any string and value should be of the type int/float/boolean/string. The application will determine the type of the value and will created fields named according to title and with the type corresponding to the value type. Since we are not creating instances of the table, the actual value will be ignored and only used for the type extraction.

**POST** http://localhost:8005/cool-table - create dynamic model.

Example body:
```json
{
    "field_1": "some string",
    "field_2": true,
    "filed_3": 14
}
```

*Example cURL:*

```bash
curl --request POST \
  --url http://localhost:8000/cool-table \
  --header 'Content-Type: application/json' \
  --data '{
  "field_1": true
}'
```

---

**PUT** http://localhost:8005/cool-table/1 - create dynamic model.

*Example cURL:*

```bash
curl --request PUT \
  --url http://localhost:8005/cool-table/1 \
  --header 'Content-Type: application/json' \
  --data '{
  "field_1": -3,
  "some_interesting_field": "meaningless_text"
}'
```

**NOTE**: there is a problem with updating boolean to postgres-specific double precision field, so it is recommend to only use intergers.

### Row Endnpoint

**POST** http://localhost:8005/table/row - create a row dynamic model.

**NOTE**: the request must contain the fields with the same names and types as the current dynamic model, overwise you'll get back a bad request.

*Example cURL:*

```bash
curl --request POST \
  --url http://localhost:8005/table/1/row \
  --header 'Content-Type: application/json' \
  --data '{
  "field_1": 12,
  "new_field": false,
  "some_field": "dfgdfsd",
  "some_interesting_field": "dfsdfdsf"
}'
```
---

**GET** http://localhost:8005/table/rows - gets all rows of a dynamic model.

*Example cURL:*

```bash
curl --request GET \
  --url http://localhost:8005/table/1/rows \
  --header 'Content-Type: application/json'
```
