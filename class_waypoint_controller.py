#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 26.03.2017

@author: MikeSmitti

Ein Controller pro .GPX-File

To-Do:


Optional:
-    6 Stellen beim XML Export erzwingen
-    Speichern in Sqlite

'''


from class_waypoint import cwaypoint as wp
from class_routepoint import croutepoint as rp
import xml.etree.ElementTree as ElementTree
import datetime as datetime
from Globals import parametersatz

class cwaypoint_controller(object):
    '''
    classdocs
    '''
    waypoint_controllers = 0

    def __init__(self, filetohandle=0, sports=0):
        '''
        Constructor
        '''
        if not filetohandle:
            self._gpxfilename= str(datetime.datetime.now()) + "_merged.gpx"
        else:
            pass
        self._gpxfilename = filetohandle
        self._sports = sports
        self._Time = 0
        self._StartTime = 0
        self._Distance = 0
        self._HeightDifferencePositiv = 0
        self._HeightDifferenceNegativ = 0
        self._Duration = 0
        self._DurationOriginal = 0
        self._waypointlist = []
        self._routelist = []
        self._tracklist = []
        self._track = 0
        self._track_root = 0
        if filetohandle:
            self.import_gpx_file()
        cwaypoint_controller.waypoint_controllers += 1
        self._sampletime = 5

     
    '''
    Datenimport
    '''
    def import_gpx_file(self):
        #    XML Datei parsen
        self._track = ElementTree.parse(self._gpxfilename)
        self._track_root = self._track.getroot()
        
        for node in self._track_root.iter():
            #print(node.tag, node.attrib, node.text)
            #print(node.text)
            if node.tag == '{http://www.topografix.com/GPX/1/0}rte': break
            if node.tag == '{http://www.topografix.com/GPX/1/0}wpt':
                lat = float(node.attrib.get('lat'))
                lon = float(node.attrib.get('lon'))
            elif node.tag == '{http://www.topografix.com/GPX/1/0}time':
                time = node.text
            elif node.tag == '{http://www.topografix.com/GPX/1/0}ele':
                ele = node.text
            elif node.tag == '{http://www.topografix.com/GPX/1/0}speed':
                speed = node.text
                newpoint = wp(lat, lon, time, ele, speed)
                #print("newpoint " +str(lat), str(lon), str(time), str(ele), str(speed))
                self.add_waypoint(newpoint)
            else:
                pass
        
        rte = 0
        for node in self._track_root.iter():
            if node.tag == '{http://www.topografix.com/GPX/1/0}rte': rte=1
            if node.tag == '{http://www.topografix.com/GPX/1/0}rtept' and rte:
                lat = float(node.attrib.get('lat'))
                lon = float(node.attrib.get('lon'))
            elif node.tag == '{http://www.topografix.com/GPX/1/0}time' and rte:
                time = node.text
            elif node.tag == '{http://www.topografix.com/GPX/1/0}ele' and rte:
                ele = node.text
            elif node.tag == '{http://www.topografix.com/GPX/1/0}speed' and rte:
                speed = node.text
                newpoint = rp(lat, lon, time, ele, speed)
                #print("newpoint " +str(lat), str(lon), str(time), str(ele), str(speed))
                self.add_routepoint(newpoint)
            else:
                pass 
    
    #    Ganze Listen importieren
    def import_lists_from_controller(self, waypoints_to_add, routes_to_add, tracks_to_add=[], calculate=True):
        self._waypointlist.extend(waypoints_to_add)
        self._routelist.extend(routes_to_add)
        self._tracklist.extend(tracks_to_add)
        if calculate:
            self._DurationOriginal = self.calc_duration()
            self.calc_distance()
            self.calc_height()
            self.calc_starttime()
        return 0
    
    

    '''
    Kalkulationsmethoden
    '''
    #    Startzeit ermitteln
    def calc_starttime(self):
        self._StartTime = self._waypointlist[0].get_pythondatetime()
        return self._StartTime
       
    #    Berechnet die Dauer der Aktivität
    def calc_duration(self):
        self._Duration = self._waypointlist[self.get_number_of_waypoints()-1].get_pythondatetime() - self._waypointlist[0].get_pythondatetime()
        self._DurationOriginal = self._Duration
        return self._Duration
    
    #
    def calc_duration_from_factor(self, number_of_waypoints=0):
        timefactor = number_of_waypoints * self._sampletime
        self._Duration=datetime.timedelta(int((timefactor/3600)/24), int(timefactor%60), 0, 0, int(timefactor/60), int(timefactor/3600))
        return self._Duration
    
    
    #    Berechnet die Höhenmeter der Aktivität
    def calc_height(self, sportart = 3):
        #Variablen für die Funktion
        heightnegativ = 0
        heightpositiv = 0
        punkt = 0
        anzahl = self.get_number_of_waypoints()
        
        sport = parametersatz(self.get_sports())
        sportart=sport[0]
        #sportart= int(self.get_sports()[0])
        
        #Wenn weniger als 2 Wegpunkte vorliegen, abbrechen
        if anzahl <= 1: return -1
        
        #    Schleife durchläuft alle Punkte und addiert Hoehenmeter aufwaerts und abwaerts
        for punkt in range(anzahl):
            
            #Beim ersten Punkt abbrechen
            if punkt == 0: continue
            
            #Letzten und aktuellen Wegpunkt ermitteln
            letzterwp = self._waypointlist[punkt-1].get_elevation()
            aktuellerwp = self._waypointlist[punkt].get_elevation()
            
            #Abbrechen wenn Differenz zu groß (Fehler beim Aufzeichnen)
            if abs(letzterwp - aktuellerwp) > sportart: continue
            
            if letzterwp > aktuellerwp:
                heightnegativ = heightnegativ + (letzterwp - aktuellerwp)
            elif letzterwp < aktuellerwp:
                heightpositiv = heightpositiv + (aktuellerwp - letzterwp)
            else:
                continue
        
        #    Werte zuweisen
        self._HeightDifferencePositiv = heightpositiv
        self._HeightDifferenceNegativ = heightnegativ
        
        #Nichts zurückgeben
        return [self._HeightDifferencePositiv, self._HeightDifferenceNegativ]
    
    
    #    Distanz berechnen
    def calc_distance(self):
        #Variablen für die Funktion
        strecke = 0
        punkt = 0
        anzahl = self.get_number_of_waypoints()
        
        #Wenn weniger als 2 Wegpunkte vorliegen, abbrechen
        if anzahl <= 1: return -1
        
        #    Schleife durchläuft alle Punkte und addiert Hoehenmeter aufwaerts und abwaerts
        for punkt in range(anzahl):
            
            #Beim ersten Punkt abbrechen
            if punkt == 0: continue
            
            #Letzten und aktuellen Wegpunkt ermitteln
            letzterwplat = self._waypointlist[punkt-1].get_latitude()
            letzterwplon = self._waypointlist[punkt-1].get_longitude()
            aktuellerwplat = self._waypointlist[punkt].get_latitude()
            aktuellerwplon = self._waypointlist[punkt].get_longitude()
            
            #Strecke nach dem Satz von Pythagoras berechnen
            strecke = strecke + pow(((aktuellerwplat-letzterwplat)*(aktuellerwplat-letzterwplat) + (aktuellerwplon-letzterwplon)*(aktuellerwplon-letzterwplon)),0.5)
        
        #5. Nachkommastelle als Meter anlegen
        self._Distance=strecke*100000
            
        return self._Distance
    
    
    #    Pausenzeiten entfernen:
    #    Bewegungen mit weniger als 1m/sampletime werden entfernt
    def calc_remove_breaks(self):
        #    Hilfsvariablen
        punkt = 0
        anzahl= self.get_number_of_waypoints()
        verworfene_position=[]
        
        #Wenn weniger als 2 Wegpunkte vorliegen, abbrechen
        if anzahl <= 1: return -1
        
        #    Schleife durchläuft alle Punkte und addiert Hoehenmeter aufwaerts und abwaerts
        for punkt in range(anzahl-1, 0, -1):
            
            #Letzten und aktuellen Wegpunkt ermitteln
            if self._waypointlist[punkt].get_speed() <=1:
                verworfene_position.append(punkt)
                self._waypointlist.pop(punkt)

        #    Korrektur für Zeit anlegen
        korrekturfaktor = len(verworfene_position) * int(self._sampletime)
        abweichung = datetime.timedelta(0,int(korrekturfaktor%60),0,0, int(korrekturfaktor/60), int(korrekturfaktor/3600))
        self._Duration = self._Duration - abweichung
    
    
    '''
    Anhaengemethoden
    '''
    #    Haengt Wegpunkt an Liste an
    def add_waypoint(self, wegpunkt):
        self._waypointlist.append(wegpunkt)
    
    #    Haengt Route an Liste an
    def add_routepoint(self, routepoint):
        self._routelist.append(routepoint)
    
    #    Haengt Träck an Liste an
    def add_track(self, track):
        self._tracklist.append(track)
    
        
    '''
    Ausgabefunktionen
    '''    
    #   Ausgabefunktion auf Console
    def print_controller(self):
        print("Datei: " + self._gpxfilename)
        print("Sportart: " + self._sports)
        print("Anzahl der Wegpunkte: " + str(self.get_number_of_waypoints()))
        print("Dauer: " + str(self._Duration))
        print("Aufwärts: " + str(round(self._HeightDifferencePositiv),) + "m")
        print("Abwärts: " + str(round(self._HeightDifferenceNegativ)) +"m")
        print("Strecke: " +str(round(self._Distance)) +"m")
    
    #    Ausgabefunktion in logfile
    def log_controller(self):
        logfile = open(self._gpxfilename.rstrip(".gpx") + "_results.log", "w")
        logfile.write(self._gpxfilename + '\n')
        logfile.write("Sportart: " + self._sports + '\n')
        logfile.write("Anzahl der Wegpunkte: " + str(self.get_number_of_waypoints()) + '\n')
        logfile.write("Dauer: " + str(self._Duration) + '\n')
        logfile.write("Aufwärts: " + str(round(self._HeightDifferencePositiv),) + "m\n")
        logfile.write("Abwärts: " + str(round(self._HeightDifferenceNegativ)) +"m\n")
        logfile.write("Strecke: " +str(round(self._Distance)) +"m\n")
        logfile.close()
        
    #   Export als XML-Datei 
    def export_xml(self):
        datei = open(self._gpxfilename.rstrip(".gpx") + "_new.gpx", "w")
        datei.write("<?xml version=\"1.0\"?>\n")
        datei.write("<gpx\n")
        datei.write("version=\"1.0\"\n")
        datei.write("creator=\"Mike Smitti\"\n")
        datei.write("xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n")
        datei.write("xmlns=\"http://www.topografix.com/GPX/1/0\"\n")
        datei.write("xsi:schemaLocation=\"http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd\">\n")
        
        for each in range(0, len(self._waypointlist)): #self._waypointlist:
            datei.write("<wpt lat=\"" + str(round(self._waypointlist[each]._Latitude,6)) + "\" lon=\"" + str(round(self._waypointlist[each]._Longitude,6)) + "\">\n")
            datei.write("<time>" + self._waypointlist[each]._Time + "</time>\n")
            datei.write("<ele>" + str(self._waypointlist[each]._Elevation) + "</ele>\n")
            datei.write("<speed>" + str(self._waypointlist[each]._Speed) + "</speed>\n")
            datei.write("<name><![CDATA[Point " + str(each) + "]]></name>\n")
            datei.write("</wpt>\n")
        
        datei.write("<rte>\n")
        datei.write("<name>Route</name>\n")
        
        for each in range(0, len(self._routelist)):
            datei.write("<rtept lat=\"" + str(round(self._routelist[each]._Latitude,6)) + "\" lon=\"" + str(round(self._routelist[each]._Longitude,6)) + "\">\n")
            datei.write("<time>" + self._routelist[each]._Time + "</time>\n")
            datei.write("<ele>" + str(self._routelist[each]._Elevation) + "</ele>\n")
            datei.write("<speed>" + str(self._routelist[each]._Speed) + "</speed>\n")
            datei.write("<name><![CDATA[Point " + str(each) + "]]></name>\n")
            datei.write("</rtept>\n")    
        
        datei.write("</rte>\n")    
        datei.write("</gpx>\n")    
        datei.close()
    
        
    '''   
    Getter-Methoden
    '''
    #    Funktion liefert Anzahl an gespeicherten Wegpunkten zurück
    def get_number_of_waypoints(self):
        return len(self._waypointlist)
    
    #    Funktion liefert Anzahl an gespeicherten Routen zurück
    def get_number_of_routs(self):
        return len(self._routelist)
    
    #    Funktion liefert Anzahl an gespeicherten Tracks zurück
    def get_number_of_tracks(self):
        return len(self._tracklist)
    
    #    Getter für Höhenmeter
    def get_heighttupple(self):
        height=[self._HeightDifferencePositiv, self._HeightDifferenceNegativ]
        return height
    
    #    Getter für positive Höhenmeter
    def get_heightdifferencepositiv(self):
        return self._HeightDifferencePositiv
    
    #    Getter für negative Höhenmeter
    def get_heightdifferencenegativ(self):
        return self._HeightDifferenceNegativ
    
    #    Getter für Distanz
    def get_distance(self):
        return self._Distance
    
    #    Getter für Dauer
    def get_duration(self):
        return self._Duration
    
    #    Getter für Dateinamen
    def get_filename(self):
        return self._gpxfilename
    
    #    Getter für Sportart
    def get_sports(self):
        return self._sports
    
    #    Startzeit zurückgeben
    def get_starttime(self):
        return self._StartTime
    
    #    Liste mit Wegpunkten abfragen
    def get_waypointlist(self):
        return self._waypointlist
    
    # Liste mit Routenpunkten abfragen
    def get_routelist(self):
        return self._routelist
    
    
    '''
    Setter-Methoden
    '''
    #    Namen festlegen
    def set_filename(self, new_filename):
        if new_filename: 
            self._gpxfilename= str(new_filename)
            return 0
        else:
            return -1
    
    #    Sportart festlegen
    def set_sports(self, new_sports):
        if new_sports:
            self._sports=new_sports
            return 0
        else:
            return -1
        
    #    Dauer festlegen
    def set_duration(self, new_duration):
        if new_duration:
            self._Duration=new_duration
            return 0
        else:
            return -1
        
    #   Sampletime setzen
    def set_sampletime(self, new_sampletime):
        if new_sampletime:
            self._sampletime=new_sampletime
            return 0
        else:
            return -1