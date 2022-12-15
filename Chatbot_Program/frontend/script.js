var url = "http://localhost:5005/webhooks/rest/webhook"


function submitForm(e) {

    var textfield = document.getElementById('message-input')
    var user_message = document.getElementById('message-input').value
    e.preventDefault();
    textfield.value = ""
    appendMessage(user_message, "user")
    getBotResponse(user_message)

}

function getBotResponse(user_message) {

    var request = new XMLHttpRequest();
    var params = JSON.stringify({
        sender: "test_user",
        message: user_message
    });

    request.open('POST', url, true);
    request.setRequestHeader("Content-Type", "application/json");
    request.onreadystatechange = function () {
        if (request.readyState === XMLHttpRequest.DONE) {
            if (request.status === 200) {
                var response = JSON.parse(request.response);
                botMessageText = response[0].text
                if (botMessageText.startsWith('-rec: ')) {
                    appendCocktail(getCocktailInfo(botMessageText.slice(6)))
                } else {
                    appendMessage(botMessageText, "bot")
                }

            }
        }
    }
    request.send(params);
}



function getCocktailInfo(data) {
    var recCocktails = []

    dataArray = data.split(" | ")
    for (let cocktail of dataArray) {
        let recCocktail = [""]
        info = cocktail.split(";")
        recCocktail.push(info[0])
        recCocktail.push(info[1])
        recCocktail.push(info[2].split(","))
        recCocktail.push(info[3])
        recCocktails.push(recCocktail)
    }
    return recCocktails
}

function appendCocktail(data) {

    var messageContainer = document.getElementById('scroll-container');
    var ingredientsHTML = ""
    console.log(data)

    for(let cocktail of data) {
        let i = 0
        console.log(cocktail[3])
        for(let ingredient of cocktail[3]) {
            i ++
            ingredientsHTML += "<p id='" + cocktail[1] + "-ingredient" + i + "'>" + ingredient + "</p>"
        }
        
        cocktailHTML = "<div class='recipe-container' id='" + cocktail[1] + "-container'><button class='recipe-header' data-selected='none' onclick='toggleRecipe(this)'><img src='" + cocktail[2] + "' class='recipe-img' id='" + cocktail[1] + "-img'><h3 id='" + cocktail[1] + "-title'>" + cocktail[1] + "</h3></button><div class='recipe-detail-body' id='" + cocktail[1] + "-ingredients-container'>" + ingredientsHTML + "</div><div class='recipe-detail-body' id='" + cocktail[1] + "-instructions-container'><p>" + cocktail[4] + "</p></div></div>"
        messageContainer.innerHTML += cocktailHTML

    }
}
function appendMessage(message, source) {
    
    var messageContainer = document.getElementById('scroll-container');

    if (source == "user") {
        messageContainer.innerHTML += "<div class='user-message-row'><div class='message-container'><p class='message-text'>" + message + "</p></div></div>";
    }
    if (source == "bot") {
        if (botMessageText != undefined) {
            messageContainer.innerHTML += "<div class='bot-message-row'><div class='message-container'><p class='message-text'>" + botMessageText + "</p></div></div>";
        } else {
            messageContainer.innerHTML += "<div class='bot-message-row'><div class='message-container'><p class='message-text'> Hm. Hab keine antwort vom Server bekommen. </p></div></div>";
        }
    }
}

function toggleRecipe(button) {
    button.dataset.selected = "true";
    let recipeButtons = document.getElementsByClassName("recipe-header");
    console.log(recipeButtons)
    for (let btn of recipeButtons) {
        btn.disabled = true
    }
    // recipeButtons.array.forEach(element => {
    //     btn.disabled = true
    // });
}