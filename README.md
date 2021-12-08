# Django project: Online Shop #

This is an application for an Online store website using the Django framework.

## UseCase Diagram ##

![alt text](myshop/docs/assets/use_case_diagram.png | width=100)

## Project Structure ##

myshop  
├── accounts  
├── cart  
├── manage.py  
├── media  
├── myshop  
├── orders  
├── requirements.txt  
├── shop  
└── venv  

## Stack of Technologies ##

Python==3.8.2  
Django==3.2.9  
docker==20.10.11  
Pillow==8.4.0  
celery==4.4.2  
redis==3.2.0  
pcycopg2-binary 2.9.2

## Get Started ##

To set up the PyShop project, here is the following guideline:

- Run postgres and redis:
```bash
docker-compose up
```

In another terminal:

- Use the python virtualenv tool:
```bash
virtualenv venv
source venv/bin/activate
```

- Install the requirements in your virtual environment:
```bash
pip install -r requirements.txt
```
- Create and run migrations, add the admin user:
```bash
# Migrations
python manage.py makemigrations
python manage.py migrate
# Create admin user
python manage.py createsuperuser
```

- Start the dev server:
```bash
python manage.py runserver
```

- Visit your App using http://127.0.0.1:8000
- Follow the registration link, fill following fields `Email` , `Phone` , `Password`, `Password confirm`
- Visit Admin Page using http://127.0.0.1:8000/admin and login with the credentials created above
- Add Categories under Categories Menu, also add Products under the Products Menu
- Visit the main Products Page: http://127.0.0.1:8000/
- Add Products to the Wishlist or a Cart
- Manage your Wishlist: http://127.0.0.1:8000/accounts/wishlist
- Manage your Cart: http://127.0.0.1:8000/cart/
- Create your Order: http://127.0.0.1:8000/orders/create/

