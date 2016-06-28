import websocket
import _thread as thread
import time
import sys
import json
import os
import random
import items

row=40
column=110
attempts=0

# Set the Terminal window size larger than its default!
sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=row,cols=column))

# Scottybot auth info
auth = {
	"event": "auth",
	"data": "<SCOTTYBOT_AUTH_CODE>"
}

server = {
	'host': '<TELNET_HOST>',
	'port': '<PORT>',
	'password': '<PASSWORD>',
	'username': '<PLAYER_NAME>'
}

# Path to Python Telnet Script - USE "/" as separator even on Windows
pyscript_path = './telnet.py'

# Random range of numbers
# less chance of an air drop whe using !item
num = random.randrange(0, 100)

# These can be changed but must match the commands you put in scottybot
commands = [
	'!item',
	'!tool',
	'!clothes',
	'!health',
	'!food',
	'!animal',
	'!quest',
	'!airdrop',
	'!weapon',
	'explosives',
	'!enemy',
	'!feral',
	'!screamer',
	'!horde'
]

###################################################################################
# ##########################   NO EDIT BELOW THIS LINE   ######################## #
###################################################################################

# 7 Days to Die Player Name
steam = server['username']

# Scotty Bot sub command
sub = {
	"event": "subscribe",
	"data": "commands"
}

'''
Items have variable amounts
weapons, parts, clothes, guests, books, buffs, debuffs, tools, animals, zombies = 1
food, health, explosives <= 10
ammunition, misc <= 20
'''
weapons = items.items['weapons']
explosives = items.items['explosives']
parts = items.items['parts']
tools = items.items['tools']
clothes = items.items['clothes']
health = items.items['health']
food = items.items['food']
books = items.items['books']
quests = items.items['quests']
misc = items.items['misc']

allitems = weapons + explosives + parts + tools + clothes + health + food + books + quests + misc

buffs = items.items['buffs']
debuffs = items.items['debuffs']
zombies = items.items['zombies']
animals = items.items['animals']


def on_message(ws, message):
	response = json.loads(message)
	data = []

	# check if the key event is in the response dict
	if 'event' in response:
		# if there store the value
		event = response['event']
		# check if the value is cmdran
		if event == 'cmdran':
			# if if is cmdran append the values to the data dict
			data.append(response['data']['rawcommand'])
			data.append(response['data']['username'])
			data.append(response['data']['userid'])
			#print(data)

			# Spawn Animal
			if data[0] == commands[5]:
				entity(animals)

			# Spawn Tool
			elif data[0] == commands[1]:
				give(tools)
				
			# Spawn Clothes
			elif data[0] == commands[2]:
				give(clothes)
				
			# Spawn Explosive
			elif data[0] == commands[9]:
				give(explosives)
				
			# Spawn Weapon
			elif data[0] == commands[8]:
				give(weapons)
				
			# Spawn Health
			elif data[0] == commands[3]:
				give(health)
				
			# Spawn Food
			elif data[0] == commands[4]:
				give(food)
				
			# Spawn Quest
			elif data[0] == commands[6]:
				give(quests)
				
			# Spawn Enemy
			elif data[0] == commands[10]:

				if num == 73:
					entity('spawnwanderinghorde')
				else:
					entity(zombies)

			# Spawn Item 
			elif data[0] == commands[0]:
				# **LESS CHANCE OF AIRDROP THAN BEFORE**
				if num == 73:
					give('spawnairdrop')
				else:
					give(allitems)

			# Spawn Horde
			elif data[0] == commands[13]:
				entity('spawnwanderinghorde')

			# Spawn Feral
			elif data[0] == commands[11]:
				entity('zombieFeral')

			# Spawn Screamer
			elif data[0] == commands[12]:
				entity('zombieScreamer')

			# Spawn Airdrop
			elif data[0] == commands[7]:
				give('spawnairdrop')


def give(enttype):
	key = random.randrange(0, len(enttype))
	if enttype == 'spawnairdrop':
		os.system('python {} {} {} {} 1 spawnairdrop'.format(pyscript_path, server['host'], server['port'], server['password']))
	else:
		os.system('python {} {} {} {} 4 give {} {} {}'.format(pyscript_path, server['host'], server['port'], server['password'], steam, enttype[key][0], enttype[key][1]))


def entity(enttype):
	key = random.randrange(0, len(enttype))
	print(enttype)
	if enttype == 'zombieFeral' or enttype == 'zombieScreamer':
		os.system('python {} {} {} {} 2 spawnentity {} {}'.format(pyscript_path, server['host'], server['port'], server['password'], server['username'], enttype))
	elif enttype == 'spawnwanderinghorde':
		os.system('python {} {} {} {} 2 spawnwanderinghorde'.format(pyscript_path, server['host'], server['port'], server['password']))
	elif enttype == zombies:
		os.system('python {} {} {} {} 2 spawnentity {} {}'.format(pyscript_path, server['host'], server['port'], server['password'], server['username'], enttype[key][0]))
	else:
		os.system('python {} {} {} {} 3 spawnentity {} {}'.format(pyscript_path, server['host'], server['port'], server['password'], server['username'], enttype[key][0]))


# if error is thrown
def on_error(ws, error):
	print(error)


# if connection is closed
def on_close(ws):
	print("### closed ###")


# open the connection
def on_open(ws):
	def run(*args):
		print('''
		                                                                                                      
  @@@@@@@@     @@@@@@@    @@@@@@   @@@ @@@   @@@@@@      @@@@@@@   @@@@@@      @@@@@@@   @@@  @@@@@@@@  
  @@@@@@@@     @@@@@@@@  @@@@@@@@  @@@ @@@  @@@@@@@      @@@@@@@  @@@@@@@@     @@@@@@@@  @@@  @@@@@@@@  
       @@!     @@!  @@@  @@!  @@@  @@! !@@  !@@            @@!    @@!  @@@     @@!  @@@  @@!  @@!       
      !@!      !@!  @!@  !@!  @!@  !@! @!!  !@!            !@!    !@!  @!@     !@!  @!@  !@!  !@!       
     @!!       @!@  !@!  @!@!@!@!   !@!@!   !!@@!!         @!!    @!@  !@!     @!@  !@!  !!@  @!!!:!    
    !!!        !@!  !!!  !!!@!!!!    @!!!    !!@!!!        !!!    !@!  !!!     !@!  !!!  !!!  !!!!!:    
   !!:         !!:  !!!  !!:  !!!    !!:         !:!       !!:    !!:  !!!     !!:  !!!  !!:  !!:       
  :!:          :!:  !:!  :!:  !:!    :!:        !:!        :!:    :!:  !:!     :!:  !:!  :!:  :!:       
   ::           :::: ::  ::   :::     ::    :::: ::         ::    ::::: ::      :::: ::   ::   :: ::::  
  : :          :: :  :    :   : :     :     :: : :          :      : :  :      :: :  :   :    : :: ::   
                                                                                                      
                                                                                                      
     @@@  @@@  @@@  @@@@@@@  @@@@@@@@  @@@@@@@    @@@@@@    @@@@@@@  @@@@@@@  @@@  @@@  @@@  @@@@@@@@   
     @@@  @@@@ @@@  @@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@  @@@  @@@  @@@  @@@@@@@@   
     @@!  @@!@!@@@    @@!    @@!       @@!  @@@  @@!  @@@  !@@         @@!    @@!  @@!  @@@  @@!        
     !@!  !@!!@!@!    !@!    !@!       !@!  @!@  !@!  @!@  !@!         !@!    !@!  !@!  @!@  !@!        
     !!@  @!@ !!@!    @!!    @!!!:!    @!@!!@!   @!@!@!@!  !@!         @!!    !!@  @!@  !@!  @!!!:!     
     !!!  !@!  !!!    !!!    !!!!!:    !!@!@!    !!!@!!!!  !!!         !!!    !!!  !@!  !!!  !!!!!:     
     !!:  !!:  !!!    !!:    !!:       !!: :!!   !!:  !!!  :!!         !!:    !!:  :!:  !!:  !!:        
     :!:  :!:  !:!    :!:    :!:       :!:  !:!  :!:  !:!  :!:         :!:    :!:   ::!!:!   :!:        
      ::   ::   ::     ::     :: ::::  ::   :::  ::   :::   ::: :::     ::     ::    ::::     :: ::::   
     :    ::    :      :     : :: ::    :   : :   :   : :   :: :: :     :     :       :      : :: ::  
   ''')
   
		time.sleep(3)
		
		print('''
                                                                                                      
                  ################################################################						
                  ##                                                            ##
                  ##                  TO CLOSE THIS APPLICATION:                ##
                  ##                                                            ##
                  ##                         ctrl + c                           ##
                  ##                            or                              ##
                  ##                 use the x in the upper right               ##
                  ##                                                            ##
                  ##                         BE AWARE:                          ##
                  ##                                                            ##
                  ##               Windows has a delay when closing             ##
                  ##                                                            ##
                  ##                                                            ##
                  ################################################################
						
                  ################################################################
                  ##                                                            ##
                  ##                         Credits:                           ##
                  ##                                                            ##
                  ##      AtomicYetiGaming ----- Python Scripts                 ##
                  ##                                                            ##
                  ##      AtomicYetiGaming_DC -- JS and NodeJS Scripts          ##
                  ##                                                            ##
                  ##      Bobofett ------------- Ideas, Testing, Support        ##
                  ##                                                            ##
                  ##      Coder5452 ------------ Headaches and Complaining      ##
                  ##                                                            ##
                  ################################################################
		''')
		# send the auth and sub data
		ws.send(json.dumps(auth))
		ws.send(json.dumps(sub))
		
		# keep sending to keep the connection open
		while True:
			time.sleep(10)
			ws.send(json.dumps(sub))

	thread.start_new_thread(run, ())

if __name__ == "__main__":
	# websocket.enableTrace(True)
	if len(sys.argv) < 2:
		host = "wss://api.scottybot.net/websocket/control"
	else:
		host = sys.argv[1]
	ws = websocket.WebSocketApp(host,
					on_message=on_message,
					on_error=on_error,
					on_close=on_close)
	ws.on_open = on_open

	ws.run_forever()
