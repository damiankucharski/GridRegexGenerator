from regos import Data_Entry, RegexGenerator
import time
import re 
data = [{
		"id": 1,
		"modelId": 0,
		"inputData": "show inventory NAME: \"861\", DESCR: \"861 chassis, Hw Serial#: FCZ1639C4BY, Hw Revision: 1.0\" PID: CISCO861-K9 , VID: V02, SN: FCZ1639C4BY Ce-poz-wroc-r01-zec#",
		"selectedSubStrings": [{
				"start": 116,
				"end": 119
			}
		]
	}, {
		"id": 2,
		"modelId": 0,
		"inputData": "show inventory +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ INFO: Please use \"show license UDI\" to get serial number for licensing. +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ NAME: \"Chassis\", DESCR: \"Cisco C1111-8PLTEEA Chassis\" PID: C1111-8PLTEEA , VID: V02 , SN: FCZ2340C2VM NAME: \"Power Supply Module 0\", DESCR: \"External Power Supply Module\" PID: PWR-12V , VID: V01 , SN: JAB0929092D NAME: \"module 0\", DESCR: \"Cisco C1111-8PLTEEA Built-In NIM controller\" PID: C1111-8PLTEEA , VID: , SN: NAME: \"NIM subslot 0/0\", DESCR: \"Front Panel 2 port Gigabitethernet Module\" PID: C1111-2x1GE , VID: V01 , SN: NAME: \"NIM subslot 0/1\", DESCR: \"C1111-ES-8\" PID: C1111-ES-8 , VID: V01 , SN: NAME: \"NIM subslot 0/2\", DESCR: \"C1111-LTE Module\" PID: C1111-LTE , VID: V01 , SN: NAME: \"Modem 0 on Cellular0/2/0\", DESCR: \"Sierra Wireless EM7455/EM7430\" PID: EM7455/EM7430 , VID: 1.0 , SN: 356129071057068 NAME: \"module R0\", DESCR: \"Cisco C1111-8PLTEEA Route Processor\" PID: C1111-8PLTEEA , VID: V02 , SN: FOC23345GEQ NAME: \"module F0\", DESCR: \"Cisco C1111-8PLTEEA Forwarding Processor\" PID: C1111-8PLTEEA , VID: , SN: ce-poz-szczecin-r347-mcd#",
		"selectedSubStrings": [{
				"start": 311,
				"end": 314
			}, {
				"start": 422,
				"end": 425
			}, {
				"start": 540,
				"end": 541
			}, {
				"start": 647,
				"end": 650
			}, {
				"start": 725,
				"end": 728
			}, {
				"start": 808,
				"end": 811
			}, {
				"start": 917,
				"end": 920
			}, {
				"start": 1033,
				"end": 1036
			}, {
				"start": 1149,
				"end": 1150
			}
		]
	}, {
		"id": 3,
		"modelId": 0,
		"inputData": "show inventory NAME: \"881\", DESCR: \"881 chassis, Hw Serial#: FCZ1502C4MY, Hw Revision: 1.0\" PID: CISCO881-K9 , VID: V01 , SN: FCZ1502C4MY ce-szc-przeclaw-stena-r01#",
		"selectedSubStrings": [{
				"start": 116,
				"end": 119
			}
		]
	}, {
		"id": 4,
		"modelId": 0,
		"inputData": "show inventory +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ INFO: Please use \"show license UDI\" to get serial number for licensing. +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ NAME: \"Chassis\", DESCR: \"Cisco C1111-4P Chassis\" PID: C1111-4P , VID: V01 , SN: FCZ2403C2V8 NAME: \"Power Supply Module 0\", DESCR: \"External Power Supply Module\" PID: PWR-12V , VID: V01 , SN: JAB0929092D NAME: \"module 0\", DESCR: \"Cisco C1111-4P Built-In NIM controller\" PID: C1111-4P , VID: , SN: NAME: \"NIM subslot 0/0\", DESCR: \"Front Panel 2 port Gigabitethernet Module\" PID: C1111-2x1GE , VID: V01 , SN: NAME: \"NIM subslot 0/1\", DESCR: \"C1111-ES-4\" PID: C1111-ES-4 , VID: V01 , SN: NAME: \"module R0\", DESCR: \"Cisco C1111-4P Route Processor\" PID: C1111-4P , VID: V01 , SN: FOC23510DC1 NAME: \"module F0\", DESCR: \"Cisco C1111-4P Forwarding Processor\" PID: C1111-4P , VID: , SN: ce-waw-pawia-r01-transition#",
		"selectedSubStrings": [{
				"start": 301,
				"end": 304
			}, {
				"start": 412,
				"end": 415
			}, {
				"start": 520,
				"end": 521
			}, {
				"start": 627,
				"end": 630
			}, {
				"start": 705,
				"end": 708
			}, {
				"start": 795,
				"end": 798
			}, {
				"start": 901,
				"end": 902
			}
		]
	}, {
		"id": 5,
		"modelId": 0,
		"inputData": "show inventory NAME: \"891\", DESCR: \"891 chassis, Hw Serial#: FCZ180590ES, Hw Revision: 1.0\" PID: CISCO891-K9 , VID: V02, SN: FCZ180590ES ce-waw-sofia-r13-antalis#",
		"selectedSubStrings": [{
				"start": 116,
				"end": 119
			}
		]
	}
]
data = [{

            "inputData" : "show interface description\nInterface                      Status         Protocol Description\nFa0                            down           down     \nFa1                            up             up       \nFa2                            down           down     \nFa3                            down           down     \nFa4                            up             up       WAN\nLo0                            up             up       \nVl1                            up             up       \nCe-poz-wroc-r01-zec#\n\n",
            "selectedSubStrings" : [{"start": 139, "end": 149}, {"start": 195, "end": 205}, {"start": 251, "end": 261}, {"start": 307, "end": 317}, {"start": 363, "end": 376}, {"start": 422, "end": 432}, {"start": 478, "end": 488}]
}
]

generator = RegexGenerator()
generator.parse_data(data, alternative_keys=['inputData', 'selectedSubStrings'])
start = time.time()
regex = generator.evolve(ignore_mid=False)#, mid = r".*?[\\n]")
spans = [s.group(1) for s in re.finditer(regex, data[0]['inputData'])]
print(time.time() - start)
print(regex)
print(spans)
