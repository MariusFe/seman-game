/*
    Script for script.js
*/

// Variables globales
// Id utiles
var chargement, titre, article;

var nb2findtitle, nb2findarticle;
var continue1 = false, continue2 = false;


$(document).ready(function() {

    window.onbeforeunload = function(){
        return "T'es sûr tu veux quitter chef ?";
    }

    chargement = document.getElementById("chargement");
    titre = document.getElementById("titre");
    article = document.getElementById("article");

    newarticle();
    document.getElementById("submit_word").click(); //triggers the ask of a document


    document.getElementById("word").addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
          event.preventDefault();
          document.getElementById("submit_word").click();
        }
      }); 

    // Soumission d'un mot
    $("#submit_word").click(function(){
        var motToTest = document.getElementById("word").value.trim()
        if(motToTest != ""){
            //$( "#chargement" ).fadeIn("fast");
            axios.post('/submit',{
                "in_word": motToTest
            })
                .then(function (response) {
                // handle success
                //$( "#chargement" ).fadeOut("fast");
                document.getElementById("word").value = "";
                updateArticle(response.data);
                checkdone();
            })
                .catch(function (error) {
                // handle error
                console.log(error);
                chargement.innerHTML = "Erreur lors du chargement de la page.";
            });
        }
        else{
            Swal.fire('Empty mot');
        }
    });
});

function updateArticle(data){
    article.innerHTML = "";
    titre.innerHTML = "";
        
    for(let i in data){
        const mot = document.createElement("span");
        //mot.id = i;
        

        data[i].classes.forEach(classe => {
            mot.classList.add(classe);
        });

        mot.innerHTML = data[i].mot.trim(); //save the word
    
        if(data[i].classes.includes("titre"))
            titre.appendChild(mot);
        else 
            article.appendChild(mot);

    }
};

// Génération d'un nouvel article
function newarticle() {
    $( "#chargement" ).fadeIn("slow");
    axios.get('/new_article')
        .then(function (response) {
        // handle success
        $( "#chargement" ).fadeOut("slow");
        updateArticle(response.data);
        nb2findtitle = document.getElementById("titre").getElementsByClassName("cache").length - document.getElementById("titre").getElementsByClassName("character").length;
        nb2findarticle = document.getElementById("article").getElementsByClassName("cache").length - document.getElementById("article").getElementsByClassName("character").length;
        document.getElementById("word").focus();
    })
        .catch(function (error) {
        // handle error
        console.log(error);
        chargement.innerHTML = "Erreur lors du chargement de la page.";
    });
};

function checkdone(){
    var nbfound_title = document.getElementById("titre").getElementsByClassName("trouve").length;
    var nbfound_article = document.getElementById("article").getElementsByClassName("trouve").length;


    if(nbfound_title==nb2findtitle && !continue1 || nbfound_article==nb2findarticle && !continue2){
        Swal.fire({
            title: 'Good Job !',
            showDenyButton: true,
            confirmButtonText: 'New game',
            denyButtonText: `Continue`,
          }).then((result) => {
            if (result.isConfirmed) {
                window.location.reload();
            } else if (result.isDenied) {
                Swal.fire('Okay let\'s continue then !', '', 'info');
                if(continue1 && !continue2) continue2 = true;
                if(!continue1) continue1 = true;
            }
          });
    }
}