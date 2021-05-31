#import database
from csv import writer
from queue import Queue
import numpy as np
import websocket
import _thread
import json
import sys
from datetime import datetime
import time
from datetime import date as d
import ssl

# define request id
QUERY_HEADSET_ID                    =   1
CONNECT_HEADSET_ID                  =   2
REQUEST_ACCESS_ID                   =   3
AUTHORIZE_ID                        =   4
CREATE_SESSION_ID                   =   5
SUB_REQUEST_ID                      =   6
SETUP_PROFILE_ID                    =   7
QUERY_PROFILE_ID                    =   8
BCI_PROFILE_ID                      =   9
DISCONNECT_HEADSET_ID               =   10
CREATE_RECORD_REQUEST_ID            =   11
STOP_RECORD_REQUEST_ID              =   12
EXPORT_RECORD_ID                    =   13
INJECT_MARKER_REQUEST_ID            =   14
UPDATE_RECORD_ID                    =   15
CLOSE_SESSION_ID                    =   16
GET_USER_ID                         =   17
UNSUBSCRIBE_ID                      =   18
DELETE_RECORD_ID                    =   19
UPDATE_MARKER_ID                    =   20

class Cortex():

    def __init__(self, user, name, debug_mode=False):
        self.Q_ALL = Queue(maxsize=1028)
        self.Q_EEG = Queue(maxsize=28)
        self.Q_POW = Queue(maxsize=12)
        self.Q_DEV = Queue(maxsize=65)

        self.name = name

        url = "wss://localhost:6868"
        self.ws = websocket.create_connection(url,
                                              sslopt={"cert_reqs": ssl.CERT_NONE})
        self.user = user
        self.debug = debug_mode

        self.streams = ["eeg",
        #               "mot", because it is not supported by our headset
                        "dev",
                        "pow",
                        "met",
        #                "com",
        #               "fac",
                        "sys"]

    """ AUTHENTICATION SETUP """

    def getUserLogin(self):
        cmd = {"id": GET_USER_ID,
               "jsonrpc": "2.0",
               "method": "getUserLogin"}

        self.ws.send(json.dumps(cmd, indent=4))

    def requestAccess(self):
        cmd = {"id": REQUEST_ACCESS_ID,
               "jsonrpc": "2.0",
               "method": "requestAccess",
               "params": {
                   "clientId": self.user['client_id'],
                   "clientSecret": self.user['client_secret'],

               }
               }
        self.ws.send(json.dumps(cmd, indent=4))
        result = self.ws.recv()
        result_dic = json.loads(result)
        if self.debug:
            print('Request Access:', json.dumps(result_dic, indent=4))
            return result_dic

    def authorize(self):
        cmd = {"jsonrpc": "2.0",
               "method": "authorize",
               "params": {
                   "clientId": self.user['client_id'],
                   "clientSecret": self.user['client_secret'],
                   "debit": 11
               },
               "id": AUTHORIZE_ID,
               }
        self.ws.send(json.dumps(cmd, indent=4))
        result = self.ws.recv()
        result_dic = json.loads(result)

        #To get a Cortex Token --> self.auth
        if self.debug:
            print('auth request \n', json.dumps(cmd, indent=4))

        self.ws.send(json.dumps(cmd))

        while True:
            result = self.ws.recv()
            result_dic = json.loads(result)
            if 'id' in result_dic:
                if self.debug:
                    print('auth result \n', json.dumps(result_dic, indent=4))
                self.auth = result_dic['result']['cortexToken']
                return self.auth
                break

    """HEADSET SETUP"""

    def queryHeadsets(self):
        cmd = {"id": QUERY_HEADSET_ID,
               "jsonrpc": "2.0",
               "method": "queryHeadsets",
               "params": {
                   "id": "EPOCPLUS-3B9AEBFF"
               }
               }
        self.ws.send(json.dumps(cmd, indent=4))
        result = self.ws.recv()
        result_dic = json.loads(result)
        if self.debug:
            print('Request Access:', json.dumps(result_dic, indent=4))
            return result_dic

    def controlDevice(self, command='connect'):
        cmd = {"id": CONNECT_HEADSET_ID,
               "jsonrpc": "2.0",
               "method": "controlDevice",
               "params": {
                   "command": command,
                   "headset": "EPOCPLUS-3B9AEBFF"
               }
               }
        self.ws.send(json.dumps(cmd, indent=4))
        time.sleep(5)
        result = self.ws.recv()
        result_dic = json.loads(result)
        if self.debug:
            print('Request Access:', json.dumps(result_dic, indent=4))
            return result_dic


    """SESSION SETUP"""

    def createSession(self, status="active"):
        cmd = {"id": CREATE_SESSION_ID,
               "jsonrpc": "2.0",
               "method": "createSession",
               "params": {
                   "cortexToken": self.auth,
                   "headset": "EPOCPLUS-3B9AEBFF",
                   "status": status
               }
               }

        if self.debug:
            print(json.dumps(cmd, indent=4))

        self.ws.send(json.dumps(cmd))
        result = self.ws.recv()
        result_dic = json.loads(result)

        if self.debug:
            print(json.dumps(result_dic, indent=4))

        self.session_id = result_dic['result']['id']

        return self.session_id

    """     
    def updateSession(self, status="active"):

        cmd = {"id": 1,
                "jsonrpc": "2.0",
                "method": "updateSession",
                "params": {
                "cortexToken": self.auth,
                "session": self.session_id,
                "status": status
                    }
                }
        self.ws.send(json.dumps(cmd, indent = 4))
        result = self.ws.recv()
        result_dic = json.loads(result)
            if self.debug:
            print(json.dumps(result_dic, indent=4))"""

    def closeSession(self, status="close"):

        cmd = {"id": CLOSE_SESSION_ID,
               "jsonrpc": "2.0",
               "method": "updateSession",
               "params": {
                   "cortexToken": self.auth,
                   "session": self.session_id,
                   "status": status
               }
               }
        self.ws.send(json.dumps(cmd, indent=4))
        result = self.ws.recv()
        result_dic = json.loads(result)
        if self.debug:
            print(json.dumps(result_dic, indent=4))

        self.closedSession = result_dic

        return self.closedSession

    """EEG DATA SUBSCRIBE SETUP """

    def subscribe(self, streams=[]):
        cmd = {"id": SUB_REQUEST_ID,
               "jsonrpc": "2.0",
               "method": "subscribe",
               "params": {
                   "cortexToken": self.auth,
                   "session": self.session_id,
                   "streams": streams
               }
               }
        self.ws.send(json.dumps(cmd, indent=4))
        result = self.ws.recv()
        result_dic = json.loads(result)
        self.sub_data = result_dic

        return self.sub_data

    def unsubscribe(self, streams=[]):
        cmd = {"id": UNSUBSCRIBE_ID,
               "jsonrpc": "2.0",
               "method": "unsubscribe",
               "params": {
                   "cortexToken": self.auth,
                   "session": self.session_id,
                   "streams": streams
               }
               }
        self.ws.send(json.dumps(cmd, indent=4))
        result = self.ws.recv()
        result_dic = json.loads(result)
        self.unsub_data = result_dic


        return self.unsub_data

    """RECORD SETUP"""

    def startRecord(self, title="", description=""):
        cmd = {"id": CREATE_RECORD_REQUEST_ID,
               "jsonrpc": "2.0",
               "method": "createRecord",
               "params": {
                   "cortexToken": self.auth,
                   "title": title,
                   "description": description,
                   "session": self.session_id
               }
               }
        self.ws.send(json.dumps(cmd, indent=4))
        result = self.ws.recv()
        result_dic = json.loads(result)
        if self.debug:
            print('start record request \n',
                  json.dumps(cmd, indent=4))
            print('start record result \n',
                  json.dumps(result_dic, indent=4))

        record_id = result_dic['result']['record']['uuid']

        return result_dic, record_id

    def stopRecord(self):
        cmd = {"id": STOP_RECORD_REQUEST_ID,
               "jsonrpc": "2.0",
               "method": "stopRecord",
               "params": {
                   "cortexToken": self.auth,
                   "session": self.session_id
               }
               }
        self.ws.send(json.dumps(cmd, indent=4))
        result = self.ws.recv()
        result_dic = json.loads(result)

    def updateRecord(self, title="", description=""):
        cmd = {"id": UPDATE_RECORD_ID,
               "jsonrpc": "2.0",
               "method": "updateRecord",
               "params": {
                   "cortexToken": self.auth,
                   "title": title,
                   "description": description,
                   "record": self.record_id
               }
               }


        self.ws.send(json.dumps(cmd, indent=4))
        result = self.ws.recv()
        result_dic = json.loads(result)

    def deleteRecord(self):
        cmd = {"id": DELETE_RECORD_ID,
               "jsonrpc": "2.0",
               "method": "deleteRecord",
               "params": {
                   "cortexToken": self.auth,
                   "records": self.record_id
               }
               }
        self.ws.send(json.dumps(cmd, indent=4))
        result = self.ws.recv()
        result_dic = json.loads(result)

    def exportRecord(self,
                     folder,
                     export_format,
                     export_version,
                     record_ids,
                     export_types):

        all_records = []

        export_record_request = {"jsonrpc": "2.0",
                                 "id": EXPORT_RECORD_ID,
                                 "method": "exportRecord",
                                 "params": {
                                     "cortexToken": self.auth,
                                     "folder": folder,
                                     "format": export_format,
                                     "streamTypes": export_types,
                                     "recordIds": record_ids,
                                     'includeMarkerExtraInfos': True
                                 }
                                 }

        # "version": export_version,
        if export_format == 'CSV':
            export_record_request['params']['version'] = export_version

        if self.debug:
            print('export record request \n',
                  json.dumps(export_record_request, indent=4))

        self.ws.send(json.dumps(export_record_request))


        # wait until export record completed
        while True:
            result = self.ws.recv()
            result_dic = json.loads(result)

            if self.debug:
                print('export record result \n', json.dumps(result_dic))
                all_records.append(result_dic)

            if 'result' in result_dic:
                if 'success' in result_dic['result']:
                    if len(result_dic['result']['success']) > 0:
                        break


        return all_records

    """MARKERS SETUP"""

    def injectMarker(self, marker):
        cmd = {"jsonrpc": "2.0",
               "id": 1,
               "method": "injectMarker",
               "params": {
                   "cortexToken": self.auth,
                   "session": self.session_id,
                   "label": marker['Label'],
                   "value": marker['value'],
                   "port": 'Software',
                   "time": time.time()*1000
               }
               }

        #e1b3e982-4b0f-4827-8c95-02e7e61c7ef0
        # ID c82f61b5-81bc-4302-b5f1-98c40f3e4299'


        MARKER_FOUND = False
        self.ws.send(json.dumps(cmd))
        while MARKER_FOUND == False:
            result = self.ws.recv()
            result_dic = json.loads(result)
            if 'eeg' in result_dic:
                print(result_dic['eeg'][18])
                print('loop')
                if len(result_dic['eeg'][18]) != 0:
                    print(result_dic['eeg'][18][0])
                    self.marker_id = result_dic['eeg'][18][0]["markerId"]
                    print("********")
                    print(self.marker_id)
                    print("********")
                    MARKER_FOUND = True


        return self.marker_id



        #self.marker_id = result_dic['result']['id']

    def updateMarker(self, marker):
        cmd = {"id": 1,
               "jsonrpc": "2.0",
               "method": "updateMarker",
               "params": {
                   "cortexToken": self.auth,
                   "session": self.session_id,
                   "markerId": marker,
                   "time": time.time()*1000
               }
               }
        print('UPDATING')
        self.ws.send(json.dumps(cmd))
        result = self.ws.recv()
        result_dic = json.loads(result)

        print(result_dic)
    #######

    """BCI SETUP"""

    def bciProfile(self):
        cmd = {"id": BCI_PROFILE_ID,
               "jsonrpc": "2.0",
               "method": "queryProfile",
               "params": {
                   "cortexToken": self.auth
               }
               }
        self.ws.send(json.dumps(cmd))
        result = self.ws.recv()
        result_dic = json.loads(result)

    def setupProfile(self, profile='', status=''):
        cmd = {"id": SETUP_PROFILE_ID,
               "jsonrpc": "2.0",
               "method": "setupProfile",
               "params": {
                   "cortexToken": self.auth,
                   "profile": profile,
                   "status": status
               }
               }
        self.ws.send(json.dumps(cmd))
        result = self.ws.recv()
        result_dic = json.loads(result)

    def basicSteps(self):
        values = []
        try:
            qH = self.queryHeadsets()
            values.append(qH)

            cD = self.controlDevice()
            values.append(cD)

            rA = self.requestAccess()
            values.append(rA)

            auth = self.authorize()
            values.append(auth)

        except Exception as BASIC_ERROR:
            self._error_message("BASIC STEPS", BASIC_ERROR)

        finally:
            return values

    # Find way to make it work multiple times when haveing GUI window opened

    def buildLink(self, title="def", description="def", streams=["eeg", "dev", "pow", "sys"]):
        values = []
        # out comment the unneeded streams

        try:
            self._printer("Creating Session")
            createS = self.createSession()
            values.append(createS)

            self._printer("Start Recording")
            startR, self.rec_id = self.startRecord(title, description)
            values.append(startR)

            self._printer("Start Data Subscription")
            subs = self.subscribe(streams)
            values.append(subs)

        except Exception as LINK_ERROR:
            self._error_message("BUILDING LINK", LINK_ERROR)

        finally:
            return values

    def terminateLink(self, streams=["eeg", "dev", "pow", "sys"]):
        values = []

        try:
            self._printer("Start Data Unsubscription")
            unsubs = self.unsubscribe(streams)
            values.append(unsubs)

            self._printer("Stop Data Record")
            stopR = self.stopRecord()
            values.append(stopR)

            self._printer("Close Session")
            closeS = self.closeSession()
            values.append(closeS)

            self._printer("Exporting Data")
            self.expData = self.exportRecord(folder='/Users/alexander/Desktop',
                                        export_format='CSV',
                                        export_types=streams,
                                        export_version="V1",
                                        record_ids=self.rec_id)

            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            file_name = 'EEG_' + str(self.name) + '_' + str(current_time) + '_' + str(d.today()) + '.csv'
            self._pre_build_csv(file_name, 'eeg')

            for elem in self.expData:
                if 'eeg' in elem:
                    row = str(elem['time']) + ', ' + str(elem['eeg']).replace("[", "")
                    row = row.replace("]", "")
                    print("element: ")
                    print(row)
                    print(row.split(', '))
                    self._build_csv(file_name, row.split(', '), 'eeg')

            file_name = 'POW_' + str(self.name) + '_' + str(current_time) + '_' + str(d.today()) + '.csv'
            self._pre_build_csv(file_name, 'pow')

            for elem in self.expData:
                if 'pow' in elem:
                    row = str(elem['time']) + ', ' + str(elem['pow']).replace("[", "")
                    row = row.replace("]", "")
                    print("element: ")
                    print(row)
                    print(row.split(', '))
                    self._build_csv(file_name, row.split(', '), 'pow')

            file_name = 'DEV_' + str(self.name) + '_' + str(current_time) + '_' + str(d.today()) + '.csv'
            self._pre_build_csv(file_name, 'dev')

            for elem in self.expData:
                if 'dev' in elem:
                    row = str(elem['time']) + ', ' + str(elem['dev']).replace("[", "")
                    row = row.replace("]", "")
                    print("element: ")
                    print(row)
                    print(row.split(', '))
                    self._build_csv(file_name, row.split(', '), 'dev')

            print("EEG DATA SUCCESS")

            # createSession needs to be "activated", read under createSession
        except Exception as TERM_ERROR:
            self._error_message("TERMINATING LINK", TERM_ERROR)

        finally:
            return values

    """ Stream & Queues """

    def stream_processing(self, th, val):
        _thread.start_new_thread(self.filter_main_Q, ('Thread Q', 3))
        while True:
            self.Q_ALL.put(json.loads(self.ws.recv()))

    def filter_main_Q(self, text, val):
        counter = 0
        while True:
            time.sleep(0.1)
            result = self.Q_ALL.get()

            if 'eeg' in result:
                q_elem = np.array(result['eeg'])
                self.Q_EEG.put(q_elem)

            elif 'pow' in result:
                q_elem = np.array(result['pow'])
                self.Q_POW.put(q_elem)

            elif 'dev' in result:
                q_elem = np.array(result['dev'])
                print('QUEUE ELEM')
                print(q_elem)
                self.Q_DEV.put(q_elem)
            #print remaining elements in each queue

    """ HELPER FUNCTIONS """
    def _pre_build_csv(self, file, sig):
        row = []
        if sig == 'eeg':
            row = ['Timestamp', 'EEG.Counter', 'EEG.Interpolated', 'EEG.AF3', 'EEG.F7', 'EEG.F3', 'EEG.FC5',
                   'EEG.T7', 'EEG.P7', 'EEG.O1', 'EEG.O2', 'EEG.P8', 'EEG.T8', 'EEG.FC6', 'EEG.F4', 'EEG.F8',
                   'EEG.AF4', 'EEG.RawCq']

        elif sig == 'dev':
            row = ['Timestamp','EEG.Battery', 'EEG.MarkerHardware',
                   'CQ.AF3',    'CQ.F7',    'CQ.F3',    'CQ.FC5',   'CQ.T7',    'CQ.P7',    'CQ.O1',    'CQ.O2',
                   'CQCQ.P8',   'CQ.T8',    'CQ.FC6',   'CQ.F4',    'CQ.F8',    'CQ.AF4',   'CQ.Overall']

        elif sig == 'pow':
            row = ['Timestamp',
                   'POW.AF3.Theta'  ,   'POW.AF3.Alpha',   'POW.AF3.BetaL',   'POW.AF3.BetaH',  'POW.AF3.Gamma',
                   'POW.F7.Theta'   ,   'POW.F7.Alpha' ,   'POW.F7.BetaL' ,   'POW.F7.BetaH' ,  'POW.F7.Gamma',
                   'POW.F3.Theta'   ,   'POW.F3.Alpha' ,   'POW.F3.BetaL' ,   'POW.F3.BetaH' ,  'POW.F3.Gamma',
                   'POW.FC5.Theta'  ,   'POW.FC5.Alpha',   'POW.FC5.BetaL',   'POW.FC5.BetaH',	'POW.FC5.Gamma',
                   'POW.T7.Theta'   ,   'POW.T7.Alpha' ,   'POW.T7.BetaL' ,   'POW.T7.BetaH' ,	'POW.T7.Gamma',
                   'POW.P7.Theta'   ,   'POW.P7.Alpha' ,   'POW.P7.BetaL' ,   'POW.P7.BetaH' ,	'POW.P7.Gamma',
                   'POW.O1.Theta'   ,   'POW.O1.Alpha' ,   'POW.O1.BetaL' ,   'POW.O1.BetaH' ,	'POW.O1.Gamma',
                   'POW.O2.Theta'   ,   'POW.O2.Alpha' ,   'POW.O2.BetaL' ,   'POW.O2.BetaH' ,	'POW.O2.Gamma',
                   'POW.P8.Theta'   ,   'POW.P8.Alpha' ,   'POW.P8.BetaL' ,   'POW.P8.BetaH' ,	'POW.P8.Gamma',
                   'POW.T8.Theta'   ,   'POW.T8.Alpha' ,   'POW.T8.BetaL' ,   'POW.T8.BetaH' ,	'POW.T8.Gamma'	,
                   'POW.FC6.Theta'  ,   'POW.FC6.Alpha',   'POW.FC6.BetaL',   'POW.FC6.BetaH',	'POW.FC6.Gamma',
                   'POW.F4.Theta'   ,   'POW.F4.Alpha' ,   'POW.F4.BetaL' ,   'POW.F4.BetaH' ,	'POW.F4.Gamma',
                   'POW.F8.Theta'   ,   'POW.F8.Alpha' ,   'POW.F8.BetaL' ,   'POW.F8.BetaH' ,	'POW.F8.Gamma',
                   'POW.AF4.Theta'  ,   'POW.AF4.Alpha',   'POW.AF4.BetaL',   'POW.AF4.BetaH',	'POW.AF4.Gamma']

        self._build_csv(file, row, sig, True)

    def _build_csv(self, file, row, sig, pre_build=False):
        if pre_build == False:
            if sig == 'eeg':
                row.pop(18)
                for i in range(18):
                    row[i] = float(row[i])

            elif sig == 'dev':
                for i in range(len(row)):
                    row[i] = float(row[i])

            elif sig == 'pow':
                for i in range(len(row)):
                    row[i] = float(row[i])
                    print(row[i])
        else:
            print('Pre-building of CSV File')

        with open(file, "a+", newline='') as csv_file:
            csv_writer = writer(csv_file)
            csv_writer.writerow(row)

    def _printer(self, val):
        message = "\n- - - - - - - - - - - -\n" \
                  "CURRENT STATUS: {}..." \
                  "\n- - - - - - - - - - - -\n".format(str(val))
        print(message)

    def _error_message(self, val, text):
        message = "\n---------------------------\n" \
                  "ERROR DURING {}\n" \
                  "MESSAGE: {}" \
                  "\n---------------------------\n".format(val, text)
        print(message)

        # pass data frames with overlap
        # use cython
        # circular fifo queue faster-fifo
        # https://pypi.org/project/faster-fifo/


if __name__ == '__ain__':

    # implement a buffer for eeg data from the cortex api
    # for live mode
    # 1. have windows
    # 2. overlapping
    # 3. save to variable
    # 4. call dummy function
    # 5. show possible sequence of moving cubes

    #input_id = {'client_id': 'FqBZUgxeajUkiNwhRaTmRiUcSHRmwl42PneVbNh1','client_secret': 'FXQj2Arp7Uw28eAbnWkUG1SBzqWAu5hY2pNpRZDIsqkvBCZFobj5voPAvGH0YrEAC0cx1CasxLwepJ9lKXDVY3qCAagD4DNCugxk29aUjehvSaTYBef3jLycrPf5Tmqz'}


    time.sleep(2)



    #print("Status", testing[1]["error"]['message'])


