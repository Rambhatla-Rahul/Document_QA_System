import re
from typing import List


class TextNormalizer:
    def __init__(self):
        # Common OCR junk patterns
        self.multiple_spaces = re.compile(r"\s{2,}")
        self.page_numbers = re.compile(r"^\s*\d+\s*$")
        self.header_footer_noise = re.compile(
            r"(copyright|all rights reserved|page \d+)",
            re.IGNORECASE
        )
        self.hyphen_break = re.compile(r"(\w+)-\n(\w+)")

    def normalize_pages(self, pages: List[str]) -> List[str]:
        cleaned_pages = []

        for page in pages:
            text = page.strip()

            if not text:
                continue

            # Remove obvious page numbers
            if self.page_numbers.match(text):
                continue

            # Fix hyphenated line breaks
            text = self.hyphen_break.sub(r"\1\2", text)

            # Merge broken lines (OCR & PDF)
            text = text.replace("\n", " ")

            # Remove header/footer noise
            text = self.header_footer_noise.sub("", text)

            # Normalize whitespace
            text = self.multiple_spaces.sub(" ", text)

            cleaned_pages.append(text.strip())

        return cleaned_pages