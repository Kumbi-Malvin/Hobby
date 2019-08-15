#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 17:27:10 2019
@author: kumbim
"""

class SDC(object):
    
    def __init__(self,num): # Initialisng all the components of a car
        self.num = num
        self.call_sign = 'Available'
        self.cur_pos = [0,0]
        self.ride = 'None'
    
    def drive(self,time_period): # Situation where the car is on route to the start of a ride. This either takes place when it isn't at the starting place and is on-route and not actually delivering a person; it's not time for the ride yet but you are on your way/already there waiting.
        if self.ride != 'None':
            if (self.ride[0:2] != self.cur_pos and (self.call_sign == 'Available' or self.call_sign == 'OR')) or (self.ride[4]>= time_period and self.ride[0:2] != self.cur_pos) or (self.ride[4] > time_period and self.ride[0:2] == self.cur_pos):
                self.call_sign = 'OR' 
                if self.ride[0] != self.cur_pos[0]: # If the x co-ordinate isn't the same as the start position x co-ordinate
                    self.call_sign = 'OR'
                    self.cur_pos[0] += round( (self.ride[0] - self.cur_pos[0]) / abs(self.ride[0] - self.cur_pos[0]) ) # Move x co-ordinate
                elif self.ride[1] != self.cur_pos[1]: # If the y co-ordinate isn't the same as the start position y co-ordinate
                    self.call_sign = 'OR'
                    self.cur_pos[1] += round( (self.ride[1] - self.cur_pos[1]) / abs(self.ride[1] - self.cur_pos[1]) ) # Move y co-ordinate
                else:
                    self.call_sign = 'W' # Otherwise you are probably already there so you wait
            elif self.cur_pos[0] != self.ride[2] and time_period >= self.ride[4] and time_period <= self.ride[-1]: # x co-ordinate isn't equal to the destination x co-ordinate and the timeperiod is within the start and finish time of the ride
                self.call_sign = 'D'
                self.cur_pos[0] += round( (self.ride[2] - self.cur_pos[0]) / abs(self.ride[2] - self.cur_pos[0]) )
            elif self.cur_pos[1] != self.ride[3] and time_period >= self.ride[4] and time_period <= self.ride[-1]: # y co-ordinate isn't equal to the destination y co-ordinate and the timeperiod is within the start and finish time of the ride
                self.call_sign = 'D'
                self.cur_pos[1] += round( (self.ride[3] - self.cur_pos[1]) / abs(self.ride[3] - self.cur_pos[1]) )
            else:
                self.call_sign = 'Idle / Ride Expired' # Otherwise the ride is probably out of the start/finish range so the ride expires
            if self.cur_pos[0] == self.ride[2] and self.cur_pos[1] == self.ride[3]: # After a move is made, this cheks if the ride finishes on that move
                self.call_sign = 'F'
            else:
                pass
        else:
            pass
        
    def achievable(self,timeperiod): # This function checks whether takes taking a ride is worth it
        dist_to_start = abs(self.cur_pos[0] - self.ride[0]) + abs(self.cur_pos[1] - self.ride[1])
        ride_dist = abs(self.ride[0] - self.ride[2]) + abs(self.ride[1] - self.ride[3])
        if (ride_dist + dist_to_start + timeperiod - 1 <= self.ride[-1]) and (ride_dist <= (abs(self.ride[-1] - self.ride[-2]))): #  The conditions are that the length of the ride and the distance to the start of the ride are less than the finish time given what time period we are in.
            return True
        else:
            return False

class City(object):
    
    def __init__(self,name):
        self.vehicles = []
        self.rides = []
        self.name = name
        self.finished_rides = []
    def addCars(self,num_car):
        for num in range(num_car):
            self.vehicles.append(SDC(num))
    def addRides(self,rides):
        for ride in rides:
            self.rides.append(ride)
    def rideAssignment(self,time_period):
        for car in self.vehicles:
            if car.ride == 'None' and car.call_sign == 'Available':
                for ride in self.rides:
                    car.ride = ride
                    if car.achievable(time_period):
                        self.rides.pop(self.rides.index(ride))
                        break
                    else:
                        car.ride = 'None'
                        continue
            else:
                pass
    def finished(self):
        for car in self.vehicles:
            if car.call_sign == 'F' and car.ride != 'None':
                self.finished_rides.append(car.ride)
                car.ride = 'None'
                car.call_sign = 'Available'
            else:
                pass
    def Bayes(self):
        pass

def Simulation(City,rides):
    num_car = int(input('Enter the number of Cars: '))
    time = int(input('Enter length of Simulation: '))
    City.addCars(num_car)
    City.addRides(rides)
    for time_period in range(time):
        City.rideAssignment(time_period)
        for car in City.vehicles:
            car.drive(time_period)
            print('-------------------')
            print('Time Period:',time_period)
            print('Call Sign:',car.call_sign)
            print('Current Position:',car.cur_pos)
        City.finished()
        print('******************')
        print('')
    print('The Simulation has Finished!')
