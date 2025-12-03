# MongoDB RAG Agent - Intelligent Knowledge Base Search

Agentic RAG system combining MongoDB Atlas Vector Search with Pydantic AI for intelligent document retrieval.

## Features

- **Hybrid Search**: Combines semantic vector search with full-text keyword search using MongoDB's `$rankFusion`
- **Multi-Format Ingestion**: PDF, Word, PowerPoint, Excel, HTML, Markdown, Audio transcription
- **Intelligent Chunking**: Docling HybridChunker preserves document structure and semantic boundaries
- **Conversational CLI**: Rich-based interface with real-time streaming and tool call visibility
- **Multiple LLM Support**: OpenAI, OpenRouter, Ollama, Gemini

## Prerequisites

- Python 3.10+
- MongoDB Atlas account (free tier available)
- LLM provider API key (OpenAI, OpenRouter, etc.)
- Embedding provider API key (OpenAI recommended)
- UV package manager

## Quick Start

### 1. Install UV Package Manager

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone and Setup Project

```bash
git clone <repository-url>
cd MongoDB-RAG-Agent

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # Unix/Mac
.venv\Scripts\activate     # Windows
uv sync
```

### 3. Set Up MongoDB Atlas

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register) and create a free account
2. Click **"Create"** → Choose **M0 Free** tier → Select region → Click **"Create Deployment"**
3. **Quickstart Wizard** appears - configure security:
   - **Database User**: Create username and password (save these!)
   - **Network Access**: Click "Add My Current IP Address"
4. Click **"Connect"** → **"Drivers"** → Copy your connection string
   - Format: `mongodb+srv://username:<password>@cluster.mongodb.net/?appName=YourApp`
   - Replace `<password>` with your actual password

**Note**: Database (`rag_db`) and collections (`documents`, `chunks`) will be created automatically when you run ingestion in step 6.

### 4. Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` with your credentials:
- **MONGODB_URI**: Connection string from step 3
- **LLM_API_KEY**: Your LLM provider API key (OpenRouter, OpenAI, etc.)
- **EMBEDDING_API_KEY**: Your OpenAI API key for embeddings

### 5. Validate Configuration

```bash
uv run python -m src.test_config
```

You should see: `[OK] ALL CONFIGURATION CHECKS PASSED`

---

## Complete Setup (After Phase 4 - Ingestion)

Once the ingestion pipeline is built (Phase 4), complete these additional steps:

### 6. Run Ingestion Pipeline

```bash
# Add your documents to the documents/ folder
uv run python -m src.ingestion.ingest -d ./documents
```

This will:
- Process your documents (PDF, Word, PowerPoint, Excel, Markdown, etc.)
- Chunk them intelligently
- Generate embeddings
- Store everything in MongoDB (`rag_db.documents` and `rag_db.chunks`)

### 7. Create Search Indexes

**Important**: Only do this AFTER running ingestion - you need data in your `chunks` collection first.

1. In MongoDB Atlas, click **Database** → **Search & Vector Search**
2. Click **"Create Search Index"**

**Vector Search Index:**
1. Choose **"Atlas Vector Search"** → **"JSON Editor"**
2. Database: `rag_db`
3. Collection: `chunks`
4. Index name: `vector_index`
5. Paste:
```json
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 1536,
      "similarity": "cosine"
    }
  ]
}
```

**Full-Text Search Index:**
1. Click **"Create Search Index"** → **"Atlas Search"**
2. Database: `rag_db`
3. Collection: `chunks`
4. Index name: `text_index`
5. Paste:
```json
{
  "mappings": {
    "dynamic": false,
    "fields": {
      "content": {
        "type": "string",
        "analyzer": "lucene.standard"
      }
    }
  }
}
```

Wait 1-5 minutes for indexes to build (status: "Building" → "Active").

### 8. Run the Agent

```bash
uv run python -m src.cli
```

Now you can ask questions and the agent will search your knowledge base!

## Current Status

**✅ Phase 1 Complete:**
- MongoDB Atlas cluster setup
- Configuration management with `.env`
- Environment validation
- LLM & embedding provider configuration

**⏳ Phase 2 Next:**
- Document ingestion pipeline (PDF, Word, PowerPoint, Excel, Markdown, Audio)
- MongoDB connection with PyMongo async
- Data population in `rag_db.documents` and `rag_db.chunks`
- Search index creation in Atlas UI

**🚧 Coming After:**
- Phase 3: Search tools (semantic & hybrid)
- Phase 4: Agent & CLI interface
- Phase 5: Testing & documentation

## Development Roadmap

| Phase | Feature | Status |
|-------|---------|--------|
| 1 | Project scaffolding & configuration | ✅ Complete |
| 2 | Document ingestion pipeline & MongoDB connection | ⏳ Next |
| 3 | Semantic & hybrid search tools | ⏳ Planned |
| 4 | Agent & CLI interface | ⏳ Planned |
| 5 | Testing & documentation | ⏳ Planned |

**Why this order?** You need data in MongoDB before you can create search indexes or test search functionality. Phase 2 populates the database, then Phase 3 can search against real data.

## Project Structure

```
MongoDB-RAG-Agent/
├── src/                    # MongoDB implementation
│   ├── settings.py        # Configuration management
│   ├── providers.py       # LLM/embedding providers
│   ├── test_config.py     # Configuration validation
│   └── (Phase 2+)         # dependencies.py, tools.py, agent.py, cli.py
├── examples/              # PostgreSQL reference (DO NOT MODIFY)
├── documents/             # Document folder for ingestion
├── .claude/               # Project documentation (for AI assistants)
└── pyproject.toml        # UV package configuration
```

## Technology Stack

- **Database**: MongoDB Atlas (Vector Search + Full-Text Search)
- **Agent Framework**: Pydantic AI 0.1.0+
- **Document Processing**: Docling 2.14+ (PDF, Word, PowerPoint, Excel, Audio)
- **Async Driver**: PyMongo 4.10+ with native async API
- **CLI**: Rich 13.9+ (terminal formatting and streaming)
- **Package Manager**: UV 0.5.0+ (fast dependency management)

## Troubleshooting

### Connection Issues

If you get connection errors:
1. Check your IP address is whitelisted in MongoDB Atlas Network Access
2. Verify your username and password in the connection string
3. Make sure you replaced `<password>` with your actual password

### Search Index Issues

If searches fail:
1. Verify both indexes are created in Atlas (check **Database** → **Search & Vector Search**)
2. Ensure index names match your `.env` file (`vector_index` and `text_index`)
3. Confirm indexes show "Active" status (not "Building")
4. Remember: You must run ingestion BEFORE creating indexes

### Configuration Validation Fails

Run `uv run python -m src.test_config` to see specific error messages about missing environment variables.

## Additional Resources

- [MongoDB Atlas Documentation](https://www.mongodb.com/docs/atlas/)
- [MongoDB Vector Search Quick Start](https://www.mongodb.com/docs/atlas/atlas-vector-search/tutorials/vector-search-quick-start/)
- [Pydantic AI Documentation](https://ai.pydantic.dev/)
- [UV Package Manager](https://docs.astral.sh/uv/)

## License

[Add your license here]
