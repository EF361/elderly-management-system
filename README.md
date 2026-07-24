# Elderly Management System  
![Python](https://img.shields.io/badge/Python-3.10-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.6.0-red) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-blue) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-green) ![Plotly](https://img.shields.io/badge/Plotly-5.6.0-orange) ![OpenAI](https://img.shields.io/badge/OpenAI-API-yellow)

## Business Value  
The **Elderly Management System** is a streamlined software solution for enhancing efficiency and quality of care within elderly care facilities.  
- **For Staff & Administrators**: Automate daily operations like resident monitoring, health tracking, task assignments, and more.  
- **For Residents**: Personalize recommendations for health plans, activities, and diets tailored by AI.  
- **For Continuous Improvement**: Integrated user feedback loop ensures that the AI provides smarter, more efficient recommendations over time.  

Ultimately, it enhances facility workflows and prioritizes well-being for those who matter the most, all while reducing administrative overhead.

---

## Tech Stack  
- **Backend**: Python + SQLAlchemy  
- **Frontend**: Streamlit for seamless, interactive user interfaces  
- **Database**: PostgreSQL for scalable, reliable data storage  
- **AI Integration**: OpenAI API for personalized resident recommendations  
- **Data Visualization**: Plotly for real-time insights and analytics  

---

## How It Works  

### 1. **Resident Management**  
Admins can easily add, update, or delete resident data (e.g., name, medical history, dietary preferences). All records are stored securely using PostgreSQL with SQLAlchemy as the ORM.  

### 2. **AI-Powered Personalization**  
Through OpenAI's API, the system generates personalized health and activity recommendations for each resident. Inputs like health details and preferences are processed to create adaptive care suggestions.  

### 3. **Data Reporting and Monitoring**  
Interactive dashboards built with Plotly visualize statistics like health trends, attendance patterns, and staff performance. This promotes informed decision-making.  

### 4. **User Feedback Integration**  
- Residents and staff can now submit structured feedback directly on AI-generated recommendations.  
- Feedback is logged, analyzed, and used to retrain the recommendation model periodically, ensuring continuous improvement over time.  

### 5. **Scalability and Security**  
Built with enterprise-grade tools (PostgreSQL + SQLAlchemy), this system is designed to handle increasing user loads without compromising performance or security.

---

## Getting Started  
1. Clone the repository:  
   ```bash
   git clone https://github.com/EF361/elderly-management-system.git
   cd elderly-management-system
   ```  

2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  

3. Set up your `.env` file with the following environment variables:  
   ```bash
   DATABASE_URL=your_postgresql_database_url
   OPENAI_API_KEY=your_openai_api_key
   ```  

4. Start the Streamlit App:  
   ```bash
   streamlit run app.py
   ```  

---

## Contributing  
We welcome contributions to enhance the **Elderly Management System**!  
- Report bugs or suggest features via `Issues`.  
- Submit a pull request for proposed improvements.  

---

## License  
This project is licensed under the MIT License. See the `LICENSE` file for more details.  

--- 

Built with ❤️ for smarter and more compassionate elderly care solutions.