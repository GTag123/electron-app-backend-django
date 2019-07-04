# Electron.js backend on Django
Чтобы запустить:  
  
**0. Создай виртуальное окружение(необязательно):**  
```python -m venv [envname]```  
  
**1. Клонируешь репозиторий:**  
```git clone https://github.com/GTag123/electron-app-backend-django.git```  
  
**2. Установи зависимости:**  
```pip install -r requirements.txt```
  
**3. Примени миграции:**  
```python manage.py makemigrations```  
```python manage.py migrate```  
  
**4. Запускаешь сервак:**  
```python manage.py runserver [port]```
  
**5. Deploy frontend. See:**  ```https://github.com/GTag123/electron-app-frontend```
  