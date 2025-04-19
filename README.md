# Email Header Analyzer

A simple Flask web application to analyze email headers.


## Running Locally

Follow these steps to run the application on your local machine:

1.  **Clone the repository (if applicable) or ensure you have the project files.**

2.  **Create a virtual environment:**
    It's recommended to use a virtual environment to manage dependencies.
    ```bash
    # Navigate to the project directory
    cd projectdowload/Email_Header_Analyzer

    # Create a virtual environment (e.g., named 'venv')
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   On Windows:
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**
    Install the required Python packages using the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the Flask application:**
    ```bash
    python app.py
    ```

6.  **Access the application:**
    Open your web browser and navigate to `http://127.0.0.1:5000` (or the address provided in the console output).

7.  **Use the Analyzer:**
    Paste the full email header text into the provided text area and click "Analyze Header". The results will be displayed below the form.
