i = 0
def iPlusPlus():
    print(locals())
    i = i + 1
while i < 10:
    iPlusPlus()
print(i)