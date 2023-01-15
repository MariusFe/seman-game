/*
    Script for script.js
*/

// Variables globales
// Id utiles
var chargement, titre, article;


$(document).ready(function() {
    /*var jison = JSON.parse(document.getElementById("receive").innerHTML);
    for(let i = 0; i< Object.keys(jison).length; i = i+1){
        for (var classe in jison[i]["classes"]){
            document.getElementById(i).classList.add(jison[i]["classes"][classe]);
        }
    }*/

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
            console.log(response.data);
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
            console.log(response.data);
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
        console.log(data[i]);
    }
};

/*
<div id="receive">{% if receive %}{{ receive1 }}{% endif %}</div>
        
        <p id="titre">
            {% if receive %}
                {% for word in receive %}
                    {% if "article" not in receive[word]["classes"] %}
                        {% if receive[word]["mot"] == " " %}
            <span id = {{ word }} class="mot">&nbsp;</span>
                        {% else %}
                            {% if receive[word]["mot"] == "\n" %}
            <br>          
                            {% else %}
            <span id = {{ word }} class="">{{ receive[word]["mot"] }}</span>
                            {% endif %}
                        {% endif %}        
                    {% endif %}
                {%endfor%}
            {% endif %}
    
        </p>

        <p id="article">
            {% if receive %}
                {% for word in receive %}
                    {% if "titre" not in receive[word]["classes"] %}
                        {% if receive[word]["mot"] == " " %}
            <span id = {{ word }} class="mot">&nbsp;</span>
                        {% else %}
            <span id = {{ word }} class="">{{ receive[word]["mot"] }}</span>
                        {% endif %}        
                    {% endif %}
                {%endfor%}
            {% endif %}
        </p>
        */