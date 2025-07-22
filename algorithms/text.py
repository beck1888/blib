"""
text.py

A collection of text processing utilities, including string similarity,
pattern matching, normalization, and more.

Functions:
    levenshtein(s1, s2): Compute the Levenshtein distance between two strings.
    kmp_search(text, pattern): Perform Knuth-Morris-Pratt pattern matching.
    is_palindrome(s): Check if a string is a palindrome.
    slugify(text): Convert text to a URL-safe slug.
    normalize(text): Normalize text by removing accents and converting to lowercase.
    text_similarity(s1, s2): Calculate normalized similarity between two strings.
"""

import unicodedata
import re
from typing import List


def levenshtein(s1: str, s2: str) -> int:
    """
    Compute the Levenshtein (edit) distance between two strings.

    Args:
        s1 (str): The first string.
        s2 (str): The second string.

    Returns:
        int: The Levenshtein distance between the two strings.
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
    Perform Knuth-Morris-Pratt (KMP) pattern matching algorithm.

    Args:
        text (str): The text to search within.
        pattern (str): The pattern to search for.

    Returns:
        List[int]: A list of starting indices where the pattern is found in the text.
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

    Args:
        s (str): The string to check.

    Returns:
        bool: True if the string is a palindrome, False otherwise.
    """
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    return cleaned == cleaned[::-1]


def slugify(text: str) -> str:
    """
    Convert text to a URL-safe slug.

    Args:
        text (str): The input text to convert.

    Returns:
        str: A URL-safe slug generated from the input text.
    """
    text = normalize(text)
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text).strip('-')
    return text


def normalize(text: str) -> str:
    """
    Normalize text by removing accents, converting to lowercase, and stripping whitespace.

    Args:
        text (str): The input text to normalize.

    Returns:
        str: The normalized text.
    """
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    return text.lower().strip()


def text_similarity(s1: str, s2: str) -> float:
    """
    Calculate normalized similarity between two strings using Levenshtein distance.

    Args:
        s1 (str): The first string.
        s2 (str): The second string.

    Returns:
        float: A value between 0 (no similarity) and 1 (identical), representing the similarity.
    """
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0
    distance = levenshtein(s1, s2)
    return 1 - distance / max_len