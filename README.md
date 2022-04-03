# padel-page


## Deploy webpage
```bash
docker build -t flask/padel-planner .
```
```bash
docker run -d -p 8003:8000 flask/padel-planner
```


## Deploy nginx
```bash
docker build -t nginx .
```
```bash
docker run -d -p 80:80 nginx
```
