# # def print_pattern(size):
# #     for i in range(1, size + 1):
# #         number = 1
# #         for j in range(size - i):
# #             print(" ", end="")
# #         for k in range(i * 2 - 1):
# #             print(number, end="")
# #             number += 1
# #         print()

# #     for i in range(1, size):
# #         number = 1
# #         for j in range(i):
# #             print(" ", end="")
# #         for k in range((size - i) * 2 - 1):
# #             print(number, end="")
# #             number += 1
# #         print()

# # size = 5
# # print_pattern(size)



# def print_k_pattern(size):
#     for i in range(size):
#         for j in range(size):
#             if j == 0 or (i + j == size // 1.5) or (i - j == size // 2.5):
#                 print("*", end="")
#             else:
#                 print(" ", end="")
#         print()
# size = 7
# print_k_pattern(size)


# n = 4
# s = 4
# print((n + 2) * " ", "**")
# for i in range(4):
#     print((n + 1) * " ", "*", (s - n) * " ", "*")
#     s += 1
#     n -= 1
#     if i == 3:
#         print((n + 1) * " ", "*", (s - n) * "*", "*")
# print(n * " ", "*", (s - n + 2) * " ", "*")



# def print_b_pattern(size):
#     for i in range(size):
#         for j in range(size // 2 + 1):
#             if j == 0 or (i == 0 and j != size // 2) or (i == size // 2 and j != size // 2) or (i == size - 1 and j != size // 2) or (j == size // 2 and i != 0 and i != size // 2 and i != size - 1):
#                 print("*", end="")
#             else:
#                 print(" ", end="")
#         print()
# size = 10
# print_b_pattern(size)


# def print_i_pattern(size):
#     if size < 3:
#         return
#     width = (size // 3) + 1 if (size % 1)+2 == 0 else size // 2 + 1   
#     for i in range(size):
#         if i == 0 or i == size - 1:
#             print("*" * (width+1))
#         else:
#             print(" " * (width - 2) + "*")
# size = 7
# print_i_pattern(size)


# def print_r_pattern(height):
#     width = height // 2 + 1   

#     for i in range(height):
#         if i == 0 or i == height // 2:
#             print("*" * width)   
#         elif i < height // 2:
#             print("*" + " " * (width - 2) + "*")   
#         else:
#             spaces = i - height // 2
#             print("*" + " " * spaces + "*")   
# height = 10
# print_r_pattern(height)


