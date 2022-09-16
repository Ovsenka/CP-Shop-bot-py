from db import db

CPUs = {}
MBs = {}
VCs = {}
RAMs = {}
PSs = {}

categ_nums = {"cpu":1, "mb":2, "vc":3, "ram":4, "ps":5}
categ_names = {1:"cpu", 2:"mb", 3:"vc", 4:"ram", 5:"ps"}

parts = db.get_all_parts()
id_first_cpu = 0

for part in parts:
   if part[1] == 1:
      CPUs[part[0]] = [part[2], part[3], part[4], part[5], part[6] ]
   if part[1] == 2:
      MBs[part[0]] = [ part[2], part[3], part[4], part[5], part[6] ]
   if part[1] == 3:
      VCs[part[0]] = [ part[2], part[3], part[4], part[5], part[6] ]
   if part[1] == 4:
      RAMs[part[0]] = [ part[2], part[3], part[4], part[5], part[6] ]
   if part[1] == 5:
      PSs[part[0]] = [ part[2], part[3], part[4], part[5], part[6] ]

id_first_cpu = list(CPUs.keys())[0]
id_first_mb = list(MBs.keys())[0]
id_first_vc = list(VCs.keys())[0]
id_first_ram = list(RAMs.keys())[0]
id_first_ps = list(PSs.keys())[0]
