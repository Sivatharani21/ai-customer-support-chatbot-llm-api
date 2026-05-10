```text
===========================================================================
README.txt
Project: Implementation of AI-Based Customer Support Chatbot Using LLM and API Integration
===========================================================================

# OVERVIEW
This project is an intelligent chatbot-based B2B support system designed to replace traditional form-based ticketing. It leverages Large Language Models (LLMs) to understand natural language queries, extract necessary information, and integrate with backend APIs to automatically generate and manage structured support tickets,,.

# TECHNOLOGIES USED
- Programming Language: Python
- Frontend: Streamlit
- Backend: FastAPI
- AI Frameworks: LangChain, LangGraph
- Database: SQLite

---------------------------------------------------------------------------
# SETUP & INSTALLATION (For VS Code)
---------------------------------------------------------------------------
1. Open your terminal in VS Code.
2. Clone the repository and navigate into the project folder:
   git clone <repository_url>
   cd project-folder

3. Create and activate a virtual environment:
   python -m venv env
   env\Scripts\activate

4. Install the required dependencies:
   pip install -r requirements.txt

5. Configuration:
   - Create a `.env` file in the root directory and add your API keys.
   - Configure the backend API URL in your Streamlit app script.

---------------------------------------------------------------------------
# HOW TO RUN THE APPLICATION
---------------------------------------------------------------------------
You need to run the backend and frontend simultaneously in two separate VS Code terminals.

1. Run the Backend (FastAPI):
   uvicorn main:app --reload

2. Run the Frontend (Streamlit):
   streamlit run app.py

---------------------------------------------------------------------------
# SYSTEM MODULES & CORE FUNCTIONS (Code Reference)
---------------------------------------------------------------------------
When writing or reviewing the code in VS Code, you will interact with the following core modules and functions:

1. User Interface Module (Frontend - app.py)
   - Functionality: Provides the chat-based interface using Streamlit. It accepts user queries in natural language, sends them to the backend, and displays the chatbot's responses in real-time,.

2. Chatbot Processing Module (Backend Logic)
   - Functionality: Acts as the main controller. It processes natural language input, communicates with the LLM, and maintains the conversation flow and context across multi-turn interactions using a unique `session_id`,.

3. Intent Classification Module
   - Functionality: Analyzes the user's input using prompt engineering to categorize the request into specific domains: Order Management, Quotation Requests, Invoice Queries, or Other Support Issues,,.

4. Entity Extraction Module
   - Functionality: Parses the unstructured text to identify and extract key business data required for a ticket, such as Product details, Quantity, Order ID, and Invoice number,.

5. Conversation Management Module
   - Functionality: Handles missing data. If the Entity Extraction module is missing required fields, this function prompts the chatbot to dynamically ask follow-up questions to the user before generating a ticket,.

6. Ticket Generation Module
   - Functionality: Once all data is collected and validated, this function formats the extracted information into a structured ticket object prepared for backend submission,.

7. API Integration Module
   - Functionality: Connects the chatbot logic to the backend services. It sends the structured ticket data via REST APIs and receives confirmation responses,.

8. Database Module
   - Functionality: Connects to the SQLite database. It contains functions to save ticket details (ticket_id, intent, product, etc.), store conversation logs (query, response, timestamp), and maintain session data,,.

---------------------------------------------------------------------------
# API ENDPOINTS
---------------------------------------------------------------------------
The FastAPI backend exposes the following primary endpoints for the chatbot to function:
- POST /chat : Accepts the user's query payload (e.g., {"message": "I want to order laptops"}) and returns the AI response.
- GET /history : Retrieves the conversation log to maintain context.

===========================================================================
```