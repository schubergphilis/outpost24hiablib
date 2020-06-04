#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: outpost24lib.py

import logging
from requests import Session
import xml.etree.ElementTree as ET
import json
from .outpost24exceptions import AuthFailed
from .entities import User
from .entities import TargetGroup
from .entities import UserGroup
from .entities import Target
from .entities import Scanner
from outpost24hiablib.tools import xmltools

LOGGER_BASENAME = '''outpost24lib'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


class Outpost24:
    def __init__(self, host, token):
        logger_name = u'{base}.{suffix}'.format(base=LOGGER_BASENAME,
                                                suffix=self.__class__.__name__)
        self._logger = logging.getLogger(logger_name)
        self.host = host
        self.api = '{host}/opi/XMLAPI'.format(host = host)
        self.token = token
        self.session = self._setup_session()


    def _setup_session(self):
        session = Session()
        #TODO: find out why OP24 certificate is invalid and remove this line
        session.verify = False        
        session.params.update({
            'APPTOKEN': self.token
        })
        response = session.get(self.api)
        if not response.ok:
            raise AuthFailed(response.content)
        return session

    def get_users(self):
        payload={'ACTION': 'SUBACCOUNTDATA', 'node': '-1', 'INCLUDESELF': '0', 'limit': '-1', 'id': '-1'}
        response = ET.fromstring(self._post_url(self.api,payload))
        users = response.findall('USERLIST')[0].findall('USER')
        return [User(self,u) for u in users]

    def get_usergroups(self):
        payload={'ACTION': 'USERGROUPDATA', 'limit': '-1'}
        response = ET.fromstring(self._post_url(self.api,payload))
        usergroups = response.findall('USERGROUPLIST')[0].findall('USERGROUP')
        return [UserGroup(self,g) for g in usergroups]

    def get_targetgroups(self):
        payload={'ACTION': 'TARGETGROUPDATA', 'node': '-1', 'INCLUDEUNGROUP': '1', 'limit': '-1', 'id': '-1'}
        response = ET.fromstring(self._post_url(self.api,payload))
        groups = response.findall('GROUPLIST')[0].findall('GROUP')
        return [TargetGroup(self,g) for g in groups]

    def get_targets(self, targetgroup = None):
        groupid = "-1"
        if(targetgroup):
            groupid = str(targetgroup.xid)
        payload={'ACTION': 'TARGETDATA', 'GROUP': groupid, 'limit': '-1', 'sort': 'HOSTNAME', 'dir': 'ASC'}
        response = ET.fromstring(self._post_url(self.api,payload))
        targets = response.findall('TARGETLIST')[0].findall('TARGET')
        return [Target(self,t) for t in targets]

    def get_scanners(self):
        payload={'ACTION': 'SCANNERDATA', 'SCANNERS': '1', 'GROUPS': '1', 'limit': '-1', 'sort': 'NAME', 'dir': 'ASC'}
        response = ET.fromstring(self._post_url(self.api,payload))
        scanners = response.findall('SCANNERLIST')[0].findall('SCANNER')
        return [Scanner(self,s) for s in scanners]

    def get_parent_targetgroup_of_targetgroup(self, targetgroup):
        for t in self.get_targetgroups():
            if(targetgroup.xparentid == t.xid):
                return t
        return None

    def get_child_targetgroups_of_targetgroup(self, targetgroup):
        targetgroups = self.get_targetgroups()
        result = []
        for t in targetgroups:
            if(t.xparentid == targetgroup.xid):
                result.append(t)
        return result

    def get_user_of_targetgroup(self, targetgroup):
        users = self.get_users()
        for u in users:
            if(targetgroup.xuserxid == u.xid):
                return u
        return None
    
    def get_targets_in_targetgroup(self, targetgroup):
        return self.get_targets(targetgroup.xid)

    def get_users_in_usergroup(self, usergroup):
        result = []
        usergroupid = usergroup.xid
        users = self.get_users()
        for u in users:
            groups = u.usergrouplist
            if(usergroupid in groups):
                result.append(u)
        return result

    def get_usergroups_of_user(self, user):
        result = []
        groups = self.get_usergroups()
        grouplist = user.usergrouplist
        for gids in grouplist:
            for g in groups:
                if(gids == g.xid):
                    result.append(g)
        return result

    def create_user(self, vcfirstname, vclastname, vcemail, vcphonenumber, vccountry, vcusername, vcpassword, xid = -1, xisubparentid = -1, emailencryptionkey = 'Unencrypted', 
                    authenticationmethod = 0, twofactorauthentication = 0, credentialid = '', changepasswordonlogon = False, bactive = True, superuser = False, systemnotifications = False, 
                    hiabenroll = False, sendemailnotification = True, ticketparent = False, grouplist = '', usergrouplist = [], targetlist = [], boallhosts = True, allscanners = False, scannerlist = []):
        usergroupliststr = self._convert_list_to_string(usergrouplist)
        targetliststr = self._convert_list_to_string(targetlist)
        scannerliststr = self._convert_list_to_string(scannerlist)

        changepasswordonlogon_val = int(changepasswordonlogon == True)
        bactive_val = int(bactive == True)
        superuser_val = int(superuser == True)
        systemnotifications_val = int(systemnotifications == True)
        hiabenroll_val = int(hiabenroll == True)
        sendemailnotification_val = int(sendemailnotification == True)
        ticketparent_val = int(ticketparent == True)
        boallhosts_val = int(boallhosts == True)
        allscanners_val = int(allscanners == True)

        payload={'ACTION': 'UPDATESUBACCOUNTDATA', 'JSON': 1, 'XID': xid, 'USERGROUPLIST': usergroupliststr, 'VCPASSWORD': vcpassword, 'XISUBPARENTID': xisubparentid, 
                 'VCFIRSTNAME': vcfirstname, 'VCLASTNAME': vclastname, 'VCEMAIL': vcemail, 'VCPHONEMOBILE': vcphonenumber, 'VCCOUNTRY': vccountry, 'EMAILENCRYPTIONKEY': emailencryptionkey,
                 'AUTHENTICATIONMETHOD': authenticationmethod, 'VCUSERNAME': vcusername, 'VCPASSWD1': vcpassword, 'VCPASSWD2': vcpassword, 'TWOFACTORAUTHENTICATION': twofactorauthentication,
                 'CREDENTIALID': credentialid, 'CHANGEPASSWORDONLOGON': changepasswordonlogon_val, 'BACTIVE': bactive_val, 'SUPERUSER': superuser_val, 'SYSTEMNOTIFICATIONS': systemnotifications_val, 
                 'HIABENROLL': hiabenroll_val, 'SENDEMAILNOTIFICATION': sendemailnotification_val, 'TICKETPARENT': ticketparent_val, 'GROUPLIST': grouplist, 'TARGETLIST': targetliststr,
                 'BOALLHOSTS': boallhosts_val, 'ALLSCANNERS': allscanners_val, 'SCANNERLIST': scannerliststr}

        response = self._post_url(self.api,payload)
        r = json.loads(response)
        if(r['success']==True):
            xid = r['data']['XID']
            users = self.get_users()
            for u in users:
                if(u.xid == xid):
                    return u
        elif(r['success']==False):
            print(r['data']['errorMessage'])
            raise RuntimeError(r['data']['errorMessage'])
        return None

    def _convert_list_to_string(self, list):
        result = ''
        for l in list:
            if(result == ''):
                result = str(l.xid)
            else:
                result = result + ',' + str(l.xid)
        return result

    def delete_users(self, userlist):
        userliststr=""
        for u in userlist:
            if(userliststr == ""):
                userliststr = str(u.xid)
            else:
                userliststr = userliststr + ',' + str(u.xid)
        payload={'ACTION': 'REMOVESUBACCOUNTDATA', 'XID': userliststr}
        response = ET.fromstring(self._post_url(self.api,payload))
        result = xmltools.get_str_from_child_if_exists(response, 'SUCCESS')
        if(result == 'true'):
            return True
        return False

    def create_targets(self, targetlist, targetgroup, dnslookup, scanner, CUSTOM0=None, CUSTOM1=None, CUSTOM2=None, CUSTOM3=None, CUSTOM4=None, CUSTOM5=None):
        result = []
        print(targetlist)
        targetliststr = '\n'.join(targetlist)
        dnslookup_val = int(dnslookup == True)
        payload={'ACTION': 'INSERTTARGETDATA', 'JSON': '1', 'GROUP': targetgroup.xid, 'TARGETLIST': targetliststr, 'DNSLOOKUP': dnslookup_val, 'SCANNERID': scanner.xid}
        if(CUSTOM0 != None):
            payload['CUSTOM0'] = CUSTOM0
        if(CUSTOM1 != None):
            payload['CUSTOM1'] = CUSTOM1
        if(CUSTOM2 != None):
            payload['CUSTOM2'] = CUSTOM2
        if(CUSTOM3 != None):
            payload['CUSTOM3'] = CUSTOM3
        if(CUSTOM4 != None):
            payload['CUSTOM4'] = CUSTOM4
        if(CUSTOM5 != None):
            payload['CUSTOM5'] = CUSTOM5
        response = self._post_url(self.api,payload)
        r = json.loads(response)
        if(r['success']==True):
            targets = self.get_targets(targetgroup)
            for t1 in targets:
                for t2 in targetlist:
                    if(t1.hostname == t2 or t1.ipaddress == t2):
                        result.append(t1)
        elif(r['success']==False):
            print(r['data']['errorMessage'])
            raise RuntimeError
        return result

    def delete_targets(self, targetlist):
        targetliststr=""
        for t in targetlist:
            if(targetliststr == ""):
                targetliststr = str(t.xid)
            else:
                targetliststr = targetliststr + ',' + str(t.xid)
        payload={'ACTION': 'REMOVETARGETDATA', 'XID': targetliststr}
        response = ET.fromstring(self._post_url(self.api,payload))
        result = xmltools.get_str_from_child_if_exists(response, 'SUCCESS')
        if(result == 'true'):
            return True
        return False

    def create_targetgroup(self, name, parent_targetgroup=None):
        payload={'ACTION': 'UPDATETARGETGROUPDATA', 'JSON': '1', 'XID': '-1', 'NAME': name}
        if(parent_targetgroup):
            payload[XIPARENTID] = parent_targetgroup.xid
        response = self._post_url(self.api,payload)
        r = json.loads(response)
        if(r['success']==True):
            xid = r['data']['XID']
            tgs = self.get_targetgroups()
            for t in tgs:
                if(t.xid == xid):
                    return t
        elif(r['success']==False):
            print(r['data']['errorMessage'])
            raise RuntimeError
        return None

    def delete_targetgroups(self, targetgrouplist):
        targetgroupliststr=""
        for t in targetgrouplist:
            if(targetgroupliststr == ""):
                targetgroupliststr = str(t.xid)
            else:
                targetgroupliststr = targetgroupliststr + ',' + str(t.xid)
        payload={'ACTION': 'REMOVETARGETGROUPDATA', 'XID': targetgroupliststr}
        response = ET.fromstring(self._post_url(self.api,payload))
        result = xmltools.get_str_from_child_if_exists(response, 'SUCCESS')
        if(result == 'true'):
            return True
        return False

    def _post_url(self, url, payload, request_timeout=120):
        results = []
        payload['REQUESTTIMEOUT'] = request_timeout
        try:
            response = self.session.post(url, data=payload)
            #print(response.text)
            return response.text
        except ValueError:
            self._logger.error('Error getting url :%s', url)
            return []
