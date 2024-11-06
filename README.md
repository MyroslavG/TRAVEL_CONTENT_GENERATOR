# GPT-3 Paraphrasing API for SEO Content

This project built in 2020 is an API service that uses OpenAI's GPT-3 to paraphrase Wikipedia articles for generating unique, SEO-friendly content. Designed for content creators and SEO professionals, this API takes a topic, retrieves the corresponding Wikipedia article, and returns a JSON response with the paraphrased text.

## Features

- **Wikipedia Content Retrieval**: Fetches summaries of articles directly from Wikipedia.
- **AI-Driven Paraphrasing**: Utilizes GPT-3 to rewrite content with preserved meaning and improved uniqueness.
- **Uniqueness Validation**: Ensures rephrased text is unique enough by calculating the cosine similarity to the original article.
- **Logging**: Tracks similarity scores, rephrased content, and failed attempts for quality assurance.

## Requirements

- Python 3.7+
- OpenAI API key
- Required packages (install via `pip`):
  ```bash
  pip install flask openai wikipedia scikit-learn pandas
  ```

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/gpt3-paraphrasing-api.git
    cd gpt3-paraphrasing-api
    ```
2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Add your OpenAI API key by updating the `openai.api_key` in `app.py`.

## Usage

1. **Run the API**:
   ```bash
   python app.py
   ```

2. **API Endpoint**:
   - **Endpoint**: `/generate`
   - **Method**: `POST`
   - **Parameters**:
     - `input`: The topic of the article (e.g., "Hobart").
     - `length`: Desired output length (integer).
     - `temperature`: Controls creativity in text generation (0-1 range).
   - **Example Request**:
     ```bash
     curl -X POST http://127.0.0.1:5000/generate -d "input=Hobart&length=200&temperature=0.7"
     ```

## Code Structure

- **`app.py`**: Main Flask app that defines routes and API functionality.
- **Similarity Function**: Calculates cosine similarity between original and paraphrased text to assess uniqueness.
- **Logging**: Logs generated paraphrased content along with similarity scores.

## How It Works

1. **Article Retrieval**: Retrieves a summary of the specified Wikipedia article.
2. **Paraphrasing with GPT-3**: GPT-3 generates a unique version of the summary, controlled by pre-defined prompts and example inputs.
3. **Uniqueness Check**: If similarity to the original is above a set threshold, the service re-generates the paraphrase until a unique version is achieved.
4. **Response**: Returns the final paraphrased text as JSON.
