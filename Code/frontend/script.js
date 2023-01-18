function submitForm(e) {

    const textfield = document.getElementById('message-input')
    const message = textfield.value

    e.preventDefault();
    textfield.value = ""

    sendMessage(message)

    displayMessage(message, "user")
}

function sendMessage(message) {
    const package = {
        "sender": "user",
        "message": message,
    }

    fetch("http://localhost:5005/webhooks/rest/webhook", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(package)
    })
        .then(res => res.json())
        .then(data => {
            handleResponse(data[0]);
        });
}

function handleResponse(data) {
    if (data.hasOwnProperty("text")) {
        console.log("DISPLAY_MESSAGE")
        displayMessage(data.text, "bot")
    }
    if (data.hasOwnProperty("buttons")) {
        console.log("DISPLAY_BUTTONS")
        displayButtons(data.buttons)
    }
    if (data.hasOwnProperty("custom")) {
        console.log("DISPLAY_COCKTAILS")
        displayCocktails(data.custom)
    }
}

function displayMessage(message, source) {
    const scrollContainer = document.getElementById('scroll-container');
    const messageRow = document.createElement("div")
    const messageContainer = document.createElement("div")
    const messageText = document.createElement("p")

    messageContainer.className = 'message-container'
    messageText.innerText = message

    if (source == "user") {
        messageRow.className = "user-message-row"
    }
    if (source == "bot") {
        messageRow.className = "bot-message-row"
    }

    messageContainer.appendChild(messageText)
    messageRow.appendChild(messageContainer)
    scrollContainer.appendChild(messageRow)
}

function displayButtons(buttons) {
    const scrollContainer = document.getElementById('scroll-container');
    const buttonContainer = document.createElement("div")

    buttonContainer.className = 'selection-button-container'

    buttons.forEach(btn => {
        const button = document.createElement("button")
        button.className = "selction-button"
        button.dataset.payload = btn.payload
        button.innerText = btn.title
        button.addEventListener("click", handleButtonClick)
        buttonContainer.appendChild(button)
    })

    scrollContainer.appendChild(buttonContainer)
}

function displayCocktails(cocktails) {
    const scrollContainer = document.getElementById('scroll-container');
    const cocktailsContainer = document.createElement("div")

    cocktailsContainer.className = 'cocktails-container'

    cocktails.forEach(cocktail => {
        const cocktailContainer = document.createElement("button")
        const cocktailHeader = document.createElement("div")
        const cocktailImage = document.createElement("img")
        const cocktailName = document.createElement("h3")
        const cocktailBody = document.createElement("div")
        const cocktailIngredients = document.createElement("div")
        const cocktailInstructions = document.createElement("p")

        cocktailContainer.className = 'cocktail-container'
        cocktailHeader.className = 'cocktail-header'
        cocktailImage.className = 'cocktail-img'
        cocktailBody.className = 'cocktail-body'

        cocktailImage.src = cocktail.url
        cocktailName.innerText = cocktail.name
        cocktail.ingredients.forEach(ingridient => {
            const cocktailIngridient = document.createElement("p")
            cocktailIngridient.innerText = ingridient
            cocktailIngredients.appendChild(cocktailIngridient)
        })
        cocktailInstructions.innerText = cocktail.instructions

        cocktailContainer.addEventListener("click", function() {
            handleCocktailClick(this);
        }, false)

        cocktailBody.appendChild(cocktailIngredients)
        cocktailBody.append(cocktailInstructions)
        cocktailHeader.appendChild(cocktailImage)
        cocktailHeader.append(cocktailName)
        cocktailContainer.appendChild(cocktailHeader)
        cocktailContainer.appendChild(cocktailBody)
        cocktailsContainer.appendChild(cocktailContainer)
    })

    scrollContainer.appendChild(cocktailsContainer)
}

function handleButtonClick(event) {
    console.log("HANDLEBUTTONCLICK")
    const selectedButton = event.target
    const allButtons = Array.from(selectedButton.parentNode.children)
    console.log(selectedButton.dataset.payload)
    const taste = selectedButton.dataset.payload

    allButtons.forEach(button => {
        if(button != selectedButton) button.dataset.selected = false
        button.disabled = true
    }); 
    selectedButton.dataset.selected = true

    sendMessage(taste)
}

function handleCocktailClick(selectedCocktail) {
    console.log("HANDLECOCKTAILCLICK")

    const allCocktails = Array.from(selectedCocktail.parentNode.children)
    console.log(allCocktails)

    allCocktails.forEach(cocktail => {
        console.log(cocktail)
        if(cocktail != selectedCocktail) cocktail.dataset.selected = false
        cocktail.disabled = true
    })
    selectedCocktail.dataset.selected = true
}


/* function getBotResponse(user_message) {

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
} */

/* function getCocktailInfo(data) {
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
} */

/* function appendCocktail(data) {

    var messageContainer = document.getElementById('scroll-container');
    var ingredientsHTML = ""
    console.log(data)

    for (let cocktail of data) {
        let i = 0
        console.log(cocktail[3])
        for (let ingredient of cocktail[3]) {
            i++
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
} */