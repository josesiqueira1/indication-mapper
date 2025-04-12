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

## Fetcher(Python)

I tried to use the XML version of the label info, but as the request return a `.zip` I decided to move to scrapping from the HTML

## Mapper(Python)

At first I tried using a propmt to specify de data structure, but after some tries I decided to move to using the [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses), so I had to adjust the tests to further modify the implementation

## gRPC Server(Python)

I've decided to use gRPC to establish a high-performance communication channel between the Node.js backend and the Python service. This approach offers several advantages:

- Type safety through `.proto` files, which define the request/response structure and prevent common serialization issues
- Low latency communication, making it ideal for inter-service calls where speed is critical
- Scalability and easy integration with additional services in the future, should the architecture grow

The Python service exposes the mapping functionality via a simple gRPC interface. The Node.js backend uses the generated client stub to call this service whenever a mapping request is needed. This keeps the API layer focused on user interaction and access control, while delegating all LLM-heavy processing to the Python layer.

## Redis Caching

To avoid redundant API calls to OpenAI and speed up repeated queries, I've integrated Redis caching at the Python layer. Each combination of drug label and request is hashed and stored as a key, ensuring that identical requests reuse previously computed results. This not only reduces response time but also helps stay within usage limits of the LLM API.

## NestJS API

I chose NestJS for the backend because it provides a well-structured framework that scales well as the application grows. From the beginning, I aimed to clearly separate concerns (users, drugs, mappings, etc.), and Nest’s modular architecture, built-in dependency injection, and native support for middlewares, interceptors, and guards made that straightforward.

NestJS also has excellent built-in support for inter-service communication, including gRPC, which made integration with the Python mapping service clean and minimal in terms of boilerplate.

Authentication is handled using JWTs, with route guards in NestJS ensuring secure access to resources.

## MongoDB Schema

MongoDB is used to persist user data, drug information, and indication-to-ICD mappings. The schema is designed to be flexible, with each drug document containing:

- Basic metadata (DailyMed ID and name)
- Mapped ICD-10 codes
- Timestamps for tracking and auditing changes

--

## User Workflow

This is the typical flow a user follows when interacting with the system:

1. **Account Creation**  
   The user registers via the authentication endpoint and receives a JWT token to authenticate future requests.

2. **Browse Available Drugs**  
   After logging in, the user can query the list of drugs currently supported by the system. These drugs are pre-fetched or manually added based on available DailyMed entries.

3. **Query ICD-10 Mappings**  
   For any drug in the list, the user can fetch its mapped indications (as ICD-10 codes) using its **DailyMed ID**.

4. **Manage Mappings**  
   The user has full control over mappings associated with their account:

   - **Create** new mappings (custom or AI-generated)
   - **Update** existing mappings
   - **Delete** mappings they no longer need

5. **Trigger New Mapping via gRPC**  
   A dedicated endpoint allows the user to trigger a fresh mapping process for a drug. This will:
   - Call the Python service via gRPC
   - The Python service scrapes the drug label from DailyMed
   - Extracts indications and maps them to ICD-10 using the LLM
   - Returns the mapped data back to the Node.js API
   - The API stores the result in MongoDB and returns it in the response

This workflow allows users to explore, customize, and generate structured drug indication data in a seamless and programmatic way.
