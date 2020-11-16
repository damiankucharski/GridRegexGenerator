from regos import Data_Entry, RegexGenerator
import time

data = [{

            "string" : "show inventory +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ INFO: Please use \"show license UDI\" to get serial number for licensing. +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ NAME: \"Chassis\", DESCR: \"Cisco C1111-8PLTEEA Chassis\" PID: C1111-8PLTEEA , VID: V02 , SN: FCZ2340C2VM NAME: \"Power Supply Module 0\", DESCR: \"External Power Supply Module\" PID: PWR-12V , VID: V01 , SN: JAB0929092D NAME: \"module 0\", DESCR: \"Cisco C1111-8PLTEEA Built-In NIM controller\" PID: C1111-8PLTEEA , VID: , SN: NAME: \"NIM subslot 0/0\", DESCR: \"Front Panel 2 port Gigabitethernet Module\" PID: C1111-2x1GE , VID: V01 , SN: NAME: \"NIM subslot 0/1\", DESCR: \"C1111-ES-8\" PID: C1111-ES-8 , VID: V01 , SN: NAME: \"NIM subslot 0/2\", DESCR: \"C1111-LTE Module\" PID: C1111-LTE , VID: V01 , SN: NAME: \"Modem 0 on Cellular0/2/0\", DESCR: \"Sierra Wireless EM7455/EM7430\" PID: EM7455/EM7430 , VID: 1.0 , SN: 356129071057068 NAME: \"module R0\", DESCR: \"Cisco C1111-8PLTEEA Route Processor\" PID: C1111-8PLTEEA , VID: V02 , SN: FOC23345GEQ NAME: \"module F0\", DESCR: \"Cisco C1111-8PLTEEA Forwarding Processor\" PID: C1111-8PLTEEA , VID: , SN: ce-poz-szczecin-r347-mcd#",
            "selections" : [{
				"start": 255,
				"end": 284
			}, {
				"start": 371,
				"end": 401
			}, {
				"start": 469,
				"end": 514
			}, {
				"start": 579,
				"end": 622
			}, {
				"start": 689,
				"end": 701
			}, {
				"start": 767,
				"end": 785
			}, {
				"start": 859,
				"end": 890
			}, {
				"start": 969,
				"end": 1006
			}, {
				"start": 1081,
				"end": 1123
			}
		]
}
]


generator = RegexGenerator()
generator.parse_data(data)
start = time.time()
regex = generator.evolve(True)
print(time.time() - start)
print(regex)