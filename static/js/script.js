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
    //Update

    for(let i = 0; i<Object.keys(data).length; i = i+1){
        const mot = document.createElement("span");
        mot.id = i;
        data[i].classes.forEach(classe => {
            mot.classList.add(classe);
        });

        if(data[i].mot == " "){
            mot.innerHTML = "&nbsp";
        } else {
            mot.innerHTML = data[i].mot;
        }
    
        if(data[i].classes.includes("titre")){
            titre.appendChild(mot);
        } else {
            article.appendChild(mot);
        }
    }
};