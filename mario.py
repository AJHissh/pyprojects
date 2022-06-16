from cs50 import get_int


def main():
    # Get input from user aslong as values are appropriate
    while True:
        try:
            height = get_int('Enter Height:')
            if height <= 0 or height >= 9:
                print('Please try again')
            else:
                pyramid(height)
                break
        except ValueError:
            print('Error')


def pyramid(height):
    # Build pyramid by iterating through loop by adding/removing spaces and hashes per iteration

    hashes = 0
    for i in range(height, -1, -1):
        print(hashes * ' #'.strip() + (i * ' '))
        hashes = hashes + 1
    print()

#     for i in range(1, height):
#         for g in range(i + 1):
#             print('#', end='')
#         for f in range(g + 1):
#             print('', end='')
#         print()



#  for i in range(height):
#         for g in range(i - 1):
#             print('', end=' ')
#         for f in range(i+1):
#             print('#', end=' ')
#         print()

main()
