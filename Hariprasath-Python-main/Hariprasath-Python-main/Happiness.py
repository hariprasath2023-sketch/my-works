n, m = map(int, input().split())  
array = list(map(int, input().split()))  
Likedset = set(map(int, input().split()))  
Dislikedset = set(map(int, input().split()))  


happiness = 0


for element in array:
    if element in Likedset:
        happiness += 1
    elif element in Dislikedset:
        happiness -= 1


print(happiness)
