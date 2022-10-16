::Download nin model if it does not exist yet
IF EXIST "./data/model.bin" (
    echo 'Bin model file already exists'
) ELSE (
    curl -o ./data/model.bin https://embeddings.net/embeddings/frWac_non_lem_no_postag_no_phrase_200_cbow_cut100.bin
)
::Launch server
python index.py