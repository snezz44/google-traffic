
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import mysql.connector
#dane do połączenia z bazą danych (jest postawiona lokalnie)
host = '127.0.0.1'
user = 'admin'
password = 'GoogleTraffic'
database = 'Googletraffic'
#słownik z zapytaniami, później po nim iterujemy
queries ={
            'Pasaż Grunwaldzki-Bielany': "SELECT * FROM Googletraffic.traffic where nazwa_trasy like 'BIELPASAZ'",
            'Brama Grabiszyńska-DORD' : "SELECT * FROM Googletraffic.traffic where nazwa_trasy like 'BG-DORD'",
            'Fashion Outlet-Most Grunwaldzki' : "SELECT * FROM Googletraffic.traffic where nazwa_trasy like 'WFO-MG'",
            'ulica Zwycięska' : "SELECT * FROM Googletraffic.traffic where nazwa_trasy like 'ZWYCIESKA'",
            'ZOO-UWR' : "SELECT * FROM Googletraffic.traffic where nazwa_trasy like 'ZOO-UWR'"
        }
#wykonanie zapytania
def execute_query(host, user, password, database, query):
    try:
        #połączenie z bazą
        connection = mysql.connector.connect(
            host=host,
            user=user,
            database=database,
            password=password
        )
        #wykonanie zapytania i zwrócenie jego wyników
        if connection.is_connected():
            print("connected")
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        #jeśli error
    except mysql.connector.Error as err:
        print("error connecting", err)
        return None
    finally:
        #close connection
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("connection closed")

#konwersja na poprawną tabele
def create_data_table(x):
#wczytanie wyniku zapytania
    df = pd.DataFrame(x)
#konwersja do przetwarzalnych formatów
    #godzina
    df[3] = df[3].astype(str).str.split().str[2].str.split(':').str[0].astype(int)
    #dzień
    df[2] = pd.to_numeric(df[2])
    #czas
    df[6] = pd.to_numeric(df[6])
    #stworzenie tabeli
    heatmap_data_table = df.pivot_table(index=3, columns=2, values=6, aggfunc='mean')
    return heatmap_data_table

#Pętla wykonująca zapytania do bazy. Wyniki zapytań trafiają następnie do funkcji, która przekształca je w tabele, które są kompatybilne z matplotlibem, ostatecznie konfiguruje heatmapy (wygląd)
for i, (query_name, query)  in enumerate(queries.items()):
    result = execute_query(host, user, password,
        database, query)
        #konfiguracja heatmapy
    heatmap_data = create_data_table(result)
    #rozmiar
    plt.figure(figsize=(10, 8))
    #konfig heatmapy (kolorystyka, jak od siebie zależą poszczególne 'kafelki')
    plt.imshow(heatmap_data, cmap='RdYlGn_r', interpolation='nearest', origin='upper')
    #podpis skali kolorystycznej
    plt.colorbar(label='Czas (minuty)')
    #podpis oś X
    plt.xlabel('Dzień tygodnia')
    # podpis oś Y
    plt.ylabel('Godzina')
    #etykiety X
    plt.xticks(np.arange(len(heatmap_data.columns)), heatmap_data.columns, rotation=45)
    #etykiety Y
    plt.yticks(np.arange(len(heatmap_data.index)), heatmap_data.index)
    #title
    plt.title(f'{query_name}')
    plt.tight_layout()
    #zapis
    plt.savefig(f'heatmap{i+1}.png', bbox_inches='tight')
