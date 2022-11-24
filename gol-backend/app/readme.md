# 執行步驟
1. 創建 env
```
python -m venv migration_env
```
2. 開啟 env
```
.\app\migration_env\Scripts\activate.ps1
```
3. 
在 env 裡 install requirements.txt
```
app\migration_env\Scripts\pip install -r requirements.txt
```

# migration command
- 在 app 路徑執行，不然找不到 alembic.ini
## 升級
```
.\migration_env\Scripts\alembic upgrade head
```
## 確認版本
```
.\migration_env\Scripts\alembic current 
```

# 參考資料
## database migration(資料庫版本控制) 
https://medium.com/@acer1832a/%E4%BD%BF%E7%94%A8-alembic-%E4%BE%86%E9%80%B2%E8%A1%8C%E8%B3%87%E6%96%99%E5%BA%AB%E7%89%88%E6%9C%AC%E7%AE%A1%E7%90%86-32d949f7f2c6

# alembic 放置位子
![](https://i.imgur.com/1eoAtXE.png)

