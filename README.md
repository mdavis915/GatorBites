# GatorBites
GatorBites is a React-based web application that allows users to search for recipes based on ingredients and tags. The app dynamically filters recipes and displays detailed information, including matching and missing ingredients, estimated cooking time, and relevant tags. The user then has the opportunity to select on these recipes and view more information regarding the recipe, such as its descriptions and instructions. The project utilizes two data structures to achieve the project's task: a hashmap and a trie. 


## Setup Instructions

### Prerequisites
- Node.js
- Python
- Git

### 1. Clone the Repository
   ```bash
git clone https://github.com/mdavis915/GatorBites.git
cd GatorBites
```

## 2. Set Up the Backend
- Navigate to the `backend` directory:
  
  ```bash
  cd backend
- Install the following dependencies
  
  ```bash
  pip install flask, flask-cors, pandas
- Start the Flask server:
  
  ```bash
  python main.py
  By default, the backend will be accessible at:
  ```bash
  http://127.0.0.1:5000

## 3. Set Up the Frontend
- Open a new terminal and ensure you're in the **GatorBites** root directory
- Navigate to the `frontend` directory
  
  ```bash
  cd frontend
- Install Node.js dependencies:
  ```bash
  npm install
- Start the React development server:
  ```bash
  npm start
  ```
  By default, the frontend will be accessible at:
  ```bash
  http://localhost:3000
  ```
  
## 4. Using the Application
- After starting the backend server with `python main.py` and the frontend with         `npm start`, open your brower and navigate to `http://localhost:3000` if not loaded automatically.
    
## 5. Interacting with the App
- Once the frontend is loaded, you can search for recipes by entering ingredients         in the search bar and filtering using tags. Users also have the opportunity to 
        select between a Trie or Hashmap to perform all operations and sort the order 
        in how the found recipes are displayed.
- You can view more detailed information about a recipe, such as instructions and 
        descriptions, by selecting a recipe from the recipe list.

## 6. Stopping the Servers
-  To stop the backend server, press `Ctrl + C` in the terminal where you started it.
-  To stop the frontend server, press `Ctrl + C` in the terminal where you ran npm 
     start.

   
