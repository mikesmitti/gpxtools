#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 03.06.2017

@author: Mike
To-Do:



'''


import tkinter, tkinter.filedialog, tkinter.messagebox
from class_gpx_tools import cgpx_tools as tools
from Globals import SPORTARTEN
import webbrowser


class cgui(tkinter.Frame):
    '''
    classdocs
    '''


    def __init__(self, master=None):
        '''
        Constructor
        '''
        self._toolset = tools()
        tkinter.Frame.__init__(self, master, height=480, width=640)
        self.pack()
        self.createWidgets()

       
    def createWidgets(self):
        #   Labelframe für Einstellungen
        self._guiLabelFrameSettings = tkinter.LabelFrame(self, text="Einstellungen", labelanchor="se").place(x=5, y=261, width=390, height=180)
        
        #    Beenden-Button
        self._guiquit = tkinter.Button(self, text="Beenden", command=self.quit).place(x=550,y=445, width=80, height=25)
        
        #    Datei öffnen Dialog
        self._guiopenfile = tkinter.Button(self, text="Datei öffnen", command=self.on_Openfile).place(x=530,y=10, width=100, height=25)
        
        #    Daten löschen
        self._guideletedata = tkinter.Button(self, text="Daten löschen", command=self.on_deletedata).place(x=430, y=445, width=100, height= 25)
        
        #    Dateien Zusammenfügen
        self._guimerge_tours = tkinter.Button(self, text="Dateien zusammenfügen", command=self.on_Mergetours).place(x=480, y=220, width=150, height=25)
        
        #    GPX-Datei Export Button
        self._guiexportGPX = tkinter.Button(self, text="GPX-Datei exportieren", command=self.on_ExportGPX).place(x=10, y=445, width=140, height=25)
        
        #    Button Logdatei schreiben
        self._guiwritelogfile = tkinter.Button(self, text="Logdatei schreiben", command=self.on_writelogfile).place(x=160, y=445, width=120, height=25)
        
        #    Konsole schreiben
        self._guiwriteconsole = tkinter.Button(self, text="Konsole ausgeben", command=self.on_writeconsole).place(x=290, y=445, width=120, height=25)
        
        #    GPX-Datei Auswerten
        self._guicalculateGPX = tkinter.Button(self, text="Datei auswerten", command=self.on_Convertfile).place(x=530, y=40, width=100, height=25)
        
        #    GPX-Viewer online öffnen
        self._guiopenGPXviewer = tkinter.Button(self, text="GPX-Viewer online öffnen", command=self.on_openGPXviewer).place(x=430, y=405, width=200, height=25)
        
        #    Eingabefeld für Dateinamen
        self._guiFileEntry = tkinter.Entry(self)
        self._guiFileEntry.place(x = 10, y=10 , width=510, height=25)
        self._guiValueFileName = tkinter.StringVar()
        self._guiValueFileName.set("   GPX-Datei wählen")
        self._guiFileEntry["textvariable"] = self._guiValueFileName
        
        #    Eingabefeld für Dateinamen 2
        self._guiFileAddEntry = tkinter.Entry(self)
        self._guiFileAddEntry.place(x = 10, y=220 , width=460, height=25)
        self._guiValueFileNameAdd = tkinter.StringVar()
        self._guiValueFileNameAdd.set("   GPX-Datei zum Anhängen wählen")
        self._guiFileAddEntry["textvariable"] = self._guiValueFileNameAdd
        
        #    Dropdown für die Sportart
        self._guiValueSports = tkinter.StringVar()
        self._guiValueSports.set("Mountainbike")
        self._guiOptionMenuSports = tkinter.OptionMenu(self, self._guiValueSports, *SPORTARTEN)
        self._guiOptionMenuSports.place(x=70, y=270, width=150, height=25)

        #    Spinbox für Sampletime
        self._guiValueSampletime = tkinter.StringVar()
        self._guiValueSampletime.set("5")
        self._guiSpinboxSampletime = tkinter.Spinbox(self, from_=1, to=100, textvariable=self._guiValueSampletime)
        self._guiSpinboxSampletime.place(x=330, y=270, width=50, height=25)
        
        #    Checkboxen anlegen
        self.createwidget_Checkboxes()
           
        #    Textfelder anlegen
        self.createwidget_Entries()
        
        #    Labels zeichnen
        self.createwidget_Labels()
        

        
    
    '''
    Erzeugen von Nicht-GUI Elementen
    '''
    #    Neuen Controller für Wegpunkte anlegen
    def create_new_waypoint_controller_in_gpxtools(self, filename, sports):
        self._toolset.append_waypoint_controller(filename, sports)
        return 0
    
    #    Datei auswerten lassen
    def calc_gpx_tools(self, number_of_controller=0):        
        #    Sampletime ermitteln
        self._toolset.set_sampletime(self._guiValueSampletime.get())
        
        #    Werte im COntroller berechnen
        self._toolset.calc_values_in_controller(number_of_controller, remove_breaks=self._guiValueRemoveBreaks.get())
        
        #    Ausgaben abhängig von der Eingabe
        if self._guiValueWriteConsole.get()==True: self._toolset.print_controller_to_console(number_of_controller)
        if self._guiValueLogFile.get()==True: self._toolset.print_controller_to_logfile(number_of_controller)
        if self._guiValueXMLExport.get()==True: self._toolset.print_controller_to_gpxfile(number_of_controller)
        return 0
    
             
    
    
    
    '''
    Funktionen bei betätigen eines Widget
    Callbacks
    '''
    #    Funktion bei Drücken des 'Datei öffnen' Knopfes
    def on_Openfile(self):
        self._filename = tkinter.filedialog.askopenfilename()
        if len(self._filename) == 0: return -1
        else:
            self._guiValueFileName.set(self._filename)
            #self.on_Convertfile()
        return 0
            
    
    #    Button Datei auswerten
    def on_Convertfile(self):
        #    Prüfen ob Controller vorhanden
        if len(self._toolset._waypoint_controller_list):
            self._toolset.delete_waypoint_controller(0)
        
        #    Sportart ermitteln
        sports = self._guiValueSports.get()
        
        #    Neuen Controller im GPX Tool erzeugen
        self.create_new_waypoint_controller_in_gpxtools(self._filename, sports)
        
        #    Werte im Controller berechnen lassen
        self.calc_gpx_tools()
        
        #    Werte in Zeilen schreiben
        self._guiValueDistance.set(str(round(self._toolset.get_distance_from_controller(0)))+"m")
        self._guiValueDuration.set(str(self._toolset.get_duration_from_controller(0)))
        self._guiValueHeightDifferencePositiv.set(str(round(self._toolset.get_heightdifferencepositiv_from_controller(0)))+"m")
        self._guiValueHeightDifferenceNegativ.set(str(round(self._toolset.get_heightdifferencenegativ_from_controller(0)))+"m")
        self._guiValueWaypoints.set(str(self._toolset.get_number_of_waypoints_from_controller(0)))
        
        return 0
    
    
    #    Bei Klicken von Dateien zusammenfügen
    def on_Mergetours(self):
        #    Wenn keine erste Datei zum zusammenfügen ausgewählt wurde
        if self._toolset.get_number_of_waypointcontrollers()==0:
            tkinter.messagebox.showerror("Fehler", "Es wurde keine Datei ausgewählt an die die Daten angehängt werden sollen. Erst eine Datei auswählen und auswerten.")
            return -1
        
        #    Filedialog
        self._filenameadd = tkinter.filedialog.askopenfilename()
        
        #    Wenn keine Datei ausgewählt wurde
        if len(self._filenameadd) == 0: return -1    
        else:
            self.create_new_waypoint_controller_in_gpxtools(self._filenameadd, self._guiValueSports.get())
            self._guiValueFileNameAdd.set(self._filenameadd)
            self.calc_gpx_tools(1)
            self._toolset.merge_tours(self._guiValueRemoveBreaks.get())
        
        #    Ausgabewerte aktualisieren
        self._guiValueDistance.set(str(round(self._toolset.get_distance_from_controller(0)))+"m")
        self._guiValueDuration.set(str(self._toolset.get_duration_from_controller(0)))
        self._guiValueHeightDifferencePositiv.set(str(round(self._toolset.get_heightdifferencepositiv_from_controller(0)))+"m")
        self._guiValueHeightDifferenceNegativ.set(str(round(self._toolset.get_heightdifferencenegativ_from_controller(0)))+"m")
        self._guiValueWaypoints.set(str(self._toolset.get_number_of_waypoints_from_controller(0)))
        return 0
    
    
    #    Alle Daten löschen
    def on_deletedata(self):
        while len(self._toolset._waypoint_controller_list):
            del self._toolset._waypoint_controller_list[0]
        self.initiate_standardvalues()
        return 0
    
    
    #    Callback für GPX Exportieren
    def on_ExportGPX(self):
        if self._toolset.print_controller_to_gpxfile() == -1:
            tkinter.messagebox.showerror("Fehler", "Keine Daten vorhanden")
            return -1
        else:
            return 0
    
    
    #    Callback für Logdatei schreiben
    def on_writelogfile(self):
        if self._toolset.print_controller_to_logfile() == -1:
            tkinter.messagebox.showerror("Fehler", "Keine Daten vorhanden")
            return -1
        else:
            return 0
            
    
    #    Callback zum Konsole schreiben
    def on_writeconsole(self):
        if self._toolset.print_controller_to_console() == -1:
            tkinter.messagebox.showerror("Fehler", "Keine Daten vorhanden")
            return -1
        else:
            return 0
    
    
    #    GPX-Viewer öffnen
    def on_openGPXviewer(self):
        pfad = tkinter.Tk()
        pfad.clipboard_clear()
        if self._guiValueFileName: pfad.clipboard_append(self._guiValueFileName.get())
        webbrowser.open("https://www.j-berkemeier.de/ShowGPX.html", 2)
    
    '''
    Funktionen zum Erzeugen der Widgets
    '''
    #    Standardwerte erzeugen
    def initiate_standardvalues(self):
        
        self._guiValueFileName.set("   GPX-Datei wählen")
        self._guiFileEntry["textvariable"] = self._guiValueFileName
        
        self._guiValueFileNameAdd.set("   GPX-Datei zum Anhängen wählen")
        self._guiFileAddEntry["textvariable"] = self._guiValueFileNameAdd
        
        self._guiValueDistance.set(" 0m")
        self._guiEntryDistance["textvariable"] = self._guiValueDistance
        
        self._guiValueDuration.set(" 0s")
        self._guiEntryDuration["textvariable"] = self._guiValueDuration
        
        self._guiValueHeightDifferencePositiv.set(" 0m")
        self._guiEntryHeightDifferencePositiv["textvariable"] = self._guiValueHeightDifferencePositiv
        
        self._guiValueHeightDifferenceNegativ.set(" 0m")
        self._guiEntryHeightDifferenceNegativ["textvariable"] = self._guiValueHeightDifferenceNegativ
        
        self._guiValueWaypoints.set(" 0")
        self._guiEntryWaypoints["textvariable"] = self._guiValueWaypoints
    
    
    #    Checkboxen erzeugen
    def createwidget_Checkboxes(self):
        #    Checkbox für den GPX Export
        self._guiValueXMLExport = tkinter.BooleanVar()
        self._guiValueXMLExport.set(False)
        self._guiCheckboxXMLExport=tkinter.Checkbutton(self, anchor="w", text="XML Export", offvalue=False, onvalue=True, variable=self._guiValueXMLExport)
        self._guiCheckboxXMLExport.place(x=10, y=300, height=25, width=200)
        
        #    Checkbox für Logdateiexport
        self._guiValueLogFile = tkinter.BooleanVar()
        self._guiValueLogFile.set(True)
        self._guiCheckboxLogFile=tkinter.Checkbutton(self, anchor="w")
        self._guiCheckboxLogFile["text"] = "Logdatei schreiben"
        self._guiCheckboxLogFile["offvalue"]= False
        self._guiCheckboxLogFile["onvalue"]= True
        self._guiCheckboxLogFile["variable"]= self._guiValueLogFile
        self._guiCheckboxLogFile.place(x=10, y=325, height=25, width=200)
        
        #    Checkbox für Pausen entfernen
        self._guiValueRemoveBreaks = tkinter.BooleanVar()
        self._guiValueRemoveBreaks.set(False)
        self._guiCheckboxRemoveBreaks=tkinter.Checkbutton(self, anchor="w")
        self._guiCheckboxRemoveBreaks["text"] = "Pausen entfernen"
        self._guiCheckboxRemoveBreaks["offvalue"]= False
        self._guiCheckboxRemoveBreaks["onvalue"]= True
        self._guiCheckboxRemoveBreaks["variable"]= self._guiValueRemoveBreaks
        self._guiCheckboxRemoveBreaks.place(x=10, y=375, height=25, width=200)
        
        #    Checkbox für Konsolenausgabe
        self._guiValueWriteConsole = tkinter.BooleanVar()
        self._guiValueWriteConsole.set(False)
        self._guiCheckboxWriteConsole=tkinter.Checkbutton(self, anchor="w")
        self._guiCheckboxWriteConsole["text"] = "Konsole schreiben"
        self._guiCheckboxWriteConsole["offvalue"]= False
        self._guiCheckboxWriteConsole["onvalue"]= True
        self._guiCheckboxWriteConsole["variable"]= self._guiValueWriteConsole
        self._guiCheckboxWriteConsole.place(x=10, y=350, height=25, width=200)    
    
    
    #    Textfelder anlegen
    def createwidget_Entries(self):
        #    Textfeld für Distanz
        self._guiEntryDistance = tkinter.Entry(self)
        self._guiEntryDistance.place(x=150, y=50, width=100, height = 25)
        self._guiValueDistance = tkinter.StringVar()
        self._guiValueDistance.set(" 0m")
        self._guiEntryDistance["textvariable"] = self._guiValueDistance
        
        #    Textfeld für Dauer
        self._guiEntryDuration = tkinter.Entry(self)
        self._guiEntryDuration.place(x=150, y=80, width=100, height=25)
        self._guiValueDuration = tkinter.StringVar()
        self._guiValueDuration.set(" 0s")
        self._guiEntryDuration["textvariable"] = self._guiValueDuration
        
        #    Textfeld für Höhenmeter positiv
        self._guiEntryHeightDifferencePositiv = tkinter.Entry(self)
        self._guiEntryHeightDifferencePositiv.place(x=150, y=110, width=100, height=25)
        self._guiValueHeightDifferencePositiv = tkinter.StringVar()
        self._guiValueHeightDifferencePositiv.set(" 0m")
        self._guiEntryHeightDifferencePositiv["textvariable"] = self._guiValueHeightDifferencePositiv
        
        #    Textfeld für Höhenmeter negativ
        self._guiEntryHeightDifferenceNegativ = tkinter.Entry(self)
        self._guiEntryHeightDifferenceNegativ.place(x=150, y=140, width=100, height=25)
        self._guiValueHeightDifferenceNegativ = tkinter.StringVar()
        self._guiValueHeightDifferenceNegativ.set(" 0m")
        self._guiEntryHeightDifferenceNegativ["textvariable"] = self._guiValueHeightDifferenceNegativ
        
        #    Textfeld für Wegpunkte im Controller
        self._guiEntryWaypoints = tkinter.Entry(self)
        self._guiEntryWaypoints.place(x=150, y=170, width=100, height=25)
        self._guiValueWaypoints = tkinter.StringVar()
        self._guiValueWaypoints.set(" 0")
        self._guiEntryWaypoints["textvariable"] = self._guiValueWaypoints
        
        
    #    Funktion erstellt die Labels im Fenster
    def createwidget_Labels(self):
        
        #    Label vor Distanz
        self._guiLabelDistance = tkinter.Label(self, anchor="e", text="Distanz: ").place(x=10, y=50, width=130, height=25)
        
        #    Label vor Dauer
        self._guiLabelDuration = tkinter.Label(self, anchor="e", text="Dauer: ").place(x=10, y=80, width=130, height=25)
        
        #    Label vor Höhenmeter positiv
        self._guiLabelHeightDifferencePositiv = tkinter.Label(self, anchor="e", text="Höhenmeter positiv: ").place(x=10, y=110, width=130, height=25)
        
        #    Label vor Höhenmeter negativ
        self._guiLabelHeightDifferenceNegativ = tkinter.Label(self, anchor="e", text="Höhenmeter negativ: ").place(x=10, y=140, width=130, height=25)
        
        #    Label vor Wegpunkte
        self._guiLabelWaypoints = tkinter.Label(self, anchor="e", text="Wegpunkte der Strecke: ").place(x=10, y=170, width=130, height=25)   

        #    Label für Sportart
        self._guiLabelSportsAdd = tkinter.Label(self, anchor="e", text="Sportart: ").place(x=10, y=270, width=50, height=25)
        
        #   Label für Sampletime
        self._guiLabelSampletimeAdd = tkinter.Label(self, anchor="w", text="Sampletime:").place(x=250, y=270, width=70, height=25)
        
        #   Labelframe für Einstellungen
        #self._guiLabelFrameSettings = tkinter.LabelFrame(self, text="Einstellungen", labelanchor="ne").place(x=8, y=262, width=250, height=200)