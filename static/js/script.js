/*
    Script for script.js
*/

// Variables globales
// Id utiles
var chargement, titre, article;


$(document).ready(function() {

    chargement = document.getElementById("chargement");
    titre = document.getElementById("titre");
    article = document.getElementById("article");

    // Génération d'un nouvel article
    $("#new").click(function() {
        chargement.innerHTML = "Chargement...";
        axios.get('/new_article')
            .then(function (response) {
            // handle success
            chargement.innerHTML = "";
            updateTitreArticle(response.data);
        })
            .catch(function (error) {
            // handle error
            console.log(error);
            chargement.innerHTML = "Erreur lors du chargement de la page.";
        });
    });

    document.getElementById("word").addEventListener("keypress", function(event) {
        // If the user presses the "Enter" key on the keyboard
        if (event.key === "Enter") {
          // Cancel the default action, if needed
          event.preventDefault();
          // Trigger the button element with a click
          document.getElementById("submit_word").click();
        }
      }); 

    // Soumission d'un mot
    $("#submit_word").click(function(){
        chargement.innerHTML = "Chargement...";
        const motToTest = document.getElementById("word");
        axios.post('/submit',{
            "in_word": motToTest.value
        })
            .then(function (response) {
            // handle success
            chargement.innerHTML = "";
            motToTest.value = "";
            updateTitreArticle(response.data);
        })
            .catch(function (error) {
            // handle error
            console.log(error);
            chargement.innerHTML = "Erreur lors du chargement de la page.";
        });
    });
});

function updateTitreArticle(data){
    article.innerHTML = "";
    titre.innerHTML = "";
        
    for(let i in data){
        const mot = document.createElement("span");
        //mot.id = i;
        
        if(data[i].mot.trim() != "") //avoid writing sapces in my beatiful cemantix game
        {

            data[i].classes.forEach(classe => {
                mot.classList.add(classe);
            });

            mot.innerHTML = data[i].mot.trim(); //save the word
        
            if(data[i].classes.includes("titre"))
                titre.appendChild(mot);
            else 
                article.appendChild(mot);
        }
    }
};