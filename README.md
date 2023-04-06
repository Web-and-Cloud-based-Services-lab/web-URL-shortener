# URL-Shortener

*Web Services and Cloud-based Systems course Project*

**API Functions:** 
- List all IDs in use 
- Post a URL to the server and get a unique short ID
- Use the ID to retrieve the origianl URL
- Update a URL based on the ID
- Delete a URL based on the ID


**Additional Features:**
- ID generator
- Base10 to Base 62 converter
- URL validation（checked at Create and Update）
- Duplicate check（checked at Create and Update）
- Reuse deleted IDs 
- Connected with Database (MongoDB)
- A dataset with more than 100 thousands URLs (can choose the range of records to be added into database)

## Prerequisites

1. `Docker`  installed
2. `Python >= 3.4`  installed

## Build

### 1. Run the database

#### Pull `MongoDb` official image from docker

Run the following command to pull MongoDB

```bash
$ docker pull mongo:4.4.6
```

#### Run database

Run the following command to create a container

```bash
$ docker run --name mongo -p 27017:27017 -d mongo:4.4.6
```

### 2. Run the Server

After successfully installed these modules, enter  directory `/src` , run the python file `run.py`

```bash
$ python3 run.py
```

## Server API
| API | Parameter | Method | Example| Description |
| :--- | :---- | :---: |:---|:---|
| / |/ |  GET   | 127.0.0.1:5000/ | List Keys (short url id)|
/:id |/ |GET|127.0.0.1:5000/cwt|Use short id to retrieve original URL|
/:id|query parameter: [?url=...]|PUT|127.0.0.1:5000/?url=http://fuzz.com| Update existing URL by id|
/ | /| DELETE| 127.0.0.1:5000/ | Invalid Request| 
/:id |/| DELETE | 127.0.0.1:5000/cwt| Delete existing URL by id|
/ |query parameter: [?url=...] | POST  | 127.0.0.1:5000/?url=http://foo.com |Add a new outlet into the database|

