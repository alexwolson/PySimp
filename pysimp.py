from imdb import IMDb
from tqdm import tqdm
import numpy as np
ia = IMDb()
simpsons = ia.search_movie('The Simpsons')[0]
ia.update(simpsons, 'episodes')
episodes = simpsons['episodes']

def obtain_ratings(episodes):
        allratings = []
        simpsratings = {}
        ##Main loop
        for seasontuple in tqdm(episodes.items()):
                simpsratings[seasontuple[0]] = {}
                for episodetuple in tqdm(seasontuple[1].items()):
                    episode = episodetuple[1]
                    ia.update(episode)
                    try:
                        simpsratings[seasontuple[0]][episodetuple[1]['title']] = episode['rating']
                        allratings.append(episode['rating'])
                    except:
                        simpsratings[seasontuple[0]][episodetuple[1]['title']] = 5.00
                        allratings.append(5.00)
        return (simpsratings, np.mean(allratings), np.std(allratings))

def std_factor(x, results):
    (episoderatings, mean, stddev) = results
    number_of_episodes = 0
    for season in episoderatings.items():
        number_of_episodes += len(season[1])
    shrunk_episodes = 0
    for season in episoderatings.items():
        shrunk_episodes += len([episode[0] for episode in season[1].items() if episode[1] > (mean + (x * stddev))])
    #print("Total number of episodes: %d" % number_of_episodes)
    #print("Shrunk number: %d" % shrunk_episodes)
    return shrunk_episodes
    
def get_best(x, results):
    (episoderatings, mean, stddev) = results
    outputdict = {}
    for season in episoderatings.items():
        outputdict[season[0]] = [episode[0] for episode in season[1].items() if episode[1] > (mean + (x * stddev))]
    return outputdict

if __name__ == "__main__":
    ia = IMDb()
    simpsons = ia.search_movie('The Simpsons')[0]
    ia.update(simpsons, 'episodes')
    episodes = simpsons['episodes']
    results = obtain_ratings(episodes)
    inval = raw_input("([q]uit) How many episodes you want? ")
    while(inval.lower() != "q"):
        std_result = -4
        epcount = std_factor(std_result, results)
        while(epcount > inval):
            std_result -= 0.1
            epcount = std_factor(std_result, results)
        best_episodes = get_best(std_result, results)
        for season in best_episodes.items():
            print("Season %d: " % season[0])
            for episode in season[1].items():
                print("\t" + episode[1])
