"""
arrays.py

A collection of array and sequence-related algorithms for common use cases,
including prefix sums, search, transformation, and classic problem-solving utilities.

Functions:
    running_sum(array): Computes the running sum of an array.
    prefix_sum(array): Computes the prefix sum of an array.
    binary_search(arr, target): Performs binary search on a sorted array.
    rotate_array(arr, k): Rotates an array by k steps.
    longest_increasing_subsequence(arr): Finds the longest increasing subsequence.
    two_sum(arr, target): Finds two indices whose values sum to a target.
    flatten(nested_list): Flattens a nested list into a single list.
"""

from bisect import bisect_left
from typing import List, Any

def running_sum(array: List[int]) -> List[int]:
    """
    Computes the running sum of the input array.

    Args:
        array (List[int]): The input array of integers.

    Returns:
        List[int]: A list where each element is the cumulative sum up to that index.
    """
    result = []
    total = 0
    for num in array:
        total += num
        result.append(total)
    return result

def prefix_sum(array: List[int]) -> List[int]:
    """
    Computes a prefix sum array where each element at index i is the sum of array[:i].

    Args:
        array (List[int]): The input array of integers.

    Returns:
        List[int]: A list where each element is the prefix sum up to that index.
    """
    result = [0]
    for num in array:
        result.append(result[-1] + num)
    return result

def binary_search(arr: List[int], target: int) -> int:
    """
    Performs binary search on a sorted array.

    Args:
        arr (List[int]): The sorted array to search.
        target (int): The value to search for.

    Returns:
        int: The index of the target if found, or -1 if not found.
    """
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
    """
    Rotates the array k steps to the right. Negative k rotates to the left.

    Args:
        arr (List[Any]): The input array to rotate.
        k (int): The number of steps to rotate.

    Returns:
        List[Any]: The rotated array.
    """
    n = len(arr)
    if n == 0:
        return []
    k %= n
    return arr[-k:] + arr[:-k]

def longest_increasing_subsequence(arr: List[int]) -> List[int]:
    """
    Finds the longest increasing subsequence in the array.

    Args:
        arr (List[int]): The input array of integers.

    Returns:
        List[int]: The longest increasing subsequence as a list of integers.
    """
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
    """
    Finds two indices of numbers in the array that add up to the target.

    Args:
        arr (List[int]): The input array of integers.
        target (int): The target sum.

    Returns:
        List[int] | None: A list of two indices if a pair is found, or None otherwise.
    """
    seen = {}
    for i, num in enumerate(arr):
        diff = target - num
        if diff in seen:
            return [seen[diff], i]
        seen[num] = i
    return None

def flatten(nested_list: List[Any]) -> List[Any]:
    """
    Recursively flattens a nested list into a single list.

    Args:
        nested_list (List[Any]): The nested list to flatten.

    Returns:
        List[Any]: A flattened list containing all elements from the nested list.
    """
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result