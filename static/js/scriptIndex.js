/*
    Script for script.js
*/

// Variables globales
// Id utiles
var chargement, titre, article;

var continue1 = false;


$(document).ready(function() {

    window.onbeforeunload = function(){
        return "T'es sûr tu veux quitter chef ?";
    }

    chargement = document.getElementById("chargement");
    titre = document.getElementById("titre");
    article = document.getElementById("article");

    // newarticle();
    document.getElementById("submit_word").click(); //triggers the ask of a document


    document.getElementById("word").addEventListener("keypress", function(event) { // Handle the press of Enter (because it is not in a form)
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

    $("#new_article").click(function(){
        Swal.fire({
            title: 'Êtes vous sûrs de vouloir recharger une nouvelle page ?',
            showDenyButton: true,
            confirmButtonText: 'Oui',
            denyButtonText: 'Non',
          }).then((result) => {
            if (result.isConfirmed) {
                newarticle();
            } else if (result.isDenied) {
                Swal.fire('Okay let\'s continue then !', '', 'info');
            }
          });
    });

    $("#copier_code").click(function(){
        var code = document.getElementById("code_article_texte").innerHTML;
        navigator.clipboard.writeText(code);
    });
});

function updateArticle(data){

    titre.innerHTML = "";
    article.innerHTML = "";
        
    for(let i in data){
        var mot = document.createElement("span");
        
        data[i].classes.forEach(classe => {
            mot.classList.add(classe);
        });

        if(data[i].mot == " "){
            mot.innerHTML = "&nbsp;";
        } /*else if (data[i].mot == "\n"){ // What to do with line break? it doesn't seem to work properly with just a creation of a <br>
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
    }
};

// Génération d'un nouvel article
function newarticle() {
    $( "#chargement" ).fadeIn("slow");
    continue1 = false;
    axios.get('/new_article')
        .then(function (response) {
        // handle success
        $( "#chargement" ).fadeOut("slow");
        updateArticle(response.data);
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
    console.log("Length trouvé: " + nbfound_title);
    var length_title = document.getElementById("titre").getElementsByClassName("titre").length;
    console.log("Length titre: " + length_title);

    if(nbfound_title==length_title && !continue1){
        Swal.fire({
            title: 'Good Job !',
            showDenyButton: true,
            confirmButtonText: 'New game',
            denyButtonText: `Continue`,
          }).then((result) => {
            if (result.isConfirmed) {
                newarticle();
            } else if (result.isDenied) {
                Swal.fire('Okay let\'s continue then !', '', 'info');
                if(!continue1) continue1 = true;
            }
        });
    }
}