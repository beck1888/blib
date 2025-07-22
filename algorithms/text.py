import unicodedata
import re
from typing import List


def levenshtein(s1: str, s2: str) -> int:
    """
    Compute the Levenshtein (edit) distance between two strings.
    """
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def kmp_search(text: str, pattern: str) -> List[int]:
    """
    Knuth-Morris-Pratt (KMP) pattern matching algorithm.
    Returns list of starting indices where pattern is found in text.
    """
    def build_lps(pat):
        lps = [0] * len(pat)
        length = 0
        i = 1
        while i < len(pat):
            if pat[i] == pat[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    result = []
    lps = build_lps(pattern)
    i = j = 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == len(pattern):
            result.append(i - j)
            j = lps[j - 1]
        elif i < len(text) and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return result


def is_palindrome(s: str) -> bool:
    """
    Check if a string is a palindrome (ignoring case and non-alphanumerics).
    """
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    return cleaned == cleaned[::-1]


def slugify(text: str) -> str:
    """
    Convert text to a URL-safe slug.
    """
    text = normalize(text)
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text).strip('-')
    return text


def normalize(text: str) -> str:
    """
    Normalize text: lowercase, strip, remove accents.
    """
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    return text.lower().strip()


def text_similarity(s1: str, s2: str) -> float:
    """
    Calculate normalized similarity between two strings using Levenshtein distance.
    Returns a float between 0 (no similarity) and 1 (identical).
    """
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0
    distance = levenshtein(s1, s2)
    return 1 - distance / max_len