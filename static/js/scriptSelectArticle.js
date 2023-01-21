var titre, article, chargement;

$(document).ready(function() {

    titre = document.getElementById("titre");
    article = document.getElementById("article");
    chargement = document.getElementById("chargement");

    newarticle();

    $("#oui").click(function(){
        var titreString = "";
        if(titre.getElementsByTagName('*').length > 0){
            for(let i = 0; i <= titre.getElementsByTagName('*').length - 1; i = i+1){
                if(titre.getElementsByTagName("*")[i].innerHTML == "&nbsp;"){
                    titreString = titreString + " ";
                } else {
                    titreString = titreString + titre.getElementsByTagName("*")[i].innerHTML;
                }
            }
        }
        newarticle();
    });

    $("#non").click(function(){
        newarticle();
    });

    $("#new_article").click(function(){
        newarticle();
    });
});

// Faire la requete vers le serveur
function newarticle(){
    $("#chargement").fadeIn("slow");

    axios.get('/new_article')
        .then(function (response) {
        // handle success
        axios.get('/tricher')
            .then(function(response){

                updatePage(response.data);
                $( "#chargement" ).fadeOut("slow");
            })
            .catch(function(error){
                console.log(error);
            });
    })
        .catch(function (error) {
        // handle error
        console.log(error);
        chargement.innerHTML = "Erreur lors du chargement de la page.";
    });
}

function updatePage(data){
    titre.innerHTML = "";
    article.innerHTML = "";
    var counterSentence = 0;
        
    for(let i in data){
        var mot = document.createElement("span");

        data[i].classes.forEach(classe => {
            mot.classList.add(classe);
        });

        if(data[i].mot == " "){
            mot.innerHTML = "&nbsp;";
        } /*else if (data[i].mot == "\n"){
            mot = document.createElement("br");
        }*/ else if (data[i].mot != ""){
            mot.innerHTML = data[i].mot; //save the word
        } else {
            continue;
        }
    
        if(data[i].classes.includes("titre"))
            titre.appendChild(mot);
        else 
            article.appendChild(mot);

        // Only displays the first two sentences
        if(mot.innerHTML == "."){
            counterSentence = counterSentence + 1;
            if(counterSentence == 5){
                break;
            }
        }
    }
};