# dReveal Chatbot with Artificial Intelligence

- **Backend**: Manages the database with the official documentation from the dReveal site and performs natural language queries on the preloaded database.  
  - **Technologies**:
    - Chromadb (0.5.20)
    - Flask (3.1.0)
    - Langchain (0.2.17)
    - Langchain-community (0.2.6)
    - Python (3.12.4)

  - **Installation**: For running the backend project, follow these steps:
    1. Download project
    2. Install Python version 3.12.4
    3. In project folder, run "pip install -r requirements.txt"
    4. To run the project, "python ./app.py"

- **Frontend**: User interface component to interact with the dReveal chatbot.
  - **Technologies**:
    - Node.js (v20.14.0)
    - Vue.js (@vue/cli 5.0.8)

  - **Installation**: For running the frontend project, follow these steps:
    1. Download project
    2. Install Node version 20.14
    3. Install Vue Cli version 5.0.8
    4. In project folder, run "npm install"
    5. To run the project, "npm run serve"

- **Dataset**: A set of PDF files obtained from the Learn dReveal site. These files are the official documentation available at [learn.dreveal.com](https://learn.dreveal.com/).

    This dataset is used for the creation of the database used by the chatbot

