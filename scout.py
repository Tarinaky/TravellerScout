import random

def sum_over(a):
    y = 0
    for x in a:
        y += x
    return y    


class System:
    def __init__(self):
        self.name = "None"
        self.shadow = 0
        self.bodies = 0
        self.gas_present = False
        self.inner_bodies = 0
        self.goldilocks = 0
        self.outer_bodies = 0
        self.inner_body_list = []
        self.goldilocks_body_list = []
        self.outer_body_list = []

    def generate(self, system_name, seed=None):
        self.name = system_name
        
        prng = random.Random(seed)
        d = lambda x: prng.randint(1,x)
        

        self.shadow = d(6)
        self.bodies = d(6) + self.shadow
        if d(6)+d(6) >= 10:
            self.gas_present = False
        else:
            self.gas_present = True

        (a,b) = (d(6),d(6) )
        if a > b:
            (a,b) = (b,a)

        self.inner_bodies = min(a,self.bodies)
        self.goldilocks = max(b - a - 1, 0)
        self.outer_bodies = max(self.bodies - b + 1, 0)


        #Add planet generation here.
        current_body = 1
        gas_giant_placed = False
        for i in range(self.inner_bodies):
            (a,b) = (d(6), d(6) )
            if a == b == 1 and self.gas_present:
                body = Body(self.name+" "+roman_numeral(current_body), "Gas Giant")
                self.inner_body_list.append(body)
                gas_giant_placed = True
            else:    
                type_die = min(a, b)
                body = Body(self.name+" "+roman_numeral(current_body), get_type(type_die, prng) )
                self.inner_body_list.append(body)
            current_body += 1
        for i in range(self.goldilocks):
            (a,b) = (d(6), d(6) )
            if a == b and self.gas_present:
                body = Body(self.name+" "+roman_numeral(current_body), "Gas Giant")
                self.goldilocks_body_list.append(body)
                gas_giant_placed = True
            else:
                type_die = min(a, b)
                body = Body(self.name+" "+roman_numeral(current_body), get_type(type_die, prng) )
                self.goldilocks_body_list.append(body)
            current_body += 1
        for i in range(self.outer_bodies):
            (a,b) = (d(6), d(6) )
            if (a == b or a+b > current_body/2) and self.gas_present:
                body = Body(self.name+" "+roman_numeral(current_body), "Gas Giant")
                self.outer_body_list.append(body)
                gas_giant_placed = True
            else:
                type_die = max(a, b)
                body = Body(self.name+" "+roman_numeral(current_body), get_type(type_die, prng) )
            current_body += 1
        
        if gas_giant_placed == False and self.gas_present == True:
            body = Body(self.name+" "+roman_numeral(current_body), "Gas Giant")
            self.outer_body_list.append(body)
            self.outer_bodies += 1
            self.bodies += 1
        
        
        capital = None
        for body in self.inner_body_list:
            body.generate("inner", prng)
            if capital == None or body.pop > capital.pop:
                capital = body
        for body in self.goldilocks_body_list:
            body.generate("goldilocks", prng)
            if capital == None or body.pop > capital.pop:
                capital = body
        for body in self.outer_body_list:
            body.generate("outer", prng)
            if capital == None or body.pop > capital.pop:
                capital = body

            
                




        return self

  
    def __str__(self):
        string = "="+self.name + "=\n"
        string += "Jump Shadow: " + str(self.shadow) + "\n"
        string += "Planets: " + str(self.bodies) + "\n"
        string += "\tInner Bodies: " + str(self.inner_bodies) + "\n"
        string += "\tGoldilocks Zone: " + str(self.goldilocks) + "\n"
        string += "\tOuter Bodies: " + str(self.outer_bodies) + "\n"
        string += "\n"
        string += "-Inner Region\n"
        for body in self.inner_body_list:
            string += body.__str__()
            string += "\n"
        string += "-Goldilocks Region\n"
        for body in self.goldilocks_body_list:
            string += body.__str__()
            string += "\n"
        string += "-Outer Region\n"    
        for body in self.outer_body_list:
            string += body.__str__()
            string += "\n"
            
        return string+"\n"

class Body:
    def __init__(self, name = "None", body_type="None"):
        self.name = name
        self.body_type = body_type
        self.size = 0
        self.atmos = 0
        self.temp = 0
        self.hydro = 0
        self.pop = 0
        self.government = 0
        self.law = 0

        self.gravity = 0
        self.pressure = 0
        self.hydroPercent = 0
        self.popEstimated = 0
        self.tempKelvin = [0,0]

        self.codes = []

        self.is_capital = False
        self.starport = 'X'
        
    def generate(self, region, prng): 
        d = lambda x: prng.randint(1,x)

        #If gas giant, do nothing.
        if self.body_type == "Gas Giant":
            return
        (size_bounds_min, size_bounds_max) = body_type_list[self.body_type]
        #Size
        while True:
            sizeUWP = d(6)+d(6)-2
            if sizeUWP >= size_bounds_min and sizeUWP <= size_bounds_max:
                self.size = sizeUWP
                break
        gravity = {-1:0, 0:0, 1:0.05, 2:0.15, 3:0.25, 4:0.35, 5:0.45, 6:0.7, 7:0.9, 8:1.0, 9:1.25, 10:1.4, 11:2}    
        (a,b) = (gravity[self.size-1], gravity[self.size+1])
        self.gravity = prng.randint(a*100,b*100) / 100.0
        
        
        self.atmos = max(0, d(6) + d(6) - 7 + self.size)
        if self.size in range(2):
            self.atmos = 0
        if self.size in [3,4] and self.atmos in [0,1,2]:
            self.atmos = 0
        if self.size in [3,4] and self.atmos in [3,4,5]:
            self.atmos = 1
        if self.size in [3,4] and self.atmos >= 6:
            self.atmos = 10
                



        pressures = {0:(0.0, 0.0, 0), 1:(0.01, 0.09, 0.05), 2:(0.1, 0.42, 0.21), 3:(0.1, 0.42, 0.21), 4:(0.43, 0.7, 0.58), 5:(0.43, 0.7, 0.58), 6:(0.71, 1.49, 1), 7:(0.71, 1.49,1), 8:(1.5, 2.49, 2), 9:(1.5, 2.49, 2), 10:(0, 3, 1), 11:(0,3, 1), 12:(0,3, 1), 13:(2.5, 100, 2.5), 14:(0,0.5, 0.5), 15:(0,3, 1)}
    
        (a,b, c) = pressures[self.atmos]
        if a == b:
            self.pressure = 0
        else:    
            self.pressure = prng.triangular(a,b,c)


        tempUWP = d(6) + d(6)
        atmos_mods = {0:0, 1:0, 2:-2, 3:-2, 4:-1, 5:-1, 6:0, 7:0, 8:+1, 9:+1, 10:+2, 11:+6, 12:+6, 13:+2, 14:-1, 15:+2}
        tempUWP += atmos_mods[self.atmos]
        if region == "inner":
            tempUWP += 4
        if region == "outer":
            tempUWP -= 4

        self.temp = min(12, max(0, tempUWP) )
        temperatures = {-1:5, 0:5, 1:5, 2:5, 3:222, 4:222, 5:273, 6:273, 7:273, 8:273, 9:273, 10:304, 11:304, 12:354, 13:4500, 14:4500}
        (a,b) = (temperatures[self.temp], temperatures[self.temp+1])
        if self.atmos in [0,1]:
            (a,b) = (temperatures[self.temp-1],temperatures[self.temp+2])

        self.tempKelvin = sorted([prng.randint(a,b), prng.randint(a,b)])

        hydroUWP = d(6) + d(6) - 7 + self.size
        if self.temp >= 12:
            hydroUWP -= 4
        if self.temp >= 10:
            hydroUWP -= 2
        if self.atmos in [0,1,10,11,12]:
            hydroUWP -= 4
        if self.size in [0,1]:
            hydroUWP == 0
        if self.size in [3,4] and self.atmos == 10:
            hydroUWP -= 6
        if self.atmos in [0,1]:
            hydroUWP -= 6
        if self.atmos in [2,3,11,12]:    
            hydroUWP -= 4

        self.hydro = min(10, max(0, hydroUWP) )   
        

        self.hydroPercent = min(100, max(0, self.hydro * 10 - 5 + prng.randint(0,10) ) )
        if self.hydro == 0:
            self.hydroPercent = 0

        if self.atmos in [11, 12] or self.tempKelvin[1] >= 1400:
            self.pop = 0
            self.government = 0
            self.law = 0
        else:    

            a = [d(6), d(6), d(6), d(6)]
            a.remove(max(a) )
            a.remove(max(a) )
            popUWP = a[0] + a[1]
            print 
            
            if self.size in [0,1,2]:
                popUWP -= 1
            if self.size == 10:
                popUWP -=1
            if not self.atmos in [5,6,8]:
                popUWP -= 1
            if self.atmos in [5,6,8]:
                popUWP += 1

            self.pop = popUWP
            self.popEstimated = prng.randint(int(10**(self.pop-1)), int(10**(self.pop) -1))
            
            a = [d(6), d(6), d(6)]
            a.remove(max(a) )
            self.government = min(13, max(0, a[0] + a[1] - 7 + self.pop) )

            self.law = min(9,max(0, d(6) + d(6) - 7 + self.government) )


            starport = min(11,max(2,d(6) + d(6) -7 + self.pop) )
            self.starport = {2:'X', 3:'E', 4:'E', 5:'D', 6:'D', 7:'C', 8:'C', 9:'B', 10:'B', 11:'A'}[starport]

        if self.atmos in [4,5,6,7,8,9] and self.hydro in [4,5,6,7,8] and self.pop in [5,6,7]:
            self.codes.append('Ag')
        if self.size == 0 and self.atmos == 0 and self.hydro == 0:
            self.codes.append('As')
        if self.pop == 0:
            self.codes.append('Ba')
        if self.atmos >= 2 and self.hydro == 0:
            self.codes.append("De")
        if self.atmos >= 10 and self.hydro >= 1:
            self.codes.append("Fl")
        if self.size >= 5 and self.atmos in [4,5,6,7,8,9] and self.hydro in [4,5,6,7,8]:
            self.codes.append('Ga')
        if self.pop >= 9:
            self.codes.append('Hi')
        if self.atmos in [0,1] and self.hydro >= 1:
            self.codes.append('Ic')
        if self.atmos in [0,1,2,4,7,9] and self.pop >= 9:
            self.codes.append('In')
        if self.pop in [1,2,3]:
            self.codes.append('Lo')
        if self.atmos in [0,1,2,3] and self.hydro in [0,1,2,3] and self.pop >= 6:
            self.codes.append('Na')
        if self.pop in [4,5,6]:
            self.codes.append("Ni")
        if self.atmos in [2,3,4,5] and self.hydro in [0,1,2,3]:
            self.codes.append('Po')
        if self.atmos in [6,8] and self.pop in [6,7,8]:
            self.codes.append("Ri")
        if self.atmos == 0:
            self.codes.append("Va")
        if self.hydro == 10:
            self.codes.append("Wa")



    @property
    def uwp(self):
        def toHex(n):
            if n < 10:
                return str(n)
            elif n > 15:
                return 'F'
            else:
                return {10:'A', 11:'B', 12:'C', 13:'D', 14:'E', 15:'F'}[n]
        string = toHex(self.size)+toHex(self.atmos)+toHex(self.hydro)+toHex(self.pop)+toHex(self.government)+toHex(self.law)
        for code in self.codes:
            string += " "+code
        return string    




    def __str__(self):
        if self.body_type == "Gas Giant":
            return self.name + " - "+ self.body_type + "\n"

        string = self.name+" - " + self.body_type + " UWP" + self.uwp + "\n"
        string += "\tGravity: "+str(self.gravity) + " g\n"
        atmosphere_type = {0:"None", 1:"Trace", 2:"Very Thin, Tainted", 3:"Very Thin", 4:"Thin, Tainted", 5:"Thin", 6:"Standard", 7:"Standard, Tainted", 8:"Dense", 9:"Dense, Tainted", 10:"Exotic", 11:"Corrosive", 12:"Insidious", 13:"Dense, High", 14:"Thin, Low", 15:"Unusual"}[self.atmos]
        string += "\tPressure (at sea-level or lowest elevation): "+str(int(self.pressure*100))+" kPa ("+atmosphere_type+")\n"
        string += "\tEstimated Temperature Range: " + str(self.tempKelvin[0])+"->"+str(self.tempKelvin[1])+" K\n"
        string += "\tLiquid as percentage of surface (not always water): " + str(self.hydroPercent)+"%\n"
        if self.pop == 0:
            string += "\tUninhabited\n"
        else:
            starport_services = {'A': "Shipyard (all), refined fuel, Beanstalk, Verne gun, regular spaceplanes, SSTOs and cargo rockets", 'B':"Shipyard (spacecraft), refined fuel, Verne gun, passenger spaceplanes, SSTOs and cargo rockets", 'C':"Shipyard (smallcraft only), unrefined fuel, Passenger spaceplanes, SSTOs, cargo rockets", 'D':"Limited Repair, chartered SSTO and cargo rockets available", 'E': "Frontier services, chartered rockets", 'X':"No starport"}
            string += "\tStarport Services: " + starport_services[self.starport] + ".\n"
            string += "\tKnown Population: "+str(self.popEstimated) + "\n"
            government_type = {0:"None", 1:"Company town", 2:"Participating democracy", 3:"Self-perpetuating oligarchy", 4:"Representative democracy", 5:"Feudal technocracy", 6:"Captive government", 7:"Balkanisation", 8:"Civil service bureaucracy", 9:"Impersonal buraucracy", 10:"Charismatic dictator", 11:"Non-charismatic leader", 12:"Charismatic oligarchy", 13:"Religious dictatorship"}[self.government]    
            string += "\tGovernance: "+government_type+"\n"

            prohibited_weapons = ["Poison gas, explosives, WMDs. ", "Portable energy weapons. ", "Heavy weapons. ", "Assault and Machinegun weapons. ", "Concealed carry. ", "All firearms excluding shotguns and less-lethal (ie TASER). ", "All firearms excluding less-lethal (ie TASER). ", "All bladed weapons, all firearms including less-lethal. ", "Any weapon. ",""]
            prohibited_drugs = ["Highly dangerous narcotics. ", "Highly addictive narcotics. ", "Combat drugs. ", "Addictive narcotics. ", "Anagathics. ", "Fast and Slow drugs. ", "All narcotics. ", "Medicinal drugs. ", "All drugs. ",""]
            prohibited_information = ["Intellect programs. ", "Agent programs. ", "Intrusion programs. ", "Security programs. ", "Expert programs. ", "News and media not yet state-sanctioned. ", "Most liturature, offworld knowledge. ", "Computers, personal media", "All knowledge. ",""]
            prohibited_tech = ["Dangerous technology. ", "Alien technology. ", "TL15. ", "TL13. ", "TL11. ", "TL9. ", "TL7. ", "TL5. ", "TL3. ",""]
            prohibited_travel = ["Visitors must make radio contact before landing. ", "Visitors must report crew, cargo and passenger manifests. ", "Landing at unsanctioned sites. ", "Landing only permitted at starport. ", "Citizens must register offworld travel, visitors must register all business. ", "Visitors discouraged, unsupervised contact with citizens forbidden. ", "Cizitens may not leave planet, visitors restricted to starport. ", "Landing permitted only to government agents. ", "Strictly no offworlders. ",""]
            contraband_by_government = {0:[], 1:[prohibited_weapons, prohibited_drugs, prohibited_travel], 2:[prohibited_drugs], 3:[prohibited_tech, prohibited_weapons, prohibited_travel], 4:[prohibited_drugs, prohibited_weapons], 5:[prohibited_tech, prohibited_weapons, prohibited_information], 6:[prohibited_weapons, prohibited_tech, prohibited_travel], 7:[], 8:[prohibited_drugs, prohibited_weapons], 9:[prohibited_tech, prohibited_weapons, prohibited_drugs, prohibited_travel], 10:[], 11:[prohibited_weapons, prohibited_tech, prohibited_information], 12:[prohibited_weapons], 13:[]}

            if self.law > 0 and contraband_by_government[self.government] != []:
                contraband = ""
                for i in contraband_by_government[self.government]:
                    assert self.law > 0
                    assert i != []
                    assert self.law < len(i)
                    contraband += i[self.law-1]
            else:
                contraband = "none"

            string += "Notable restrictions: "+contraband+"\n"    

        return string


body_type_list = {"Gas Giant":None, "Small Rock":(1, 3), "Large Rock":(4, 15), "Dwarf Planet":(0, 1), "Belt":(0, 1), "Small Ice":(2,4), "Large Ice":(5,15)}
body_type_table = {1:"Small Rock", 2:"Large Rock", 3:"X", 4:"Small Ice", 5:"Large Ice", 6:"X"}

def get_type(n,prng=random.random):
    if body_type_table[n] == "X":
        if prng.choice([True,False]):
            return "Dwarf Planet"
        else:
            return "Belt"
    else:
        return body_type_table[n]

def roman_numeral(n):
    X = IX = V = IV = I = 0
    #Tens
    X = n / 10
    n -= X*10
    #IXs
    if n % 10 == 9:
        IX = 1
        n -= 9
    #Fives
    V = n / 5
    n -= V*5
    #IVs
    if n % 5 == 4:
        IV = 1
        n -= 4
    #Is
    I = n
    #Build string
    string = ""
    for i in range(X):
        string += 'X'
    for i in range(IX):
        string += 'IX'
    for i in range(V):
        string += 'V'
    for i in range (IV):
        string += 'IV'
    for i in range(I):
        string += 'I'
    return string    

if __name__ == '__main__':
    print System().generate("Test System", 0xDEADBEEF)
    print System().generate("Test System 1", 0xDEADBEEF1)
    print System().generate("Test System 2", 0xDEADBEEF2)
    print System().generate("Test System 3", 0xDEADBEEF3)
    print System().generate("Test System 4", 0xDEADBEEF4)

    
