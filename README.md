# ***Build Instructions***
***Activate virtual environment linux
To BUILD on linux you must have the psycopg2 pip package but it messes up the deployment so it cannot be inside of the requirement.txt***
```

```
***Activate virtual environment on windows and install packages***
```
python -m venv venv1
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv1\Scripts\activate  
pip install -r requirements.txt
```

***Then to run on both windows and linux run***
```
Windows -> python -m src.Main
Linux   -> python3 -m src.Main
```