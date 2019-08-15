#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 21:48:28 2019
@author: kumbim
"""
###################### Initializing Number of Cars #############################

while True: # This is for the number of cars that will travel arounf the map
    try:
        numCars = int(input('Enter the Number of Cars: '))
        if numCars == 0:
            print('Invalid Integer')
        else:
            break
    except ValueError:
        print('Invalid Input')
available = [[0,0] for num in range(numCars)] # Number of cars that are available at any given point in time (step)
occupied = [] # Number of cars that are occupied at any given point in time (step)
temp = [] # This will be used for cars that are on route to pick up the first ride
Rides = [[0,0,1,3,2,9],[1,2,1,0,0,9],[2,0,2,2,0,9],[1,1,3,0,4,9],[0,1,2,1,3,9]] # This is the database of rides that are currently on offer. It entails start coordinates, finish coordinates, earliest start and latest finish
FinishedRides = []
remove = []
################################################################################
############################# Functions ########################################

def AvailTemp(temp,available,Rides):
    for i in range(len(available)):
        combination = available[i]+Rides[i]
        temp.append(combination)
    available.clear()
    return temp, available, Rides

def RemoveRide(Rides,temp):
    for car in temp:
        CurrentRide = car[2:]
        if CurrentRide in Rides:
            x = Rides.pop(Rides.index(CurrentRide))
            remove.append(x)
        else:
            pass
    return Rides,temp

def TempOccup(temp,occupied):
    for car in temp:
        if car[0] == car[2] and car[1] == car[3]:
            x = temp.pop(temp.index(car))
            occupied.append(x)
        else:
            pass
    return temp,occupied

def OccupFinRides(occupied,FinishedRides,available, CalculateScore,score,TimePeriod):
    for car in occupied:
        if car[0] == car[4] and car[1] == car[5]:
            x = occupied.pop(occupied.index(car))
            CalculateScore(x,TimePeriod,score)
            FinishedRides.append(x[2:])
            available.append(x[0:2])
        else:
            pass
    return occupied, FinishedRides, available

def Driving(temp,destination,TimePeriod):
    if destination == 'start':
        pos = 2
        for car in temp:
            if car[0] != car[pos]:
                car[0] += round((car[pos]-car[0])/abs(car[pos]-car[0]))
            elif car[1] != car[pos+1]:
                car[1] += round((car[pos+1]-car[1])/abs(car[pos+1]-car[1]))
            else:
                pass
        return temp
    elif destination == 'finish':
        pos = 4
        for car in temp:
            if TimePeriod < car[6]:
                pass
            else:
                if car[0] != car[pos]:
                    car[0] += round((car[pos]-car[0])/abs(car[pos]-car[0]))
                elif car[1] != car[pos+1]:
                    car[1] += round((car[pos+1]-car[1])/abs(car[pos+1]-car[1]))
                else:
                    pass
        return temp
    else:
        print('Invalid Input')
        pass
def CalculateScore(variable,TimePeriod,score):
    if variable[-1] > TimePeriod:
        DistanceTravelled = abs(variable[2] - variable[4]) + abs(variable[3] - variable[5])
        score.append(DistanceTravelled)
    else:
        pass
    return variable,TimePeriod,score
        
################################################################################
################# Simulation ###################################################

while True:
    try:
        Time = int(input('How many steps do you want the simulation to have?: '))
        
        score = []
        print('Rides:',Rides)
        for TimePeriod in range(Time):
            print('-------- Time Period = {x} --------'.format(x= TimePeriod))
            print('Cars available:',available)
            if len(available) > 0:
                if len(Rides) > 0:
                    AvailTemp(temp,available,Rides)
                    RemoveRide(Rides,temp)
                else:
                    pass
            else:
                pass
            
            # Temp Operations
            TempOccup(temp,occupied)
            print('Before (temp):',temp)
            Driving(temp,'start',TimePeriod) # Could switch this with the TempOccup function 2 lines below so that a car only moves a maximum of 1 times per time period. With 1 car doing all the rides there was a tendency for the car to move once and then fall into the occupied list and then later on in the same iteration (when operations are being done on the occupied list, it moves again which isn't allowed.)
            print('After (temp):',temp)
            
            # Occupied Operations
            print('Before (Occup):',occupied)
            Driving(occupied,'finish',TimePeriod)
            print('After(Occup):',occupied)
            OccupFinRides(occupied,FinishedRides,available, CalculateScore,score,TimePeriod)
            print('Finished Rides:',FinishedRides)
            print('Rides left:',Rides)
            print('')
        else:
            print('Total Score is: {x}'.format(x = sum(score)))
            print('Simulation has finished')
        break
    except ValueError:
        print('Invalid Input!')
        continue
