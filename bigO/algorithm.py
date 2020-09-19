from random import randrange


def bubbleSort(array):
    isSorted = False
    counter = 0

    while not isSorted:
        isSorted = True
        for i in range(len(array) - 1 - counter):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                isSorted = False

        counter += 1

    return array


def binarySearch(array, item, start, end):
    if start == end:
        if array[start] > item:
            return start
        else:
            return start + 1
    if start > end:
        return start

    mid = (start + end) // 2

    if array[mid] < item:
        return binarySearch(array, item, mid + 1, end)

    elif array[mid] > item:
        return binarySearch(array, item, start, mid - 1)
    else:
        return mid


def binaryInsertSort(array):
    for index in range(1, len(array)):
        value = array[index]
        pos = binarySearch(array, value, 0, index - 1)
        array = array[:pos] + [value] + array[pos:index] + array[index + 1 :]
    return array


def countSort(arr):  # stable
    # Time Complexity : O(n) | Space Complexity : O(n)
    minValue = min(arr)
    maxValue = max(arr) - minValue

    buckets = [0 for _ in range(maxValue + 1)]

    for i in arr:
        buckets[i - minValue] += 1

    index = 0
    for i in range(len(buckets)):
        while buckets[i] > 0:
            arr[index] = i + minValue
            index += 1
            buckets[i] -= 1

    return arr


def selectionSort(array):
    for currentIdx in range(len(array) - 1):
        smallestIdx = currentIdx
        for i in range(currentIdx + 1, len(array)):
            if array[smallestIdx] > array[i]:
                smallestIdx = i
        array[currentIdx], array[smallestIdx] = array[smallestIdx], array[currentIdx]

    return array


def introSort(array):  # in-place | not-stable
    # Time Complexity O(nlogn) | Space Complexity O(logn)
    maxDepth = 2 * (len(array).bit_length() - 1)
    sizeThreshold = 16
    return introSortHelper(array, 0, len(array), sizeThreshold, maxDepth)


def introSortHelper(array, start, end, sizeThreshold, depthLimit):
    def medianOf3(array, lowIdx, midIdx, highIdx):
        if (array[lowIdx] - array[midIdx]) * (array[highIdx] - array[lowIdx]) >= 0:
            return array[lowIdx]

        elif (array[midIdx] - array[lowIdx]) * (array[highIdx] - array[midIdx]) >= 0:
            return array[midIdx]

        else:
            return array[highIdx]

    def getPartition(array, low, high, pivot):
        i = low
        j = high
        while True:

            while array[i] < pivot:
                i += 1
            j -= 1
            while pivot < array[j]:
                j -= 1
            if i >= j:
                return i
            array[i], array[j] = array[j], array[i]
            i += 1

    while end - start > sizeThreshold:
        if depthLimit == 0:
            return heapSort(array)
        depthLimit -= 1

        median = medianOf3(array, start, start + ((end - start) // 2) + 1, end - 1)
        p = getPartition(array, start, end, median)
        introSortHelper(array, p, end, sizeThreshold, depthLimit)
        end = p

    return insertSort(array, start, end)


def insertSort(array, begin=0, end=None):  # in-place | stable
    """
    Best O(n) Time | O(1) Space
    Average O(n^2) Time | O(1) Space
    Worst (On^2) Time | O(1) Space
    """
    if end == None:
        end = len(array)

    for i in range(begin, end):
        j = i
        while j > begin and array[j - 1] > array[j]:
            array[j], array[j - 1] = array[j - 1], array[j]
            j -= 1

    return array


def insertSortOptimized(array):
    for i in range(1, len(array)):
        if array[i] >= array[i - 1]:
            continue
        for j in range(i):
            if array[i] < array[j]:
                array[j], array[j + 1 : i + 1] = array[i], array[j:i]
                break

    return array


def heapSort(arr):  # in-place | not-stable
    # Time Complexity O(nlogn) | Space Complexity O(1)

    def heapify(arr, n, i):  # Max Heap
        largest = i  # 트리에서 가장 큰 값 찾기
        l = 2 * i + 1  # Left Node
        r = 2 * i + 2  # Right Node

        if l < n and arr[i] < arr[l]:
            largest = l

        if r < n and arr[largest] < arr[r]:
            largest = r

        # root가 최대가 아니면
        # 최대 값과 바꾸고, 계속 heapify
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    n = len(arr)

    for i in range(n // 2, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        # Heapify root element
        heapify(arr, i, 0)

    return arr


def timSort(arr):  # in-place | stable
    """
    Best : O(n) Time | O(n) Space
    Average : O(nlogn) Time | O(n) Space
    Worst : O(nlogn) Time | O(n) Space
    """

    def calcMinRun(n):
        """Returns the minimum length of a run from 23 - 64 so that
        the len(array)/minrun is less than or equal to a power of 2.

        e.g. 1=>1, ..., 63=>63, 64=>32, 65=>33, ..., 127=>64, 128=>32, ...
        """
        r = 0
        while n >= 64:
            r |= n & 1
            n >>= 1
        return n + r

    def insertSort(array, left, right):
        for i in range(left + 1, right + 1):
            temp = array[i]
            j = i - 1
            while j >= left and array[j] > temp:
                array[j + 1] = array[j]
                j -= 1
            array[j + 1] = temp
        return array

    def fastmerge(array1, array2):
        merged_array = []
        while array1 or array2:
            if not array1:
                merged_array.append(array2.pop())
            elif (not array2) or array1[-1] > array2[-1]:
                merged_array.append(array1.pop())
            else:
                merged_array.append(array2.pop())
        merged_array.reverse()
        return merged_array

    n = len(arr)
    minRun = calcMinRun(n)

    # 32만큼 건너뛰면서 삽입 정렬 실행
    for start in range(0, n, minRun):
        end = min(start + minRun - 1, n - 1)
        arr = insertSort(arr, start, end)
    currentSize = minRun

    # minRun이 배열 길이보다 작을 때까지만 minRun * 2 를 한다.
    while currentSize < n:
        for start in range(0, n, currentSize * 2):
            mid = min(n - 1, start + currentSize - 1)
            right = min(start + 2 * currentSize - 1, n - 1)
            merged = fastmerge(
                array1=arr[start : mid + 1], array2=arr[mid + 1 : right + 1]
            )
            arr[start : start + len(merged)] = merged

        currentSize *= 2

    return arr


def quickSort(array):  # in-place | not-stable
    """
    Best : O(nlogn) Time | O(logn) Space
    Average : O(nlogn) Time | O(logn) Space
    Worst : O(n^2) Time | O(logn) Space

    Worst case solved by using random pivot
    """
    if len(array) <= 1:
        return array
    smaller, equal, larger = [], [], []
    pivot = array[randrange(0, len(array))]
    for x in array:
        if x < pivot:
            smaller.append(x)
        elif x == pivot:
            equal.append(x)
        else:
            larger.append(x)
    return quickSort(smaller) + equal + quickSort(larger)


def gnomeSort(array):  # in-place | stable
    """
    Best : O(n) Time | O(1) Space
    Average : O(n^2) Time | O(1) Space
    Worst : O(n^2) Time | O(1) Space
    """
    index = 0
    while index < len(array):
        if index == 0:
            index = index + 1
        if array[index] >= array[index - 1]:
            index = index + 1
        else:
            array[index], array[index - 1] = array[index - 1], array[index]
            index = index - 1

    return array


def mergeSort(arr):  # stable
    """
    Best : O(nlogn) Time | O(n) Space
    Average : O(nlogn) Time | O(n) Space
    Worst : O(nlongn) Time | O(n) Space
    """
    if len(arr) < 2:
        return arr

    mid = len(arr) // 2
    low_arr = mergeSort(arr[:mid])
    high_arr = mergeSort(arr[mid:])

    merged_arr = []
    l = h = 0
    while l < len(low_arr) and h < len(high_arr):
        if low_arr[l] < high_arr[h]:
            merged_arr.append(low_arr[l])
            l += 1
        else:
            merged_arr.append(high_arr[h])
            h += 1
    merged_arr += low_arr[l:]
    merged_arr += high_arr[h:]
    return merged_arr
