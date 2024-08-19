## Create virtual ENV
```python
python -m venv env
```
## Install Dependencies
```python
pip install -r requirements.txt
```
## Run using uvicorn
```python
uvicorn main:app --reload
```
- main refers to main.py file and app is the FastAPI instance