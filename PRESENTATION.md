# Dailymed Mapper

## Overall Architecture

To tackle the challenge of extracting and structuring drug indications, I opted to split into two main components:

1. A Python service responsible for:

   - Fetching and parsing drug label information from DailyMed

   - Extracting relevant indications

   - Using an LLM (OpenAI API) to semantically map those indications to ICD-10 codes

   - Structuring the output with Pydantic

   - Caching responses in Redis for performance and API cost efficiency

2. A Node.js (NestJS) backend that:

   - Exposes a fully functional API with authentication, CRUD, and validation

   - Delegates indication mapping logic to the Python service via gRPC

   - Uses MongoDB for storing users, drugs, and mappings

This setup ensures separation of concerns, clean layering, and scalability, while also allowing LLM logic to evolve independently from the API layer.

## Fetcher

I tried to use the XML version of the label info, but as the request return a `.zip` I decided to move to scrapping from the HTML

## Mapper

At first I tried using a propmt to specify de data structure, but after some tries I decided to move to using the [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses), so I had to adjust the tests to further modify the implementation
