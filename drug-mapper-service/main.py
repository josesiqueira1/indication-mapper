import app.dailymed.fetcher
import app.llm.mapper
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    indication = app.dailymed.fetcher.fetch_indications_section(
        "595f437d-2729-40bb-9c62-c8ece1f82780"
    )

    maps = app.llm.mapper.map_indications_to_icd10(
        "Dupixent", "595f437d-2729-40bb-9c62-c8ece1f82780", indication
    )

    print("Mapping Results:")
    for icd10_code, description in maps.icd10_mappings:
        print(f"{icd10_code[1]}: {description[1]}")
