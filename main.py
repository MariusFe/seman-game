from gensim.models import KeyedVectors
import random

#http://fauconnier.github.io/

def main():

  model = KeyedVectors.load_word2vec_format("./datasets/frWac_non_lem_no_postag_no_phrase_200_cbow_cut100.bin", binary=True, unicode_errors="ignore")
  # print(model.similarity("profondément", "non"))
  
  liste = open("./datasets/liste_francais.txt","r").readlines()
  mot = random.choice(liste)
  mot = mot[:-1]
  print(mot)
  inpt = ''
  while inpt != mot:
    inpt = str(input("Entrez le mot: "))
    try:
      print(f"{inpt} est à {model.similarity(inpt, mot)*100}% de la réponse et est éloigné de {model.distance(inpt, mot)}\n")
    except Exception as e:
        print("Le mot n'est pas présent dans le dictionnaire !\n")

  print("\n\nBravo vous avez trouvé!")

  # # print(model.most_similar("pauvreté"))


if __name__ == "__main__":
  main()
