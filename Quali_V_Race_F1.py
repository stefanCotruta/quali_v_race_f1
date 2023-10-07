import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests

season = input("Choose season: ")
driver = input("Choose driver: ").lower()

def download_data(s, d):
    url = "http://ergast.com/api/f1/" + str(s) + "/drivers/" + d + "/results/.json"

    r = requests.get(url)

    finishing_positions = []
    qualifying_position = []
    curr_round = []

    for race in r.json()['MRData']['RaceTable']["Races"]:
        finishing_positions.append(int(race['Results'][0]['position']))
        qualifying_position.append(int(race['Results'][0]['grid']))
        curr_round.append(int(race['round']))


    result = pd.DataFrame({
        'Round' : curr_round,
        'Qualifying_Position' : qualifying_position,
        'Finishing_Position' : finishing_positions
    })

    return result

df_results = download_data(season, driver)

def plot(df):
    fig, ax = plt.subplots()

    df.plot(x='Round', y='Qualifying_Position', ax=ax, marker='.')
    df.plot(x='Round', y='Finishing_Position', ax=ax, marker='.')

    ax.legend(['Qualifying Pos','Finish Pos'])

    plt.xticks(np.arange(1, df['Round'].iloc[-1], step=1))
    plt.yticks(np.arange(1, 21, step=1))

    plt.show()


def mean_interpretation(df):
    s_mean = np.mean(df['Qualifying_Position'])
    f_mean = np.mean(df['Finishing_Position'])

    print("Average quali pos: " + str(s_mean))
    print("Average finish pos: " + str(f_mean))
    print("--------------------------")

    if  s_mean < f_mean:
        print("Better qualifier")
    elif s_mean == f_mean:
        print("Balanced")
    else:
        print("Better racer")


try:
    plot(df_results)
    mean_interpretation(df_results)
except Exception:
    print("An error occured")
