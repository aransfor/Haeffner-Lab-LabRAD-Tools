#Created on Jan 24, 2011
#@author: christopherreilly, Michael Ramm

"""
### BEGIN NODE INFO
[info]
name = Paul Box
version = 1.1
description = 
instancename = Paul Box

[startup]
cmdline = %PYTHON% %FILE%
timeout = 20

[shutdown]
message = 987654321
timeout = 20
### END NODE INFO
"""

import socket
import shelve
import os
from labrad.server import LabradServer, setting

class script:
    scriptname = ''
    filemodtime = ''
    varlist = [];

class PBError( Exception ):
    pass

class PaulBoxServer( LabradServer ):
    #change nodename in environment vars
    name = 'Paul Box'

    def initServer( self ):
        self.connectSocket()
        self.loadDatabase()
        self.loadScripts()

    def connectSocket( self ):
        port = 8880
        self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        local_ip = socket.gethostbyname( socket.gethostname() )
        self.sock.connect( ( local_ip, port ) )

    def loadDatabase( self ):
        """
        Load database.
        """
        self.db = {}


    def loadScripts( self ):
        """
        Load scrips
        
        TODO: details
        """

        def parse_sequence( sequence_string ):
            varlist = []
            for line in sequence_string.splitlines():
                setvarindex = line.find( "self.set_variable(" )
                if setvarindex > -1: #if line contains 'self.set_variable'
                    poundindex = line.find( "#" )
                    if poundindex == -1 or poundindex > setvarindex: #if the line is not commented out ('#' after 'self.setvariable')
                        end = line.find( ")" )
                        relevantline = line[setvarindex + len( "self.set_variable(" ):end]
                        values = relevantline.split( ',' )
                        var_type = str( values[0].replace( '"', '' ) ) #gets rid of quotes by replacing them with nothing
                        var_name = str( values[1].replace( '"', '' ) )
                        default_val = str( values[2] )
                        if len( values ) == 5:
                            min_val = str( values[3] )
                            max_val = str( values[4] )
                        else:
                            min_val = ''
                            max_val = ''
                        varlist.append( [var_name, var_type, default_val, min_val, max_val] )
            return varlist

        directory = '/home/lattice/Desktop/sequencer2/PulseSequences/protected/'

        for filename in os.listdir( directory ):
            path = directory + filename
            try:
                fobj = open( path )
                sequence_string = fobj.read()
                fobj.close()
                modtime = os.stat( path ).st_mtime
            except:
                raise RuntimeError( "Error while loading sequence:" + str( filename ) )
            newscript = script()
            newscript.scriptname = filename
            newscript.filemodtime = modtime
            newscript.varlist = parse_sequence( sequence_string )
            self.db[filename] = newscript;

    def sendPB( self, toSend ):
        """
        Lower level sending
        """
        self.sock.sendall( toSend )

    def recPB( self ):
        """
        Lower level receiving
        """
        return '\n'.join( self.sock.recv( 4 * 8192 ) for i in range( 2 ) )

    @setting( 0, 'Send command',
              scriptName = 's: script name',
              inputList = '*2s: input values',
              returns = 's: response from PB' )
    def sendCommand( self, c, scriptName, inputList ):
        """
        Send command to Paul's Box.
        """
        if len( filter( lambda x: len( x ) == 3, inputList ) ) != len( inputList ):
            raise PBError( 'Input parameters must be in form of a list of 3 entry lists' )

        def flattenInputList( li ):
            return ';'.join( ','.join( i ) for i in li )

        toSend = 'NAME,%s;' % scriptName + flattenInputList( inputList )
        print toSend
        self.sendPB( toSend )
        resp = self.recPB()
        return resp
    
    @setting(1,'Get available scripts',
             returns = '*s: list of available scripts')
    def availableScripts(self, c ):
        return self.db.keys()
    
    @setting(2,'Get variable list',
             script = 's: name of script',
             returns = '*2s: list of script\'s variables')
    def getVariables(self, c, script):
        return self.db[script].varlist
        
if __name__ == "__main__":
    from labrad import util
    util.runServer(PaulBoxServer())







