#lift 
lift={
    "current":0,
    "last":None,
    "pending":[]
    }

#definitions
def set_floors():
    floors=input("Enter number of floors:")
    floor_inputs=enumerate(range(floors),start=1)
    print(floors,floor_inputs)
    return floors

def input(floor_num):
    if lift["current"]!=floor_num:
        lift["pending"].append(floor_num)
    

#program
floors=set_floors()
