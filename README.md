# Codkus: AI-Assisted Python Code Generator

Codkus is a web application that utilizes AI to generate high-quality Python code based on user-provided tasks. It leverages the power of the GROQ API and Streamlit to create an interactive and user-friendly code generation experience.

## Features

- Generate Python code based on user-defined tasks
- Clean and optimize generated code
- Automatically generate test cases for the generated code
- Run and execute the generated code and test cases
- Fix code based on user-provided error messages
- Download the generated code and test cases

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/micic-mihajlo/codkus.git
   ```

2. Navigate to the project directory:

   ```bash
   cd codkus
   ```

3. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   - For Windows:
     ```bash
     venv\Scripts\activate
     ```
   - For macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

5. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Set up the GROQ API key:

   - Create a file named `.streamlit/secrets.toml` in the project directory.
   - Open the `secrets.toml` file and add your GROQ API key:
     ```toml
     GROQ_API_KEY = "your_api_key_here"
     ```
   - Replace `"your_api_key_here"` with your actual GROQ API key.
  
7. Alternatively, check out Codkus in action on [https://codkus.streamlit.app/](https://codkus.streamlit.app/)

## Usage

1. Run the Streamlit app:

   ```bash
   streamlit run codkoni.py
   ```

2. Open your web browser and navigate to the provided URL (e.g., `http://localhost:8501`).

3. Enter a task description in the "Enter the task" text area.

4. Click the "Generate Code" button to generate Python code based on the provided task.

5. Review the generated code and test cases.

6. Click the "Run Code and Tests" button to execute the generated code and test cases.

7. If there are any errors, copy the error message and paste it into the "Error Message" text area.

8. Click the "Fix Code" button to fix the code based on the provided error message.

9. Once the code is satisfactory, click the "Confirm Code" button.

10. Download the fixed code or the full code (including test cases) using the respective download buttons.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [GROQ API](https://groq.com/) for providing the AI capabilities
- [Streamlit](https://streamlit.io/) for the web application framework
- [Langchain](https://langchain.com/) for the language model integration

## Contact

For any inquiries or questions, please contact [m2micic@uwaterloo.ca](mailto:m2micic@uwaterloo.ca).
