"""
arrays.py

A collection of array and sequence-related algorithms for common use cases,
including prefix sums, search, transformation, and classic problem-solving utilities.
"""
from bisect import bisect_left
from typing import List, Any

def running_sum(array: List[int]) -> List[int]:
    """Returns the running sum of the input array."""
    result = []
    total = 0
    for num in array:
        total += num
        result.append(total)
    return result

def prefix_sum(array: List[int]) -> List[int]:
    """Returns a prefix sum array where each element at index i is the sum of array[:i]."""
    result = [0]
    for num in array:
        result.append(result[-1] + num)
    return result

def binary_search(arr: List[int], target: int) -> int:
    """Performs binary search on a sorted array. Returns index or -1 if not found."""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def rotate_array(arr: List[Any], k: int) -> List[Any]:
    """Rotates the array k steps to the right (negative k for left)."""
    n = len(arr)
    if n == 0:
        return []
    k %= n
    return arr[-k:] + arr[:-k]

def longest_increasing_subsequence(arr: List[int]) -> List[int]:
    """Returns the longest increasing subsequence using patience sorting + backtracking."""
    if not arr:
        return []
    piles = []
    predecessors = [-1] * len(arr)
    pile_tops = []

    for i, num in enumerate(arr):
        pos = bisect_left(pile_tops, num)
        if pos == len(pile_tops):
            pile_tops.append(num)
            piles.append([i])
        else:
            pile_tops[pos] = num
            piles[pos].append(i)
        if pos > 0:
            predecessors[i] = piles[pos - 1][-1]

    # Reconstruct LIS from last pile
    lis = []
    k = piles[-1][-1]
    while k != -1:
        lis.append(arr[k])
        k = predecessors[k]
    return lis[::-1]

def two_sum(arr: List[int], target: int) -> List[int] | None:
    """Returns indices of two numbers that add up to target, or None if not found."""
    seen = {}
    for i, num in enumerate(arr):
        diff = target - num
        if diff in seen:
            return [seen[diff], i]
        seen[num] = i
    return None

def flatten(nested_list: List[Any]) -> List[Any]:
    """Recursively flattens any depth of nested lists."""
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result