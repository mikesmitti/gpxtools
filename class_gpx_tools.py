#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 03.06.2017

@author: Mike

To-Do:



'''


from class_waypoint_controller import cwaypoint_controller as wpc
from os import path as path

class cgpx_tools(object):
    '''
    classdocs
    '''
    gpx_tools = 0

    def __init__(self):
        '''
        Constructor
        '''
        self._waypoint_controller_list = []
        self._sampletime = 5
        cgpx_tools.gpx_tools+=1
    
        
    #    Neuen Controller für Datei anlegen
    def append_waypoint_controller(self, filetohandle=0, sports=0):
        #    Neuen Controller anlegen
        controller = wpc(filetohandle, sports)
        self._waypoint_controller_list.append(controller)
        return 0
    
    
    #    Controller entfernen
    def delete_waypoint_controller(self, controller_to_delete=0):
        if self._waypoint_controller_list[controller_to_delete]:
            del self._waypoint_controller_list[controller_to_delete]
        else:
            return -1
    
    
    
    #   Berechnungen veranlassen
    #    @number_of_controller: Nummer des Controllers bei dem die Operation durchgeführt werden soll
    def calc_values_in_controller(self, number_of_controller=0, remove_breaks=False):
        #    Plausibilitaetscheck
        if self.number_of_controller_check(number_of_controller) == 0:
            #    Berechnungen durchführen
            self._waypoint_controller_list[number_of_controller].calc_duration()
            self._waypoint_controller_list[number_of_controller].calc_height()
            self._waypoint_controller_list[number_of_controller].calc_distance()
            self._waypoint_controller_list[number_of_controller].calc_starttime()
            if remove_breaks==True: self._waypoint_controller_list[number_of_controller].calc_remove_breaks()
            return 0
        else:
            return -1
    
    
    '''
    Dateien zusammenfügen
    '''
    def merge_tours(self, remove_breaks):
        #    Neuen Controller anfügen
        self.append_waypoint_controller(filetohandle=0, sports=self._waypoint_controller_list[0].get_sports())
        
        #    Startzeit korrigieren
        if self._waypoint_controller_list[0].get_starttime() < self._waypoint_controller_list[1].get_starttime():
            #    Listen des ersten Controllers kopieren
            self._waypoint_controller_list[2].import_lists_from_controller(self._waypoint_controller_list[0].get_waypointlist(), self._waypoint_controller_list[0].get_routelist())
            #    Listen des zweiten Controllers kopieren
            self._waypoint_controller_list[2].import_lists_from_controller(self._waypoint_controller_list[1].get_waypointlist(), self._waypoint_controller_list[1].get_routelist())
        else:
            #    Listen des zweiten Controllers kopieren
            self._waypoint_controller_list[2].import_lists_from_controller(self._waypoint_controller_list[1].get_waypointlist(), self._waypoint_controller_list[1].get_routelist())
            #    Listen des ersten Controllers kopieren
            self._waypoint_controller_list[2].import_lists_from_controller(self._waypoint_controller_list[0].get_waypointlist(), self._waypoint_controller_list[0].get_routelist())
        
        #    Neue Werte berechnen
        self.calc_values_in_controller(2, remove_breaks)
        
        #    Unterbrechung entfernen
        self._waypoint_controller_list[2].set_duration(self._waypoint_controller_list[0].get_duration()+self._waypoint_controller_list[1].get_duration())
        
        #    Neuen Namen festlegen
        pfad = path.split(self._waypoint_controller_list[1].get_filename())
        self._waypoint_controller_list[2].set_filename(self._waypoint_controller_list[0].get_filename().rstrip(".gpx") + "_" + pfad[1])#self._waypoint_controller_list[1].get_filename())
        
        #    Alte Dateien löschen
        del self._waypoint_controller_list[0]
        del self._waypoint_controller_list[0]

        #    GPX Datei erzeugen
        self.print_controller_to_gpxfile(0)
        return 0
        
    
    '''
    Getter-Methoden
    '''
    #    Getter für Dauer eines Tracks in einem Controller
    def get_duration_from_controller(self, number_of_controller=0):
        return self._waypoint_controller_list[number_of_controller].get_duration()
    
    def get_distance_from_controller(self, number_of_controller=0):
        return self._waypoint_controller_list[number_of_controller].get_distance()
    
    def get_heightdifferencepositiv_from_controller(self, number_of_controller=0):
        return self._waypoint_controller_list[number_of_controller].get_heightdifferencepositiv()
    
    def get_heightdifferencenegativ_from_controller(self, number_of_controller=0):
        return self._waypoint_controller_list[number_of_controller].get_heightdifferencenegativ()
    
    def get_number_of_waypoints_from_controller(self, number_of_controller=0):
        return self._waypoint_controller_list[number_of_controller].get_number_of_waypoints()
     
    def get_number_of_waypointcontrollers(self):
        return len(self._waypoint_controller_list)
       
    
    '''
    Setter-Methoden
    '''
    def set_sampletime(self, new_sampletime):
        self._sampletime = new_sampletime
        if len(self._waypoint_controller_list):
            for each in range(0, len(self._waypoint_controller_list)):
                self._waypoint_controller_list[each].set_sampletime(new_sampletime)
        
    '''
    Ausgabemethoden
    '''
    #    Bildschirmausgabe
    #    @number_of_controller: Nummer des Controllers bei dem die Operation durchgeführt werden soll
    def print_controller_to_console(self, number_of_controller=0):
        #    Plausibilitaetscheck
        if self.number_of_controller_check(number_of_controller) == 0:    
            #    Logmethode des untergeordneten Controllers
            self._waypoint_controller_list[number_of_controller].print_controller()
            return 0
        else:
            return -1
    
    
    #    Ausgabe in Logdatei
    #    @number_of_controller: Nummer des Controllers bei dem die Operation durchgeführt werden soll
    def print_controller_to_logfile(self, number_of_controller=0):
        #    Plausibilitaetscheck
        if self.number_of_controller_check(number_of_controller) == 0:
            #    Logmethode des untergeordneten Controllers
            self._waypoint_controller_list[number_of_controller].log_controller()
            return 0
        else:
            return -1
    
    
    #    Ausgabe in XML Datei im GPX Format
    def print_controller_to_gpxfile(self, number_of_controller=0):
        #    Plausibilitaetscheck
        if self.number_of_controller_check(number_of_controller) == 0:
            #    Logmethode des untergeordneten Controllers
            self._waypoint_controller_list[number_of_controller].export_xml()
            return 0
        else:
            return -1
    
    
    '''
    Hilfsmethoden
    '''
    #    Check ob Controller vorhanden
    def number_of_controller_check(self, number_of_controller):
        #    Plausibilitaetscheck
        if len(self._waypoint_controller_list)==0: return -1
        if number_of_controller < 0: return -1
        if number_of_controller >= len(self._waypoint_controller_list): return -1
        return 0