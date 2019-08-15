#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 15:18:22 2019

@author: kumbim
"""

distance = lambda Drone: (abs((Drone[3]-Drone[1]))**2+(abs(Drone[2]-Drone[0]))**2)**(1/2)
def Travel(Drone):
    if Drone[5] == 0 and Drone[-3] !=0:
        if (Drone[-3] -round(Drone[-3])) > 0:
            Drone[5] = Drone[4] + (round(Drone[-3])+1)
        else:
            Drone[5] = Drone[4] + round(Drone[-3])
        Drone[4] += 1
        if Drone[4] == Drone[5]:
            Drone[0] = Drone[2]
            Drone[1] = Drone[3]
            Drone[5] = 0
            print('Delivered at first step!')
        else:
            print("Continued at first step")
    elif Drone[5] != 0 and Drone[-3] != 0:
        Drone[4] += 1
        if Drone[4] == Drone[5]:
            Drone[0] = Drone[2]
            Drone[1] = Drone[3]
            Drone[5] = 0
            print('Arrived!')
            #Next bit will get rid of current distance and time period 
            Drone[-3] = 0
        else:
            print("Continuing")
    else:
        print('Already at Destination!')
    return Drone

def Deliver(Drone,distance,Orders,Travel):
    for Order in Orders:
        if Drone[-1] == Order[0]:# Find order related to the specific drone
            if Drone[-2] == 'D':    
                if Drone[0] == Drone[2] and Drone[1] == Drone[3]:
                    # Unload items in Drone's inventory
                    x = 0
                    for item in Drone[6]:
                        Order[3][item] -= Drone[6][item]
                        Drone[6][item] = 0
                    remaining = 'No'
                    for item in Order[3]:
                        if Order[3][item] == 0:
                            pass
                        else:
                            remaining = 'Yes'
                    if remaining == 'Yes':
                        Drone[-2] = 'L'
                        Drone[4] += 1
                    else:
                        Drone[-2] = 'A'
                        Order[0] = 'F'
                        Drone[4] += 1
                else:
                    distance(Drone)
                    Drone[-3] = (float("{0:.3f}".format(distance(Drone))))
                    Travel(Drone)
            else:
                pass
        else:
            pass
        
distanceNew = lambda x,y: (abs((x[1]-y[1]))**2+(abs(x[0]-y[0]))**2)**(1/2)
def Load(Warehouse,Drone,Orders,Payload):
    for Order in Orders:
        if Order[0] == Drone[-1] and Drone[-2] == 'L':
            nearest = 0 # Set this variable to 0 so that once the nearest Warehouse is found, it goes here
            current_distance = 1000000000 # Set this to a very high number so that each time a closer distance is found, this gets updated
            for Warehouse in Warehouses: # For every Warehouse in the Warehouses variable...
                x = distanceNew((Warehouse[1],Warehouse[2]),(Order[1],Order[2])) # Calculates distance between Warehouse and the location of the order
                if current_distance > x: # If the distance of the warehouse is less than the current smallest distance, then we upgrade nearest
                    current_distance = x
                    nearest = Warehouse
                else:
                    pass # Otherwise don't change anything at all and go onto the next Warehouse (Checks all Warehouses in Warehouses)
            Drone[2] = nearest[0] # Updates Drone's destination parameters
            Drone[3] = nearest[1]
            if Drone[0] == Drone[2] and Drone[1] == Drone[3]: # If the Drone is at its destination (Warehouse)
                for Warehouse in Warehouses:
                    if Warehouse[1] == Drone[0] and Warehouse[2] == Drone[1]:
                        print('Drone Before Loading: ',Drone)
                        print('Warehouse: ',Warehouse)
                        print('Loading items...')
                        for ProductType in Order[3]: 
                            weight = Warehouse[3][ProductType][1] # Finds the weight of the item in the order
                            NumItem = Order[3][ProductType] # Finds out how much of the item the user wants
                            current_weight = 0 # This is the weight of items in the Drone and will accumulate once items are added
                            while current_weight < Payload: # While the Drone isn't full...
                                if Drone[6][ProductType] < NumItem: # If number of items currently in the drone is less than the amount ordered, continue
                                    if weight < Payload: # If one more item doesn't make the weight greater than the payload...
                                        if Warehouse[3][ProductType][0] > 0: # If the Warehouse still has item available in stock
                                            current_weight += weight # Change the weigt of Drone as an item is being added
                                            Drone[6][ProductType] += 1 # Adds item to Drone's imventory
                                            Payload -= weight # Crucial as the remaining Payload will be different as an item is already on board.
                                            Warehouse[3][ProductType][0] -= 1 #Remove item from Warehouse stock
                                        else:
                                            break
                                    else:
                                        break
                                else:
                                    break
                            print('')
                            Drone[4] += 1 # Add an additional time period for loading
                            Drone[-2] = 'D' # Once the Drone is fully loaded, it will then go ontp Delivery
                            Drone[2] = Order[1] 
                            Drone[3] = Order[2]
                        print('Loading Complete')
                        print('Drone After Loading: ',Drone)
                        print('Warehouse: ',Warehouse)
                        print('')
            else: # If the Drone is not at the Warehouse, it will travel there.
                Drone[-3] = (float("{0:.3f}".format(distanceNew((Drone[0],Drone[1]),(Drone[2],Drone[3])))))
                Travel(Drone)
                print('Travelling to Warehouse: ',Drone)
        
    else:
        pass

distanceNew = lambda x,y: (abs((x[1]-y[1]))**2+(abs(x[0]-y[0]))**2)**(1/2)
def LoadNew(Warehouses,Drone,Orders,Payload):
    for Order in Orders:
        if Order[0] == Drone[-1] and Drone[-2] == 'L':
            nearest = 0 # Set this variable to 0 so that once the nearest Warehouse is found, it goes here
            current_distance = 1000000000 # Set this to a very high number so that each time a closer distance is found, this gets updated
            for Warehouse in Warehouses: # For every Warehouse in the Warehouses variable...
                x = distanceNew((Warehouse[1],Warehouse[2]),(Order[1],Order[2])) # Calculates distance between Warehouse and the location of the order
                if current_distance > x: # If the distance of the warehouse is less than the current smallest distance, then we upgrade nearest
                    current_distance = x
                    nearest = Warehouse
                else:
                    pass # Otherwise don't change anything at all and go onto the next Warehouse (Checks all Warehouses in Warehouses)
            Drone[2] = nearest[0] # Updates Drone's destination parameters
            Drone[3] = nearest[1]
            if Drone[0] == Drone[2] and Drone[1] == Drone[3]: # If the Drone is at its destination (Warehouse)
                for Warehouse in Warehouses:
                    if Warehouse[1] == Drone[0] and Warehouse[2] == Drone[1]:
                        print('Drone Before Loading: ',Drone)
                        print('Warehouse: ',Warehouse)
                        print('Loading items...')
                        for ProductType in Order[3]:
                            if Order[3][ProductType] > 0:   
                                if Warehouse[3][ProductType][0] > 0:
                                    current_weight = 0
                                    item_weight = Warehouse[3][ProductType][1]
                                    NumItem = Order[3][ProductType]
                                    if item_weight <= Payload:
                                        while current_weight < Payload and NumItem > 0 and Warehouse[3][ProductType][0] > 0:
                                            current_weight += item_weight
                                            NumItem -= 1
                                            Drone[6][ProductType] += 1
                                            Warehouse[3][ProductType][0] -= 1
                                        Payload -= current_weight
                                    else:
                                        break
                        Drone[4] += 1 # Add an additional time period for loading
                        Drone[-2] = 'D' # Once the Drone is fully loaded, it will then go ontp Delivery
                        Drone[2] = Order[1] 
                        Drone[3] = Order[2]
                        print('Loading Complete')
                        print('Drone After Loading: ',Drone)
                        print('Warehouse: ',Warehouse)
                        print('')
            else: # If the Drone is not at the Warehouse, it will travel there.
                Drone[-3] = (float("{0:.3f}".format(distanceNew((Drone[0],Drone[1]),(Drone[2],Drone[3])))))
                Travel(Drone)
                print('Travelling to Warehouse: ',Drone)
        
    else:
        pass

def SimpleOrderAssignment(Orders,Drones): 
    for Drone in Drones: # Looks at all the Drones
        if Drone[-2] == 'A': # If that Drone is available then continue.
            for Order in Orders: # Look through the orders to see if are any unassigned orders 'U'
                if Order[0] == 'U': 
                    Order[0] = Drone[-1] # Once an unassigned order is found, it becomes assigned by the Drones ID so it can be called upon later when loading and delivering.
                    Drone[-2] = 'L' # Drone becomes unavailable and the enxt step once assignment is loading hence 'L'
                    break # Once order is assigned, tehre is no need to look as the other orders as this Drone is occupied 
                else:
                    pass # If the order is not 'U' (Unassigned), then go onto the next order
        else:
            pass #If Drone is not 'A' (Available), then move onto the next Drone
    return Orders, Drones

NumType = int(input('How many different product Types are there? '))
NumWare = int(input('How many Warehouses are there? '))
Payload = 500
weights = []
Total = []
Orders = []
count = 0
print('')
print('========================== Warehouse Initialization =========================')
print('')
for Type in range(NumType):
    inputs = int(input("Enter weight: "))
    weights.append(inputs)
Warehouses = [[num,0,0,{}] for num in range(NumWare)]
for warehouse in Warehouses:
    for Type in range(NumType):
        x = str(Type)
        warehouse[-1][x] = [0,weights[Type]]
        y = 'Enter amount of Good '+ str(Type) + ' in Warehouse #'+str(count)+ ': '
        indtotal = int(input(y))
        warehouse[-1][str(Type)][0] = indtotal
    count +=1
else:
    pass
print('Warehouses Initialized!')
print('')
print('=========================== Order Initialization ============================')
print('')
NumOrders = int(input('Enter the number of orders: '))
for i in range(NumOrders):
    Orders.append(['U'])
    Dest = input('Where do you want the items delivered? ')
    Orders[i].append(int(Dest[0]))
    Orders[i].append(int(Dest[1]))
    Orders[i].append({})
    for num in range(0,NumType):
        x = 'How much of Product Type '+str(num)+' do you want? '
        entry = int(input(x))
        Orders[i][-1][str(num)] = entry
print('Orders Initialized!')
print('')
print('=========================== Drone Initialization ============================')
print('')
NumDrone = int(input('How many Drones are there? '))
Drones = [[0,0,0,0,0,0,{},0,'A',num] for num in range(NumDrone)]
for Drone in Drones:
    for Type in range(NumType):
        x = str(Type)
        Drone[6][x] = 0
print('Drones Initialized!')

Time = int(input('How long will the simulation last? '))
for TimePeriod in range(Time):
    print('################# Time Period: '+str(TimePeriod)+' #################')
    SimpleOrderAssignment(Orders,Drones)
    for Drone in Drones:
        if Drone[-2] == 'L':
            LoadNew(Warehouses,Drone,Orders,Payload)
        elif Drone[-2] == 'D':
            Deliver(Drone,distance,Orders,Travel)
    print('Drone: ',Drone)
        
    print('')
