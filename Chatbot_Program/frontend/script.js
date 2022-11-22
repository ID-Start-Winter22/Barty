var url = "http://localhost:5005/webhooks/rest/webhook"

function submitForm(e) {

    var request = new XMLHttpRequest();
    var params = JSON.stringify({
        sender: "test_user",
        message: document.getElementById('message-input').value
    })
    console.warn(params)
    
    e.preventDefault();

    request.open('POST', url, true);
    request.setRequestHeader("Content-Type", "application/json");
    request.onreadystatechange = function () {
        if (request.readyState === XMLHttpRequest.DONE) {
            if (request.status === 200) {
                var response = JSON.parse(request.response);
                // if(response.result) {

                // }
            }
        }
    }
    request.send(params);
}