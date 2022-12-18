# 檔案結構
![](https://i.imgur.com/BRAhPNK.png)

# Docker 部屬
1. 進入 gol-backend
```
cd gol-backend
```
2. build docker image
```
docker build -t gol-backend .
```
3. 
run docker container
```
docker run -d --name gol-backend-container -p 80:80 gol-backend
```

# FastAPI Docker
https://fastapi.tiangolo.com/deployment/docker/
