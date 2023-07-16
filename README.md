# Chat with your documents (using ChatGPT and OpenSource LLMs)

## ℹ️ About
This project aims to create chatbots that are able to answer user questions using context provided from internal documents, meaning that it is possible to give knowledge to the chatbots using large corpus of data that the chatbot wasn't originally trained on. This project aims to give a choice about whether the user would like to leverage ChatGPT or use an OpenSource LLM to answer the questions.

The objective is to provide these AI models with access to a rich database of internal documents and allow them to retrieve the most relevant pieces of text in response to user queries.

The system leverages advanced text retrieval and information ranking mechanisms to sift through a vast array of internal documents. Using the provided context, the system discerns user intent and identifies the most pertinent documents. These documents are then processed, extracting the most appropriate segments that can provide the user with the most accurate and comprehensive answer.

Both choices have their own pros and cons that the user has to take into consideration before making their decision.

## 🛠 Features

- **Model Choice Flexibility**: Choose between ChatGPT or a local language model based on your preferences and needs.
- **Document Understanding**: Our system is designed to analyze your internal documents and extract the most relevant pieces of information in response to user queries.
- **Cosine Similarity Search**: By comparing the cosine similarity between a user query and the text in the document, it retrieves the most relevant information to provide accurate and precise responses.
- **Model Quantization**: The local language model uses quantization, a technique that reduces the VRAM consumed and speeds up inference considerably. This feature converts the transformer model weights from 16bit to 4bit, enabling efficient utilization of your hardware resources.

## 🧠 Potential Use-Cases

This project could be used in various scenarios, such as:

- A helpdesk chatbot that pulls answers from internal FAQ documents or knowledge bases.
- An intelligent assistant for professionals (like lawyers, doctors, researchers) that can retrieve information from a large corpus of documents.
- A tool for content creators, writers, and journalists who need to pull information from their own database of articles, notes, or references.

Our goal with this project is to leverage the power of language models and document understanding to make data retrieval and comprehension more accessible, efficient, and beneficial for everyone. This project could greatly assist in various professional and creative fields.


## 📁 Data Structure
- `data/`: This directory contains all the data that is needed for the models to perform knowledge extraction.
    - `urls.txt`: This file contains URLs for the chatbot to refer to when posed with a question.
    - `pdf_files/`: This directory contains internal documents in PDF format that the models can reference.
    - `text_files/`: This directory contains internal documents in plain text format that the models can reference.

## 💻 Tech Stack

- `LangChain`: For developing applications powered by language models.
- `ChromaDB`: For storing and searching embeddings and their metadata.
- `Django`: As the primary backend framework.
- `Docker`: For containerization of the application.
- `Nginx`: For serving the application.
- `Pytorch`: As the core machine learning library.
- `HuggingFace`: For leveraging pre-trained models.
- `InstructorEmbedding`: To generate text embeddings tailored to any task and domain.


## ☘️ How to Use

1. **Add Documents**: Add your PDFs to the `data/pdf_files` directory and your text files to the `data/text_files` directory. Also, if there any urls, please add them to `urls.txt` (one url per line).

2. **Create .env file**: Create a `.env` file in the root of the project directory and add the following environment variables:

    ```shell
    OPENAI_API_KEY=your_openai_api_key
    CHROMA_SERVER_HOST=your_chroma_db_server_ip
    ```

    Replace `your_openai_api_key` with your actual OpenAI API key and `your_chroma_db_server_ip` with the public IP address of where the Chroma DB server is deployed.

3. **Build the Docker Image**: Run the following command in your terminal to build the Docker image:

    ```shell
    docker build -t chatbot_image .
    ```

4. **Run the Docker Image**: Finally, launch the Docker image using the following command:

    ```shell
    docker run -d -p 5000:5000 chatbot_image
    ```

    Now your application is running on `localhost:5000`.


## 🚀 API Usage

This project offers two API endpoints that you can use to interface with the chatbot:

1. **ChatGPT Endpoint**: Send a POST request to `/bot/openai/` to interact with the ChatGPT model.
2. **HuggingFace Endpoint**: Send a POST request to `/bot/hf/` to interact with the local language model.

Both endpoints accept POST requests with the following JSON body:

```json
{
  "message": "your_query_here"
}

```
Replace `"your_query_here"` with your actual query.

### Example

Here's how to send a POST request to the ChatGPT endpoint using curl:

```shell
curl -X POST -H "Content-Type: application/json" -d '{"message":"what is langchain?"}' http://localhost:5000/bot/openai/
```

Similarly, you can interact with the local language model through the HuggingFace endpoint:

```shell
curl -X POST -H "Content-Type: application/json" -d '{"message":"what is langchain?"}' http://localhost:5000/bot/hf/
```





 ## 🛠 Comparison between ChatGPT and local LLM
 |                                 | Cloud-Based (ChatGPT)                               | Local Large Language Model                  |
|---------------------------------|-----------------------------------------------------|--------------------------------------------|
| Features                        | - Multilingual capabilities                          | - Depends on the specific model              |
|                                 | - Services may include usage analytics                    | - Potentially modifiable                     |
|                                 | - Customizable outputs                               | - Can be fine-tuned on specific tasks/data (if resources and expertise are available) |
|                                 | - Can handle a wide range of tasks                   | - Capacity to integrate with local systems    |
|                                 | - Regular updates for improved performance          | - May offer better data privacy compliance    |
|                                 | - APIs available for integration with various platforms | - Option to run offline                   |
|                                 |               | - Ability to manage compute resource allocation |
| Pros                            | - Easy to use and manage                             | - High data privacy and security, as data never leaves local servers   |
|                                 | - Always up-to-date with latest improvements         | - Full control over the model and data      |
|                                 | - Scalable and flexible based on needs               | - No dependency on internet connectivity    |
|                                 | - Less computational power required on user end      | - Predictable costs - no additional cost for increased usage |
|                                 | - Provides regular maintenance and support           | - Customizability (including possibility of unique fine-tuning) |
|                                 | - Can be accessed from anywhere                      | - No risks associated with vendor lock-in   |
| Cons                            | - Requires a reliable internet connection            | - High computational resource requirements |
|                                 | - Potentially higher cost for high usage             | - Needs regular manual updates for model improvements |
|                                 | - Data privacy concerns due to data transfer over internet  | - More complex to set up, maintain, and manage |
|                                 | - Dependent on provider for updates and improvements |- Lack of support unless you have a dedicated team                 |
|                                 | - Potential latency issues                           | - Limited by local resources (hardware, power etc.) |
|                                 | - Vendor lock-in risks                               |  |



