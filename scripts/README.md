# Scripts Directory

Utility scripts for ETL, embedding generation, and data processing.

## Available Scripts

### build_embeddings.py

Builds vector embeddings from documents in the `data/` directory.

**Usage:**

```bash
cd scripts
python build_embeddings.py
```

**Prerequisites:**
- Backend Python environment activated
- `GOOGLE_API_KEY` set in `backend/.env`
- Documents placed in `data/` directory

**What it does:**
1. Loads all documents from `data/` directory
2. Splits documents into chunks (1000 tokens with 200 token overlap)
3. Generates embeddings using Google Gemini
4. Creates FAISS vector store
5. Saves vector store to configured path
6. Tests retrieval with sample query

**Output:**
- Vector store saved to `data/vector_store/` (or configured path)
- Includes index file and metadata

**Supported file types:**
- `.txt` - Plain text files
- `.md` - Markdown files
- `.pdf` - PDF documents
- `.csv` - CSV files
- `.docx` - Word documents

## Running Scripts

### From scripts directory:

```bash
cd /path/to/smart-doc-retriever2/scripts
source ../backend/venv/bin/activate  # Activate backend environment
python build_embeddings.py
```

### From project root:

```bash
cd /path/to/smart-doc-retriever2
source backend/venv/bin/activate
python scripts/build_embeddings.py
```

## Adding New Scripts

When adding new scripts:

1. Add shebang: `#!/usr/bin/env python`
2. Make executable: `chmod +x script_name.py`
3. Add to this README
4. Include logging
5. Add error handling

## Environment Requirements

Scripts use the backend environment. Ensure you have:
- Activated virtual environment
- Installed requirements from `backend/requirements.txt`
- Configured environment variables in `backend/.env`
