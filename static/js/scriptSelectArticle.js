var titre, article, chargement;

$(document).ready(function() {

    titre = document.getElementById("titre");
    article = document.getElementById("article");
    chargement = document.getElementById("chargement");

    //newarticle();

    $("#oui").click(function(){
        // Add the title to a txt, json, xml file 
        axios.get('/add_article')
            .then(function(response){
                // Success
            })
            .catch(function(error){
                // Error
                console.log(error);
            });
        newarticle();
    });

    $("#non").click(function(){
        newarticle();
    });

    $("#new_article").click(function(){
        newarticle();
    });

    $("#submit_article").click(function(){
        var article = document.getElementById("article_texte").value;
        document.getElementById("faux_article").innerHTML = "";
        document.getElementById("vrai_article").innerHTML = "";
        document.getElementById("article_in_list").innerHTML = "";

        // Add an article to the list
        axios.post('/add_article',{
            'article': article
        }).then(function(response){
            // Success 
            if (response.data['vraiArticle'] == true && response.data['inList'] == false){ // Vrai article pas dans la liste

                document.getElementById("article_texte").value = "";
                document.getElementById("vrai_article").innerHTML = "Article ajouté !";

            } else if(response.data['vraiArticle'] == true && response.data['inList'] == true) { // Vrai article mais pas dans la liste
                
                document.getElementById("article_texte").value = "";
                document.getElementById("article_in_list").innerHTML = "L'article est déjà dans la liste.";

            } else { // Faux article
                document.getElementById("faux_article").innerHTML = "Entrez un titre d'article valide !";
            }
        })
        .catch(function(error){
            console.log(error);
        });

    });

    document.getElementById("article_texte").addEventListener("keypress", function(event) { // Handle the press of Enter (because it is not in a form)
        if (event.key === "Enter") {
          event.preventDefault();
          document.getElementById("submit_article").click();
        }
    }); 

    // Redirect to index
    $("#retour").click(function(){
        location.href = document.URL.split('/')[0] + "//" + document.URL.split('/')[2];
    });

});

// Faire la requete vers le serveur
function newarticle(){
    $("#chargement").fadeIn("slow");

    axios.post('/new_article', {
        'random': true,
    })
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


// Update the page to add the text in the title and in the article
function updatePage(data){
    titre.innerHTML = "";
    article.innerHTML = "";
    var counterSentence = 0;
        
    var paragraphe = document.createElement("p");
    var triggerArticle = false;

    for(let i in data){
        var mot = document.createElement("span");
        
        data[i].classes.forEach(classe => {
            mot.classList.add(classe);
        });

        if(triggerArticle == false && data[i].classes.includes("article")){
            triggerArticle = true;
            titre.appendChild(paragraphe);
            paragraphe = document.createElement("p");
        }

        if(data[i].mot == " "){
            mot.innerHTML = "&nbsp;";
        } else if (data[i].mot == "\n"){
            paragraphe.appendChild(mot);
            article.appendChild(paragraphe);
            paragraphe = document.createElement("p");
            continue;
        } else if (data[i].mot != ""){
            mot.innerHTML = data[i].mot; //save the word
        } else {
            continue;
        }
        
        paragraphe.appendChild(mot);

        // Only displays the first two sentences
        if(mot.innerHTML == "."){
            counterSentence = counterSentence + 1;
            if(counterSentence == 5){
                break;
            }
        }
    }
};