# Local_Culinary_Explorer_API
A Django Rest framework-based API for discovering and managing local cuisines,
featuring authentication, dish management, chef profiles, ingredient tracking, reviews, and recommendations.

## Features  
- User authentication (JWT-based)  
- Dish management (CRUD operations)  
- Chef profiles  
- Ingredient tracking  
- User reviews 
- Personalized dish recommendations

## Installation  

1. **Clone the repository**  
   ```bash
   git clone https://github.com/dativardzma/Local_Culinary_Explorer_API.git
   cd Local_Culinary_Explorer_API
   cd Local_Culinary

2. **Create a virtual environment & activate it**
   ```bash
   python -m venv env  
   source env/bin/activate  # On Windows use: env\scripts\activate

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt

4. **Run migrations**
   ```bash
   python manage.py migrate

5. **Start the development server**
   ```bash
   python manage.py runserver


### **API Endpoints**  
Provide examples of how to use the API.  

📌 **Example:**  
```md
## API Endpoints  
```

### Authentication  
- `POST register/` → Register a new user  
- `POST login/` → Log in and receive a token  


### Dishes  
- `GET dishes/` → Get a list of all dishes  
- `POST dish/create` → Create a new dish (authenticated users only)



## Technologies Used  
- Python 3.x  
- Django REST Framework  
- SQLite (or PostgreSQL)  
- JWT Authentication  
- Git for version control  


## Contact  
Created by David Svanidze - dati.svanidze123@gmail.com
GitHub: ["https://github.com/dativardzma"](My Github account)

