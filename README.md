***To BUILD on linux you must have the psycopg2 pip package but it messes up the deployment so it cannot be inside of the requirement.txt***
***And for some reason only module imports are guarenteed to work***
```
run on linux 
python3 -m src.Main
```

```
run on windows, shortcut does not work
python src/Main.py