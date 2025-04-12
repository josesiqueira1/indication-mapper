# DailyMed Mapper

A microservices-based application for extracting drug indications from DailyMed and mapping them to ICD-10 codes using OpenAI's LLM.

Built with:

- Python (LLM integration, scraping, ICD-10 mapping)
- NestJS (API, auth, users, drug management)
- MongoDB (data storage)
- Redis (LLM response caching)
- gRPC (inter-service communication)

---

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
- An OpenAI API key

---

### Setup

1. **Set your OpenAI API key**

Create a `.env` file from `.env.example` or define the environment variable directly in the `docker-compose.yml`.

> Inside `docker-compose.yml`:

```yaml
environment:
  OPENAI_API_KEY=your-openai-api-key-here
```

2. **Run the project**

```bash
docker compose up -d --build
```

This will:

- Build both the **Python** and **Node.js** services
- Start MongoDB and Redis containers
- Set up gRPC communication between services
- Expose the API on `http://localhost:3000`

---

## API Overview

After the app is running, you can access the Swagger docs at:

```
http://localhost:3000/api
```

There you'll find routes for:

- Auth (register/login)
- Drugs (list supported drugs)
- Mappings (fetch, create, update, delete)
- Triggering a new mapping via the Python service

---

## Architecture

- **Python Service**: Handles DailyMed scraping and ICD-10 mapping using OpenAI
- **NestJS API**: Handles user auth, drug/mapping management, and exposes REST endpoints
- **MongoDB**: Stores users, drugs, and mappings
- **Redis**: Caches LLM responses
- **gRPC**: Connects Node.js to Python for mapping logic
