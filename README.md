# sentiment analyzer

**Web API wrapper for the model - backend part**


[//]: # (FIXME)
### [Website]()


## Run by yourself

### Pipenv

```shell
git clone https://github.com/a-tagiev/hse_sentiment
cd hse_sentiment
pipenv install
pipenv run uvicorn main:app
```

### Pure python 3.12

Windows (PowerShell) (not tested):
```powershell
git https://github.com/a-tagiev/hse_sentiment
cd hse_sentiment
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app
```

Linux / MacOS:
```shell
git clone https://github.com/a-tagiev/hse_sentiment
cd hse_sentiment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app
```

## Stack

- [python 3.12](https://python.org) - programming language
- [scikit-learn](https://pypi.org/project/scikit-learn) - Logistic regression
- [FastAPI](https://pypi.org/project/fastapi) - web server engine
- And more
