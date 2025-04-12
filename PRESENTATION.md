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

   - Uses MongoDB for storing users, medications, and mappings

This setup ensures separation of concerns, clean layering, and scalability, while also allowing LLM logic to evolve independently from the API layer.

## Fetcher

I tried to use the XML version of the label info, but as the request return a `.zip` I decided to move to scrapping from the HTML

## Mapper

At first I tried using a propmt to specify de data structure, but after some tries I decided to move to using the [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses), so I had to adjust the tests to further modify the implementation

## gRPC Server

I've decided to use gRPC to establish a high-performance, language-agnostic communication channel between the Node.js backend and the Python service. This approach offers several advantages:

- Type safety through `.proto` files, which define the request/response structure and prevent common serialization issues
- Low latency communication, making it ideal for inter-service calls where speed is critical
- Scalability and easy integration with additional services in the future, should the architecture grow

The Python service exposes the mapping functionality via a simple gRPC interface. The Node.js backend uses the generated client stub to call this service whenever a mapping request is needed. This keeps the API layer focused on user interaction and access control, while delegating all LLM-heavy processing to the Python layer.

## Redis Caching

To avoid redundant API calls to OpenAI and speed up repeated queries, I've integrated Redis caching at the Python layer. Each combination of drug label and request is hashed and stored as a key, ensuring that identical requests reuse previously computed results. This not only reduces response time but also helps stay within usage limits of the LLM API.

## NestJS API

I chose NestJS for the backend because it provides a well-structured, opinionated framework that scales well as the application grows. From the beginning, I aimed to clearly separate concerns (users, drugs, mappings, etc.), and Nest’s modular architecture, built-in dependency injection, and native support for middlewares, interceptors, and guards made that straightforward.

NestJS also has excellent built-in support for inter-service communication, including gRPC, which made integration with the Python mapping service clean and minimal in terms of boilerplate.
