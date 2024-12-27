# AI-MPC

This project provides a practical demonstration of Retrieval-Augmented Generation (RAG)
from the MPC report in Nov 2024. The app responds as an MPC member to various questions.

With thanks to https://github.com/ShahMitul-GenAI/RAG-Simplified for the basis of this repo.

### Features

## Setup

### Installation
1. Clone the repository to your local machine.


2. Navigate to the project directory:
```bash
cd simplified_rag
```

3. Install Poetry using pip (if not already installed):
```bash
pip install poetry
```

4. Activate the virtual environment created by Poetry:
```bash
poetry shell
```

5. Install project dependencies using Poetry:
```bash
poetry install
```

6. Create a `.env` file and add your own OpenAI API key in the `.env` file as follows:
```
OPENAI_API_KEY=your-key-here
```

### Running the Application
1. After installing the dependencies, you can run the Streamlit app by executing the following command:
```bash
streamlit run app.py
```

2. Once the server starts, open a web browser and follow the link displayed by Streamlit to access the application.

### Usage
1. Upon launching the application, Select the MPC report and upload the pdf file.

2. Choose the desired source, and the app will retrieve relevant information based on your selection.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
