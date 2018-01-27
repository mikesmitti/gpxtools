#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 26.03.2017

@author: MikeSmitti

To-Do:

'''
import datetime as datetime

class cwaypoint(object):
    waypoints = 0
    '''
    Konstruktor
    '''
    def __init__(self, latitude, longitude, time, elevation, speed):
        self._Latitude = float(latitude)
        self._Longitude = float(longitude)
        self._Elevation = float(elevation)
        self._Time = time
        self._Speed = float(speed)
        self._Pythondatetime = self.calc_python_timestamp()
        self._Distance = 0
        self._HeightDifference = 0
        cwaypoint.waypoints += 1
      
        
    '''
    Brechnungen
    '''
    #    Zeitwert als datetime.datetime berechnen
    def calc_python_timestamp(self):
        if self.parse_time() == -1: return -1
        return datetime.datetime(int(self._Time[0:4]), int(self._Time[5:7]),int(self._Time[8:10]),int(self._Time[11:13]),int(self._Time[14:16]),int(self._Time[17:19]))
    
    
    '''
    Getter und Setter
    '''
    #    Latitude abfragen
    def get_latitude(self):
        return self._Latitude
    
    def set_latitude(self, latitude):
        self._Latitude=latitude
    
    #    Longitude abfragen
    def get_longitude(self):
        return self._Longitude
    
    def set_longitude(self, longitude):
        self._Longitude=longitude
    
    #    Höhe abfragen
    def get_elevation(self):
        return self._Elevation
    
    #    Zeitstring abfragen
    def get_time(self):
        return self._Time
    
    #    Distanz abfragen
    def get_distance(self):
        return self._Distance
    
    #    Zahlenwert für Zeit abfragen
    def get_pythondatetime(self):
        return self._Pythondatetime
    
    #    Geschwindigkeit abfragen
    def get_speed(self):
        return self._Speed
    
    
    
    '''
    Ausgabefunktionen
    '''
    #    Wegpunkt ausgeben
    def print_waypoint(self):
        print("Latitude: ", self._Latitude)
        print("Longitude: ", self._Longitude)
        print("Elevation: ", self._Elevation)
        print("Zeit: ", self._Time)
        print("Distanz: ", self._Distance)
        print("Hoehendifferenz: ", self._HeightDifference)
        print("Wegpunkte: ", cwaypoint.waypoints)
        
    
    
    '''
    Hilfsfunktionen
    '''
    #    Time-String parsen ob das Format passt
    def parse_time(self):
        if self._Time.find("T") == -1 : return -1
        if self._Time.find("Z") == -1 : return -1
        if self._Time.find("-") != 4 : return -1
        if self._Time.rfind("-") != 7 : return -1
        if self._Time.find(":") != 13 : return -1
        if self._Time.rfind(":") != 16 : return -1
        return 1