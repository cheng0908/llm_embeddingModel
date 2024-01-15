# class parrent:
# 	x = 1
	
# class child1(parrent):
	
#     def __init__():
#         self.x = 2
    
#     def __new__(cls):
#           return super().__new__()

# class child2(parrent):
# 	pass

# print(parrent.x, child1.x, child2.x)
# child1.x = 2
# print(parrent.x, child1.x, child2.x)
# parrent.x = 3
# print(parrent.x, child1.x, child2.x)

print([lambda x : i * x for i in range(5)])