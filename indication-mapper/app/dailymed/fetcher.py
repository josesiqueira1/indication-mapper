import requests
from bs4 import BeautifulSoup


def fetch_indications_section(setid: str) -> str:
    """
    Fetches the Indications and Usage section from DailyMed based on the drug setid.
    Raises:
        ValueError: If the indications section is not found.
    Returns:
        str: Extracted indication text.
    """
    url = f"https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid={setid}"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    root_section = soup.find("div", {"data-sectioncode": "34067-9"})
    if not root_section:
        raise ValueError("Indications section not found")

    all_paragraphs = root_section.find_all("p")
    text = "\n".join(
        p.get_text(strip=True) for p in all_paragraphs if p.get_text(strip=True)
    )

    if not text:
        raise ValueError("No indication text found inside the section")

    return text
