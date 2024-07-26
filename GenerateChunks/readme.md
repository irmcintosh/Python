
# Chunk Generator

A simple Python function to split a list into smaller chunks of specified size.

## Function

```python
def generateChunks(listToChunk, chunkSize):
    for i in range(0, len(listToChunk), chunkSize):
        yield listToChunk[i:i+chunkSize]
```

## Description

The `generateChunks` function is a generator that takes a list (`listToChunk`) and an integer (`chunkSize`) as input. It splits the input list into smaller lists (chunks) of size `chunkSize` and yields them one by one.

## Parameters

- `listToChunk`: The list that you want to split into smaller chunks.
- `chunkSize`: The size of each chunk.

## Returns

- Yields chunks of the list with the specified `chunkSize`.

## Usage

Here is an example of how to use the `generateChunks` function:

```python
# Example list
my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Chunk size
chunk_size = 3

# Using the generateChunks function
chunks = generateChunks(my_list, chunk_size)

# Printing the chunks
for chunk in chunks:
    print(chunk)
```

### Output

```
[1, 2, 3]
[4, 5, 6]
[7, 8, 9]
```

## Notes

- If the length of the list is not perfectly divisible by the chunk size, the last chunk will contain the remaining elements.
- This function uses the `yield` statement to return a generator, making it memory efficient for large lists.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


This `README.md` file provides an overview of the function, describes its parameters and return value, and includes an example usage with expected output.
