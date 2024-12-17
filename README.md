# QVAKK - Online Quiz Platform  

QVAKK is an engaging and customizable online quiz platform designed to provide users with an intuitive and fun experience. Users can create personalized quizzes, track their results, and even share them via email. The platform is built with a mobile-first approach, ensuring seamless performance across all devices.  

---

## Features  

### User Authentication  
- **Google Login Integration**: Secure and hassle-free login with Google.  

### Quiz Customization  
- Users can select quiz topics, difficulty levels, and number of questions.  
- Questions are fetched dynamically using a quiz API.  

### Results Display and Emailing  
- Instant quiz result display after completion.  
- Email results functionality for user convenience.  

### Responsive Design  
- Fully responsive design ensuring smooth usability across desktops, tablets, and mobile devices.  

### User Dashboard  
- A personal profile page to view and manage quizzes.  

---

## Tech Stack  

### Backend  
- **Flask**: Lightweight web framework used for API handling and server-side logic.  
- **MongoDB**: NoSQL database for efficient data storage and retrieval.  

### Frontend  
- **HTML5**, **CSS3**, **JavaScript**: For building responsive and interactive UI.  
- **Tailwind CSS**: Utility-first CSS framework for quick and customizable designs.  

### APIs  
- Quiz API to fetch questions based on user preferences.  

### Authentication  
- **Google OAuth 2.0**: Secure user login and authentication.  

---

## Installation and Setup  

### Prerequisites  
1. Python 3.8+  
2. MongoDB installed locally or accessible via a cloud service.  
3. A Google Developer account for OAuth credentials.  

### Steps  

1. Clone the repository:  
   ```bash
   git clone https://github.com/your-repo/qvakk.git
   cd qvakk

2. Set up a virtual environment and install dependencies:
   ```bash
    python -m venv venv
    source venv/bin/activate  # For Windows: venv\Scripts\activate
    pip install -r requirements.txt

3. Configure Environment Variables
   - Create a .env file in the root directory and include the following:
   ```bash
    FLASK_APP=app.py
    FLASK_ENV=development
    MONGO_URI=mongodb://localhost:27017/qvakk
    GOOGLE_CLIENT_ID=<your-google-client-id>
    GOOGLE_CLIENT_SECRET=<your-google-client-secret>

4. Run the app:
   ```bash
    flask run

5. Access the Application:
   Open your browser and navigate to: http://127.0.0.1:5000




 








