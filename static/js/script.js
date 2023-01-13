/* C'est un bordel mais ça marche */
$(document).ready(function() {
    console.log(new Date() + ": Document ready");
    /*var jison = JSON.parse(document.getElementById("receive").innerHTML);
    for(let i = 0; i< Object.keys(jison).length; i = i+1){
        for (var classe in jison[i]["classes"]){
            document.getElementById(i).classList.add(jison[i]["classes"][classe]);
        }
    }*/

    $("#new").click(function() {
        document.getElementById("chargement").innerHTML = "Chargement...";
        $("titre").html("Oui");
        $("article").html("Non");
    
        fetch('/new_article').then(response =>{
            console.log(response);
        })
            .then(data => {
            console.log(data); 
            document.getElementById("chargement").innerHTML = "";
            $("titre").html(data);
            $("article").html(data);
        });
    });

    $("#submit_word").click(function(){

    });
});



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