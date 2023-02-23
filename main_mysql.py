
import datetime
import requests
import json
import pymysql



def get_time():
    # get system time

    now = datetime.datetime.now()
    pm_solartime = now.strftime("%Y-%m-%d %H:%M:%S")
    return (pm_solartime)

def get_token():
    headers = {"Content-Type": "application/json",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"}


    with open("C:\\Users\\Marek\\PycharmProjects\\pythonProject\\config.json") as jsonFile:
    #with open("config.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()

    appId = jsonObject['appId']

    data = open('apisol_pv_conf.json', 'r')

    response = requests.post(url + 'account/v1.0/token?appId=' + str(appId) + '&language=en&=', headers=headers,
                             data=data)
    r = response.json()

    access_token = r.get("access_token")
  #  refresh_token = r.get("refresh_token")

    token = open('C:\\Users\\Marek\\PycharmProjects\\pythonProject\\token.txt', 'w')
    token.write(str(access_token))
    token.close()
    return

def odczyt_tokena_z_pliku():
    #token =  open('token.txt', 'r')

    token = open("C:\\Users\\Marek\\PycharmProjects\\pythonProject\\token.txt", "r")
    #try:
    token = token.read()
    #finally:
    #token.close()
    return (token)


def zapytanie_o_wszystko():
    access_token = odczyt_tokena_z_pliku()
    headers1 = {"Authorization": "bearer " + access_token, "Content-Type": "application/json; charset=utf-8",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"}

    with open("C:\\Users\\Marek\\PycharmProjects\\pythonProject\\config.json") as jsonFile:
    #with open("config.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()

    deviceSn  = jsonObject['deviceSn']


    temp2 = str(deviceSn)


    appId = jsonObject['appId']

    response1 = requests.post(url + "device/v1.0/currentData?appId=" + str(appId) + "&language=en&=", headers=headers1, data='{"deviceSn":'+ '"'+deviceSn+'"}')
    global r1
    r1 = response1.json()

    return ()

###########################################################


global url
url = 'https://api.solarmanpv.com/'


zapytanie_o_wszystko()

#sprawdzenie czy token jest ok

valid_token = r1.get("success")
print(valid_token)
if valid_token != True:
    print ("Some Error. API server message: ",r1.get("msg"))
    print ("Obtainig the new token....")
    get_token()


print("Token OK. API server message: ", r1.get("msg"))
# odpowiedz z serwera api na temat autoryzacji, brak odpowiedzi znaczy ze ejst ok

zapytanie_o_wszystko()


# wyłuskanie napięć AC

acv1 = r1.get('dataList')[14].get('value')
facv1 = float(acv1)

acv2 = r1.get('dataList')[15].get('value')
facv2 = float(acv2)

acv3 = r1.get('dataList')[16].get('value')
facv3 = float(acv3)

# znalezienie najwyzeszej wartosci

tablica = []
tablica.append(facv1)
tablica.append(facv2)
tablica.append(facv3)

vacmax = max(tablica)
print('max voltage ', vacmax, 'V')

# get AC power

acpwr = r1.get('dataList')[21].get('value')

print(f"power {acpwr} W")

# wyłuskanie energii w danym dniu

energy = float(r1.get('dataList')[23].get('value'))

energy_kwh = str(energy)
print('energy ', energy, ' kWh')

# wyłuskanie temperatury modułu

tinv = r1.get('dataList')[27].get('value')
tinv = str(tinv)
print(f"temp {tinv} °C")

dc1_voltage = r1.get('dataList')[8].get('value')  # pobiera z jasona  napiecie str dc1
dc2_voltage = r1.get('dataList')[9].get('value')  # pobiera z jasona  napiecie str dc2

dc1_current = r1.get('dataList')[10].get('value')  # pobiera z jasona 12 prąd str dc1
dc2_current = r1.get('dataList')[11].get('value')  # pobiera z jasona 13 orąd str dc2

dc1_power = r1.get('dataList')[12].get('value')  # pobiera z jasona  moc str dc1
dc2_power = r1.get('dataList')[13].get('value')  # pobiera z jasona  moc str dc2

acv1_current = r1.get('dataList')[17].get('value')  # pobiera z jasona  prąd ac1
acv2_current = r1.get('dataList')[18].get('value')  # pobiera z jasona  prąd ac2
acv3_current = r1.get('dataList')[19].get('value')  # pobiera z jasona  prąd ac3

ac_freq = r1.get('dataList')[20].get('value')  # get frequency AC
print(f"AC Frequency {ac_freq} Hz")

module_temperature = r1.get('dataList')[28].get('value')  # get module temperature
print(f"Module temperature {module_temperature} °C")

insulation_imp_cath_gnd = r1.get('dataList')[36].get('value')  # get "Insulation Impedance- Cathode to ground"
print(f"Insulation Impedance- Cathode to ground {insulation_imp_cath_gnd} kΩ")

insulation_imp_PV1 = r1.get('dataList')[39].get('value')  # get "Insulation Impedance- Cathode to ground"
print(f"PV1 Insulation Impedance {insulation_imp_PV1} kΩ")

insulation_imp_PV2 = r1.get('dataList')[40].get('value')  # get "Insulation Impedance- Cathode to ground"
print(f"PV2 Insulation Impedance {insulation_imp_PV2} kΩ")

print(f"Voltage string1 = {dc1_voltage} V, Current DC1 = {dc1_current} A, POWER DC2 = {dc2_power} W")
print(f"Voltage string2 = {dc2_voltage} V, Current DC2 = {dc2_current} A, POWER DC2 = {dc2_power} W")

print(f"Voltage AC1 = {acv1} V, Current AC1 = {acv1_current} A")
print(f"Voltage AC2 = {acv2} V, Current AC2 = {acv2_current} A")
print(f"Voltage AC3 = {acv3} V, Current AC3 = {acv3_current} A")
################################################################################################

DataMysql = get_time()
print(DataMysql)

#'2022-11-04 22:21:36'

#tabela tworzenie
#CREATE TABLE Sofar_Base.`Sofar` (Id DOUBLE NOT NULL AUTO_INCREMENT, Date DATE NOT NULL , Time TIME NOT NULL , Energy FLOAT NOT NULL COMMENT 'kWh' , Power_AC FLOAT NOT NULL COMMENT 'kW' , Temperature FLOAT NOT NULL COMMENT 'C°' , Voltage_AC1 FLOAT NOT NULL COMMENT 'V', Voltage_AC2 FLOAT NOT NULL COMMENT 'V' , Voltage_AC3 FLOAT NOT NULL COMMENT 'V', Current_AC1 FLOAT NOT NULL COMMENT 'A' , Current_AC2 FLOAT NOT NULL COMMENT 'A', Current_AC3 FLOAT NOT NULL COMMENT 'A', Power_DC1 FLOAT NOT NULL COMMENT 'W', Power_DC2 FLOAT NOT NULL COMMENT 'W', Voltage_DC1 FLOAT NOT NULL COMMENT 'V' , Voltage_DC2 FLOAT NOT NULL COMMENT 'V' , Current_DC1 FLOAT NOT NULL COMMENT 'A' , Current_DC2 FLOAT NOT NULL COMMENT 'A',PRIMARY KEY (Id) ) ENGINE = InnoDB;

#INSERT INTO `Sofar`(`date`, `Energy`) VALUES ('23-02-01 12:00:00', '3.9')

sql = f"""INSERT INTO Sofar (date, Energy, Power_AC, Inverter_temperature, Voltage_AC1, Voltage_AC2, Voltage_AC3, Current_AC1, Current_AC2, Current_AC3, Power_DC1, Power_DC2, Voltage_DC1, Voltage_DC2, Current_DC1, Current_DC2, Ac_freq, Module_temperature, Insulation_imp_cath_gnd, Insulation_imp_PV1, Insulation_imp_PV2) VALUES\n 
('{DataMysql}', '{energy_kwh}','{acpwr}', '{tinv}', '{acv1}', '{acv2}', '{acv3}', '{acv1_current}','{acv2_current}','{acv3_current}', '{dc1_power}','{dc2_power}', '{dc1_voltage}','{dc2_voltage}', '{dc1_current}', '{dc2_current}', '{ac_freq}', '{module_temperature}', '{insulation_imp_cath_gnd}', '{insulation_imp_PV1}', '{insulation_imp_PV2}');"""

print(sql)

with open("C:\\Users\\Marek\\PycharmProjects\\pythonProject\\config.json") as jsonFile:
    # with open("config.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()


SQL_HOST = jsonObject["SQL_HOST"]
SQL_USER = jsonObject["SQL_USER"]
SQL_PASSWORD = jsonObject["SQL_PASSWORD"]
SQL_DATABASE= jsonObject["SQL_DATABASE"]

# Open database connection
db = pymysql.connect(host=SQL_HOST, user= SQL_USER, password= SQL_PASSWORD, database= SQL_DATABASE)

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print ("Database version : %s " % data)


try:
   # Execute the SQL command
   cursor.execute(sql)

   # Commit your changes in the database
   db.commit()

except:
   # Rollback in case there is any error
   db.rollback()

# disconnect from server
db.close()
