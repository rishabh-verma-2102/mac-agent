# 🤖 MacBook System Agent

## 🎥 Demo Video

[Demo Video](https://drive.google.com/file/d/1DBlxOM_LCYwFkO0KTe6QqKVhLSuIA60u/view?usp=drive_link)

-----

## 💻 Core Logic and Architecture

This repository contains the Python code for a helpful AI assistant designed to monitor and report the hardware status of a macOS system. It utilizes the **Ollama client** to directly interact with the **Llama 3.1 8B** model for conversational intelligence.

  * **No Agentic Framework Used:** This project does **not** rely on complex external agentic frameworks (like LangChain or LlamaIndex). The entire control flow (deciding when to call a tool, processing results, and generating the final response) is implemented directly in pure Python within the `AgentService` class.

### Agent Flow

The agent operates using a custom **ReAct (Reasoning and Acting) Loop** to process requests and maintain conversation state.

1.  **Conversation Flow:** The agent maintains a persistent **message history** (`self.messages`) throughout the conversation to remember context.
2.  **LLM Decision:** The Llama 3.1 8B model is queried to decide whether the question requires a hardware check (tool call) or a simple text response.
3.  **Tool Call Orchestration:** If the LLM requests a tool, the agent executes the corresponding `psutil` function.
4.  **Looping Logic (Multi-Step Reasoning):** A safety-capped **multi-turn tool call loop** (max **5 iterations**) is used to ensure complex queries are fully answered, even if one tool call leads to a request for another.
5.  **Final Response:** The model receives the tool data and formulates a single, natural language response.

-----

## 🛠️ Tools Used (`psutil` Implementation)

All system statistics are fetched using the high-level Python library **`psutil`**, which provides reliable, cross-platform data.

| Function Name | Description | Source Library | Returns (Data Type) |
| :--- | :--- | :--- | :--- |
| **`get_battery`** | Retrieves current charge percentage and AC power status. | `psutil.sensors_battery()` | `dict` (percent `int`, plugged `bool`) |
| **`get_cpu`** | Retrieves the current instantaneous CPU utilization. | `psutil.cpu_percent(interval=1)` | `dict` (percent `float`) |
| **`get_disk`** | Retrieves total, used, and free space for the primary disk. | `psutil.disk_usage('/')` | `dict` (GB `float`) |
| **`get_memory`** | Retrieves RAM usage statistics (Total, Available, Used). | `psutil.virtual_memory()` | `dict` (GB `float`) |

### Return Value Format Example (`get_memory`)

All memory metrics are converted to **Gigabytes (GB)** and return:

```json
{
  "memory_details": {
    "total": 16.0,
    "free": 8.2,
    "used": 7.8
  }
}
```

-----

## ⚠️ Drawbacks and Limitations

### 1\. Model Hallucination

The **Llama 3.1 8B** parameter model is susceptible to **hallucinations** (making up facts) and poor instruction following due to its size.

  * **Tool Usage Disclosure:** The model may sometimes mention using "tools" or "functions" despite the system prompt's instructions, or output empty JSON (`{}`) when confused by simple greetings.
  * **Out-of-Scope Queries:** The agent is specialized. Questions outside of MacBook hardware (like general knowledge) will be handled poorly, potentially leading to incorrect answers instead of a polite refusal.

### 2\. Tool Call Looping Limit

The agent uses a safety mechanism to prevent runaway processes: the tool execution process is capped at **5 sequential calls**.

-----

## ▶️ Getting Started (How to Run)

### 1\. Model and Dependencies

First, ensure the required dependencies are listed in `requirements.txt`.

  * **Model Installation:**

    ```bash
    ollama pull llama3.1
    ```

  * **Dependency Installation:**

    ```bash
    pip install -r requirements.txt
    ```

### 2\. Execution

Assuming your main application file is named `api.py`:

```bash
python api.py
```
