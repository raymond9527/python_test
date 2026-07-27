def backtrack(nums, path):

    if len(path) == len(nums):

        print(path)

        return

    for num in nums:

        if num in path:

            continue

        path.append(num)

        backtrack(nums, path)

        path.pop()


nums = [1, 2, 3, 4]

backtrack(nums, [])
