from openai import OpenAI
from app.models.indication import DrugIndication

PROMPT = """
## Function

You are a specialized medical text mapping system that converts medication indications extracted from DailyMed to precise ICD-10 codes. Your function is to analyze the provided indication information and identify the exact corresponding ICD-10 code, without creating or inventing codes.

## General Instructions

1. Carefully analyze the medication indication text
2. Identify the medical condition(s) mentioned
3. Map each condition to the most specific corresponding ICD-10 code
4. Do not invent or modify ICD-10 codes
"""


def get_openai_client():
    """Get OpenAI client instance."""
    return OpenAI()


def map_indications_to_icd10(set_id: str, text: str) -> DrugIndication:
    """
    Maps drug indications to ICD-10 codes using OpenAI's LLM.

    Args:
        set_id: DailyMed set ID
        text: Text containing drug indications

    Returns:
        DrugIndication object containing the mapped data

    Raises:
        ValueError: If the LLM response is invalid
        Exception: For other errors (OpenAI, etc.)
    """
    client = get_openai_client()

    try:
        response = client.responses.create(
            model="gpt-4o-2024-08-06",
            input=[
                {"role": "system", "content": PROMPT},
                {
                    "role": "user",
                    "content": f"Set ID: {set_id}\nText: {text}",
                },
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "drug_indication",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "set_id": {"type": "string"},
                            "indications": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "icd10_mappings": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "code": {"type": "string"},
                                        "description": {"type": "string"},
                                    },
                                    "required": ["code", "description"],
                                    "additionalProperties": False,
                                },
                            },
                        },
                        "required": [
                            "set_id",
                            "indications",
                            "icd10_mappings",
                        ],
                        "additionalProperties": False,
                    },
                    "strict": True,
                }
            },
        )

        return DrugIndication.model_validate_json(response.output_text)

    except ValueError as e:
        raise ValueError(f"Invalid response format from LLM: {str(e)}")
    except Exception as e:
        raise Exception(f"Error mapping indications: {str(e)}")
