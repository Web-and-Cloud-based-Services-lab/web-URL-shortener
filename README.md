# URL-Shortener

*Web Services and Cloud-based Systems course Project*

**API Functions:** 
- List all IDs in use 
- Post a URL to the server and get a unique short ID
- Use the ID to retrieve the origianl URL
- Update a URL based on the ID
- Delete a URL based on the ID


**Additional Features:**
- user authentication included
- ID generator
- Base10 to Base 62 converter
- URL validation（checked at Create and Update）
- Duplicate check（checked at Create and Update）
- Reuse deleted IDs 
- Connected with Database (MongoDB)
- A dataset with more than 100 thousands URLs (can choose the range of records to be added into database)

### Reference
**URL Validation Regex:**
The design of valid regex pattern is based the idea offered by YUVRAJ CHANDRA.
The pattern is modified to also supports urls not starting with `http(s)`
[link](https://www.makeuseof.com/regular-expressions-validate-url/)

**Base10 to Base62 algorithm:**
The implementation of the Base10 to Base62 converter is based on the ideas and pseudocode provided by Marcel Jackwerth
[link](https://stackoverflow.com/questions/742013/how-do-i-create-a-url-shortener)

**Progress Bar:**
We refer to the syntax of tqdm (a library that supports progress bar) in one of the answers from stackoverflow.
[link](https://stackoverflow.com/questions/43259717/progress-bar-for-a-for-loop-in-python-script)

## Prerequisites

1. `Docker`  installed
2. `Python >= 3.4`  installed


## Docker

<!-- Buid
```shell
docker build -t reisafriche/url-service:v1 .
```

push
```shell
docker push reisafriche/url-service:v1  
``` -->

<!-- pull docker image
```shell
docker pull reisafriche/url-service:v1 -->
```

run docker container
```shell
docker run --name url-service -p 5000:5000 docker.io/reisafriche/url-service:v1
```


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
| / |[?jwt=...] |  GET   | 127.0.0.1:5000/ | List Keys(short url id) owned by the user|
/:id |/ |GET|127.0.0.1:5000/cwt|Use short id to retrieve original URL|
/:id|[?url=...&jwt=...]|PUT|127.0.0.1:5000/?url=http://fuzz.com| Update existing URL by id|
/ | /| DELETE| 127.0.0.1:5000/ | Invalid Request| 
/:id |[?jwt=...]| DELETE | 127.0.0.1:5000/cwt| Delete existing URL by id|
/ |[?url=...&jwt=...] | POST  | 127.0.0.1:5000/?url=http://foo.com |Add a new outlet into the database|

