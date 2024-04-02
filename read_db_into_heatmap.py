import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import mysql.connector

# MySQL database config
host = '34.118.70.238'
user = 'root'
#password = ''
database = 'googletraffic'
query = "SELECT * FROM googletraffic.traffic;"
def execute_query(host, user, database, query):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            database=database
        )
        if connection.is_connected():
            print("Połączono z bazą danych")
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
    except mysql.connector.Error as err:
        print("Błąd połączenia z bazą danych:", err)
        return None
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Połączenie z bazą danych zostało zamknięte")
result = execute_query(host, user, database, query)
def create_data_table():
#teraz działania na query zamiast na csv
#wczytanie wyniku zapytania
    df = pd.DataFrame(result)
#konwersja do przetwarzalnych formatów
    #godzina
    df[3] = pd.to_numeric(df[3].str.split(':').str[0])
    #dzień
    df[2] = pd.to_numeric(df[2])
    #czas
    df[6] = pd.to_numeric(df[6])
    #stworzenie tabeli
    heatmap_data_table = df.pivot_table(index=3, columns=2, values=6, aggfunc='mean')
    return heatmap_data_table

#konfiguracja heatmapy
heatmap_data = create_data_table()

plt.figure(figsize=(10, 8))
plt.imshow(heatmap_data, cmap='RdYlGn_r', interpolation='nearest', origin='upper')
plt.colorbar(label='Czas (minuty)')
plt.xlabel('Dzień tygodnia')
plt.ylabel('Godzina')
plt.xticks(np.arange(len(heatmap_data.columns)), heatmap_data.columns, rotation=45)
plt.yticks(np.arange(len(heatmap_data.index)), heatmap_data.index)
plt.title('Czas podróży w zależności od dnia tygodnia i godziny')
plt.tight_layout()
plt.show()
