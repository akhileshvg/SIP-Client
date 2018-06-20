import sys

import pjsua as pj

import threading

import time



# Default method to print the log of the call.

def log_cb(level, str, len):

    print(str),



# The class to where events of the account registration process are sent 

class Macc(pj.AccountCallback):

    def __init__(self, acc):

        pj.AccountCallback.__init__(self, acc)





# The class which deals with the  events in call process 

class Mccb(pj.CallCallback):

    def __init__(self, call=None):

        pj.CallCallback.__init__(self, call)

    

    

    def on_state(self):

        print("Call Status:", self.call.info().state_text),

        print("Status code:", self.call.info().last_code),

        print(" ("+self.call.info().last_reason+")")
        global skip
        if self.call.info().state_text=="DISCONNCTD": # A decison statement to determine whether the call has been disconnected from the other side
            skip=1
        else:
            skip=0


        

    

    def on_media_state(self): #connects the call to the sound device 

        
        if self.call.info().media_state == pj.MediaState.ACTIVE:

            
            call_slot = self.call.info().conf_slot

            lib.conf_connect(call_slot, 0)

            lib.conf_connect(0, call_slot)

            print("HELLO WORLD ----------------------------------call in progress----------------------------------------------------Hello WORLD")

 # Configuring the account with data from user.           
def info():
    sIp = raw_input("Enter the server's IP address : ")
    usr = raw_input("Enter user ID/Display name :  ")
    pas = raw_input("Enter your password : ")
    a_conf = pj.AccountConfig(domain = sIp, username = usr, password = pas, display = usr)
    a_conf.id ="sip:"+usr
    a_conf.reg_uri ='sip:'+sIp+':5060'
    return a_conf


# ------------------------------------------------------------Start of program-----------------------------------------------------------------------------------

try:

    # Create library instance of Lib class

    lib = pj.Lib()



    # Instantiate library with default config

    lib.init(log_cfg = pj.LogConfig(level=3, callback=log_cb))


    # Configuring one Transport Object

    t_conf = pj.TransportConfig()

    print "*********************************Welcome to the SIP Client program******************************************"
    print "\n\n"
    print "****************************\tLet's start with the intial registration\t *********************************** "


    CIP=raw_input("Enter the Client IP address: ")
    

    t_conf.bound_addr = CIP

    transport = lib.create_transport(pj.TransportType.UDP,t_conf)



    # Starting the instance of Lib class

    lib.start()

    lib.set_null_snd_dev() # specifies absence of any sound devices.


    print "***************************************** \tPBX Account setup \t********************************************"  
    # Configuring Account class to register with Registrar server

    # Calling a function that writes to the register SIP header.
    a_conf=info()
    

    a_cb = Macc(a_conf)
    acc = lib.create_account(a_conf,cb=a_cb)



    

    acc.set_callback(a_cb)



    print('\n')
    print "************************************************Registration Process Complete***************************************"
    print("Status: ",acc.info().reg_status, \

         '(' + acc.info().reg_reason + ')')


    t = 0

    while t==0:
        print "\n******\t\tCall Menu\t\t********\n"
        makcall=raw_input(" \t\t\tTo make a call press Y/y to exit press any other button\n")
        print "\n"

        if makcall=="y" or makcall=="Y":

            # Starting Calling process.
            print"****************************Hit ENTER to exit current call session ******************\n\n\n"
            b=raw_input("Enter the destination URI: ")
            call = acc.make_call(b, Mccb())
            input = sys.stdin.readline().rstrip()
            if skip !=1:

                call.hangup()
            


        else :
            t = 1

    print('To unregister from server and exit the program hit ENTER ')
    input = sys.stdin.readline().rstrip()

    lib.destroy()

    lib = None
    print "************************************* program shutdown *********************************************************\n***************************************** Have a nice day **************************************************************"
    
except pj.Error, e:

    print("Exception: " + str(e))

    lib.destroy()

    lib = None
    print "************************************* program shutdown ************************************************************\n**************************************** Have a nice day *************************************************************"
    sys.exit(1)
