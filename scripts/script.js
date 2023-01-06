/* C'est un bordel mais ça marche */
$(document).ready(function() {
    console.log(new Date() + ": Document ready");
    var jison = JSON.parse(document.getElementById("receive").innerHTML);
    for(let i = 0; i< Object.keys(jison).length; i = i+1){
        for (var classe in jison[i]["classes"]){
            document.getElementById(i).classList.add(jison[i]["classes"][classe]);
        }
    }
});

$("#new").click(function() {
    document.getElementById("chargement").innerHTML = "Chargement...";
});