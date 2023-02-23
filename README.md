English below.

-----------------------

**Polski**

Podgląd pod adresem Grafana http://poczta.duckdns.org:3000/d/eVcK7Wzgk/with-time?orgId=1&refresh=5m&from=now-24h&to=now

Jest to projekt który pobiera dane, dotyczące produkcji i parametrów pracy systemu fotowoltaicznego wysłane z falownika SofarSolar na serwer solarman.com za pomocą interfejsu API. Dane są przesyłane do lokalnego serwera mysql. Skrypt jest napisany w Pythonie i wywoływany za pomocą mechanizmu Cron w interwałach co 5 minut.

Pobrane dane w formacie json po ich obróbce zapisywane są na lokalnym dysku twardym SSD w bazie danych Mariadb (Mysql) która jest postawiona na Raspberry pi3 (niskie zużycie energii elektrycznej). Na tej samej maszynie uruchomiony jest serwer Grafana. Pobiera on rekordy poprzez zapytania Mysql z lokalnego serwera Mariadb i wyświetla w panelu Grafany. Całość jest udostępniona pod podanym adresem w celu podglądu bez konieczności logowania się do panelu.

Kontrolki Grafany są w pełni konfigurowalne praca nad nią nie zakończyła się. Planuje dodać inne kontrolki takie jak uzyski miesięczne roczne i całościowe. Do tego muszę dopisać program który uzyska dane archiwalne z innego serwisu pvoutput.org gdzie od 2017r dane były wysyłane.

W planie mam jeszcze dorobienie pobierania danych bezpośrednio z interfejsu modbus (Tcpip_Modbus) z falownika (tak jak to robię obecnie z pompą ciepła). Będę do tego dążył ze względu na pojawiające się trudności w uzyskaniu dostępu do korzystania z serwera API na solarman.com. Administracja serwera potrafi odrzucić wniosek o dostęp do API bez uzasadnienia. Pomimo dostępu do serwera nie można pobrać szczegółowych danych historycznych. Historycznie dostępne są jedynie dane z pełnej doby, miesiąca, roku pomimo że na serwer są wysyłane dane szczegółowe co około 3 minuty. Czytając lokalnie po modbusie będzie można uzyskać podgląd praktycznie online.

Kilka słów do konfiguracji.

Program żeby działać potrzebuje:

1. Działającego serwera mysql z dodaną  bazą i tabelą 

jak w poniższym zapytaniu. Zapytanie to jest zaczerpnięte z mojego programu i przesyła uzyskane dane do tabeli na serwerze mysql.


sql = f"""INSERT INTO Sofar (date, Energy, Power_AC, Inverter_temperature, Voltage_AC1, Voltage_AC2, Voltage_AC3,\n
 Current_AC1, Current_AC2, Current_AC3, Power_DC1, Power_DC2, Voltage_DC1, Voltage_DC2, Current_DC1, Current_DC2, \n
 Ac_freq, Module_temperature, Insulation_imp_cath_gnd, Insulation_imp_PV1, Insulation_imp_PV2) VALUES\n 
 
('{DataMysql}', '{energy_kwh}','{acpwr}', '{tinv}', '{acv1}', '{acv2}', '{acv3}', '{acv1_current}','{acv2_current}',\n
'{acv3_current}', '{dc1_power}','{dc2_power}', '{dc1_voltage}','{dc2_voltage}', '{dc1_current}', '{dc2_current}', \n
'{ac_freq}', '{module_temperature}', '{insulation_imp_cath_gnd}', '{insulation_imp_PV1}', '{insulation_imp_PV2}');"""

Prawdopodobnie jest możliwe wygenerowanie tabeli z mojego panelu phpmadmin 


2. Posiadania konta na Solarman.COM  z dostepem do usług API. Należy zawnioskować do administracji serwera o nadanie takiego dostępu. Otrzymamy wtedy dokunetacje api oraz dane niezbedne do logowania sie na serwer za pomoca API. 

3. Co do Grafany to postawiony serwer GRafany z podpiętą wcześniej wspomnianą bazą mysql i obecnym dashboardem wraz z zapy taniami. Prawdopodobnie da się wygenerować moj obecny dashboard.


4. Własną konfiguracje należy wpisać do plików config.json oraz apisol_pv_conf.json. Z  oczywistych powodów dane w tych plikach nie wskazują na moją instalacje należy podać swoje dane nie zmieniając składni i formatu pliku. W programie ustawić scieżkę dostępu do pliku na swoim dysku. Jeśli plik znajduję sie w katalogu projektu to wystarczy podać sama nazwę pliku bez pełnej ścieżki. 

5. Podczas pierwszego zapytania do Api generowany jest token i zapisywany do pliku token.txt. Token ma swój czas ważności i jeśli się przeterminuje jest  wysyłane żądanie nowego tokena przy czym stary jest nadpisywany. Podczas zwykłych zapytań hasło nie jest przesyłane, uwierzytelninie obywa się za pomocą tokena "na okaziciela" tzw. bearer token.


---------------------------------------------
**English**

View at Grafana http://poczta.duckdns.org:3000/d/eVcK7Wzgk/with-time?orgId=1&refresh=5m&from=now-24h&to=now

It is a project that downloads data on the production and operating parameters of the photovoltaic system sent from the SofarSolar inverter to the solarman.com server using the API interface. The data is sent to the local mysql server. The script is written in Python and invoked using the cron mechanism at intervals of 5 minutes.

The downloaded data in json format after processing are saved on the local SSD hard drive in the Mariadb (Mysql) database, which is installed on the Raspberry pi3 (low power consumption). The Grafana server is running on the same machine. It retrieves records via Mysql queries from a local Mariadb server and displays them in the Grafany panel. The whole thing is available at the given address for viewing without having to log in to the panel.

Grafana controls are fully configurable, work on it is not over. It plans to add other controls such as monthly, annual and total yields. To this I have to add a program that will obtain archival data from another website pvoutput.org where data has been sent since 2017.

I also plan to download data directly from the modbus interface (Tcpip_Modbus) from the inverter (as I am currently doing with the heat pump). I will strive for this due to the difficulties in obtaining access to using the API server on solarman.com. The server administration can reject an API access request without justification. Despite access to the server, detailed historical data cannot be downloaded. Historically, only full day, month and year data are available, despite the fact that detailed data is sent to the server approximately every 3 minutes. By reading locally on the modbus, you will be able to get a virtually online preview.

A few words to configure.

To run the program needs:

1. A working mysql server with added database and table

as in the query below. This query is taken from my program and sends the obtained data to a table on mysql server.


sql = f"""INSERT INTO Sofar (date, Energy, Power_AC, Inverter_temperature, Voltage_AC1, Voltage_AC2, Voltage_AC3,\n
 Current_AC1, Current_AC2, Current_AC3, Power_DC1, Power_DC2, Voltage_DC1, Voltage_DC2, Current_DC1, Current_DC2, \n
 Ac_freq, Module_temperature, Insulation_imp_cath_gnd, Insulation_imp_PV1, Insulation_imp_PV2) VALUES\n 
 
('{DataMysql}', '{energy_kwh}','{acpwr}', '{tinv}', '{acv1}', '{acv2}', '{acv3}', '{acv1_current}','{acv2_current}',\n
'{acv3_current}', '{dc1_power}','{dc2_power}', '{dc1_voltage}','{dc2_voltage}', '{dc1_current}', '{dc2_current}', \n
'{ac_freq}', '{module_temperature}', '{insulation_imp_cath_gnd}', '{insulation_imp_PV1}', '{insulation_imp_PV2}');"""

It's probably possible to generate a table from my phpmadmin panel


2. Having an account on Solarman.COM with access to API services. You should apply to the server administration to grant such access. Then we will receive api documentation and data necessary to log on to the server using the API.

3. As for Grafana, it's a GRAFany server with the previously mentioned mysql database and the current dashboard with queries. It's probably possible to generate my current dashboard.


4. Your own configuration should be entered into the config.json and apisol_pv_conf.json files. For obvious reasons, the data in these files do not indicate my installation, please enter your data without changing the syntax and file format. In the program, set the path to the file on your disk. If the file is in the project directory, it is enough to specify the file name without the full path.

5. During the first request to the Api, a token is generated and saved to the token.txt file. The token has its validity period and if it expires, a request for a new token is sent and the old one is overwritten. During regular queries, the password is not sent, authentication is done using a bearer token.
