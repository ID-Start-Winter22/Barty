var url = "http://localhost:5005/webhooks/rest/webhook"


function submitForm(e) {

    var messageContainer = document.getElementById('scroll-container');
    var textfield = document.getElementById('message-input')

    var request = new XMLHttpRequest();
    var user_message = document.getElementById('message-input').value
    var params = JSON.stringify({
        sender: "test_user",
        message: user_message
    });

    e.preventDefault();
    textfield.value = ""
    messageContainer.innerHTML += "<div class='user-message-row'><div class='message-container'><p class='message-text'>" + user_message + "</p></div></div>";


    request.open('POST', url, true);
    request.setRequestHeader("Content-Type", "application/json");
    request.onreadystatechange = function () {
        if (request.readyState === XMLHttpRequest.DONE) {
            if (request.status === 200) {
                var response = JSON.parse(request.response);
                botMessageText = response[0].text
                
                if(botMessageText != undefined) {
                     messageContainer.innerHTML += "<div class='bot-message-row'><div class='message-container'><p class='message-text'>" + botMessageText + "</p></div></div>";
                } else {
                    messageContainer.innerHTML += "<div class='bot-message-row'><div class='message-container'><p class='message-text'> Hm. Hab keine antwort vom Server bekommen. </p></div></div>";
                }
            }
        }
    }
    request.send(params);
}

function toggleRecipe(button) {
    button.dataset.active = true
}