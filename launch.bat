:: Create folder if it does not exist
IF EXIST "./data" (
    echo 'Folder exists'
) ELSE (
    mkdir data
)

::Download bin model if it does not exist
IF EXIST "./data/model.bin" (
    echo 'Bin model exists'
) ELSE (
    curl -o ./data/model.bin https://embeddings.net/embeddings/frWac_non_lem_no_postag_no_phrase_200_cbow_cut100.bin
)
:: Download packages
pip install wikipedia-api --user
pip install gensim --user
pip install flask --user
:: Launch server
python index.py