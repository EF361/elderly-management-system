# Elderly Management System ![Python](https://img.shields.io/badge/Python-v3.10-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-v1.xx-brightgreen) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-%3E=13-blue) ![License](https://img.shields.io/badge/License-MIT-success) ![Demo](https://img.shields.io/badge/Demo-Live-orange)

## Executive Summary
The Elderly Management System is a dynamic, AI-powered application designed to simplify and enhance the management of elderly care facilities. By leveraging real-time personalization via OpenAI and rich data handling capabilities with PostgreSQL, this solution ensures seamless operations while prioritizing resident well-being.

## Key Features
- **Comprehensive Resident Management**: Track, monitor, and update resident profiles, health metrics, and schedules in one intuitive interface.
- **AI-Driven Personalization**: Utilize OpenAI models to generate activity recommendations, dietary suggestions, and more, tailored to each resident's needs.
- **Streamlined Interface**: Built with Streamlit for easy navigation and user-friendly workflows.
- **Secure Data Storage**: Centralized data repository with PostgreSQL, ensuring scalability and reliability.
- **Role-Based Access Control (RBAC)**: Ensures that sensitive resident information is only accessible according to user roles (e.g., Admin, Healthcare Staff).
- **Real-Time Notifications**: Keep staff updated on critical alerts and events.
- **Scalable Architecture**: Built with modular components to support seamless future scaling.

## Architecture & Workflow
```mermaid
graph TD
    A[User Interface - Streamlit] --> B[API Gateway]
    B --> C[Resilient Backend System - Python]
    C --> D[PostgreSQL Database]
    C --> E[OpenAI Integration for Personalization]
    D --> F[Resident Data Storage]
    E --> G[AI-Based Recommendations]
    B --> H[Role-Based Access Control]
    H --> I[Data Privacy & Security Protocols]
```

1. **Streamlit (UI)**: Frontend designed for healthcare staff and administrators.
2. **Backend Logic**: Handles database interactions, AI integrations, and access policies.
3. **PostgreSQL Database**: Securely manages resident profiles, health metrics, and schedules.
4. **OpenAI Integration**: Delivers AI-enhanced personalized services for residents.

## Tech Stack & Tools Breakdown
- **Python**: Core language for backend logic, API integrations, and AI processing.
- **Streamlit**: Framework for building a clean, interactive user interface.
- **PostgreSQL**: Relational database for reliable and secure data management.
- **OpenAI API**: Enables intelligent personalization and recommendation systems.

## Data Security Protocols
Protecting resident privacy is a top priority. Here's how the system ensures data security:
- **Encrypted Data Storage**: Resident data is encrypted at rest and in transit using industry-standard AES-256.
- **Role-Based Access Control (RBAC)**: Staff access is limited to the scope required for their roles, minimizing potential exposure.
- **Activity Logging**: Every user interaction is logged to provide an auditable trail of access and modifications.
- **Environment Isolation**: Database and backend services are hosted securely, with network segmentation applied to block unnecessary access.
- **Regular Security Audits**: System undergoes periodic penetration testing and code reviews to identify and mitigate vulnerabilities.
- **Data Anonymization**: Sensitive information is anonymized in non-production and analysis environments.

## Quickstart / Installation
Clone the repository and set up the system with the following steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/EF361/elderly-management-system.git
   cd elderly-management-system
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up PostgreSQL Database**:
   - Create a database and configure the connection string in `.env`:
     ```
     DATABASE_URL=postgresql://user:password@localhost:5432/dbname
     ```

5. **Export OpenAI API Key**:
   ```bash
   export OPENAI_API_KEY=your_openai_api_key
   ```

6. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

7. **Access the Application**:
   Navigate to `http://localhost:8501` in your browser.

## License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/EF361/elderly-management-system/blob/main/LICENSE) file for details.