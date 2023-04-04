# Web-Service-Asg1

### Prerequisites

1. `Docker`  installed
2. `Python >= 3.4`  installed

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

#### Run the API

After successfully installed these modules, enter  directory `/src` , run the python file `run.py`

```bash
$ python3 run.py
```

Here is the list of API provided:

| API | Parameter | Method | Example| Description |
| :--- | :---- | :---: |:---|:---|
| / |/ |  GET   | 127.0.0.1:5000/ | List Keys (short url id)|
/:id |/ |GET|127.0.0.1:5000/cwt|Use short id to retrieve original URL|
/:id|query parameter: [?url=...]|PUT|127.0.0.1:5000/?url=http://fuzz.com| Update existing URL by id|
/ | /| DELETE| 127.0.0.1:5000/ | Invalid Request| 
/:id |/| DELETE | 127.0.0.1:5000/cwt| Delete existing URL by id|
/ |query parameter: [?url=...] | POST  | 127.0.0.1:5000/?url=http://foo.com |Add a new outlet into the database|