## Getting Started

### Clone the Repository
```bash
git clone https://github.com/sivasankakaniganti/assignment-1-MLAI.git
cd assignment-1-MLAI
```

### Set Up Environment Variables
Create a `.env` file inside the `src` folder and add your Groq API keys:
```env
GROQ_API_KEY=your_groq_api_key
```

### Run the Application with Docker Compose
```bash
docker compose up
```

### Access the Application
Once the containers are up, you can access the Chainlit chat interface at:
[http://localhost:8000](http://localhost:8000)

## Demo
You can watch a demo video of the application in action below:

<video width="600" controls>
  <source src="video/demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

If the video does not load, you can watch it [here](video/demo.mp4).

## Limitations
- Each question is processed independently, meaning there is **no memory functionality** at the moment.
- The system may take some time for web searches if the information is not present in the uploaded PDFs.
- The chatbot relies on API-based retrievals, which can be affected by network latency or API limits.

