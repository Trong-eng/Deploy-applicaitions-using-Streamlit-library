import streamlit as st # type: ignore

def levenshtein_distance(token1, token2):
    rows = len(token1) + 1
    cols = len(token2) + 1
    distance = [[0 for _ in range(cols)] for _ in range(rows)]

    # initialize the distance matrix
    for i in range(rows):
        distance[i][0] = i
    for j in range(cols):
        distance[0][j] = j
    
    # recursively compute the distance of the two tokens
    for col in range(1, cols):
        for row in range(1, rows):
            distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
                                 distance[row][col-1] + 1,          # Cost of insertions
                                 distance[row-1][col-1] + (token1[row-1] != token2[col-1]))      # Cost of substitutions
    
    distances = distance[-1][-1]
    
    return distances

def load_vocab(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    words = sorted(set([line.strip().lower() for line in lines]))
    return words
vocabs = load_vocab(file_path='data/vocab.txt')

def main():
    st.title("Word Correction using Levenshtein Distance")
    word = st.text_input('Word:')

    if st.button("Compute"):

        # compute levenshtein distance
        leven_distances = dict()
        for vocab in vocabs:
            leven_distances[vocab] = levenshtein_distance(word, vocab)
        
        # sorted by distance
        sorted_distences = dict(sorted(leven_distances.items(), key=lambda item: item[1]))
        correct_word = list(sorted_distences.keys())[0]
        st.write('Correct word: ', correct_word)

        col1, col2 = st.columns(2)
        col1.write('Vocabulary:')
        col1.write(vocabs)
        
        col2.write('Distances:')
        col2.write(sorted_distences)

if __name__ == "__main__":
    main()