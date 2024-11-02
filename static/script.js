const userInputField = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

function sendMessage() {
    document.getElementById("chat-box").scrollTop=document.getElementById("chat-box").scrollHeight;
    const userInput = userInputField.value;
    if (userInput) {
        appendMessage('user', userInput);
        userInputField.value = '';
        
        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ input: userInput })
        })
        .then(response => response.json())
        .then(data => {
            let text = data.response.replaceAll("\n","<br>");
            text = text.replace(/\*\*(.*?)\*\*/g, "<b>$1</b>");

            appendMessage('bot',text );
        });
    }
    
}

// Send message on button click
sendButton.onclick = sendMessage;

// Send message on Enter key press
userInputField.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

function appendMessage(sender, message) {
    const conversation = document.getElementById('conversation');
    const parent = document.createElement('div');
    parent.classList.add("parent-"+sender)
    const messageElement = document.createElement('div');
    messageElement.classList.add(sender);
    messageElement.innerHTML = message;

    const img = document.createElement('div');
    img.classList.add(sender+"-img");
   
    parent.appendChild(messageElement);
    parent.appendChild(img);

    conversation.appendChild(parent);

    conversation.scrollTop = conversation.scrollHeight; // Scroll to the bottom
    document.getElementById("chat-box").scrollTop=document.getElementById("chat-box").scrollHeight;
    document.getElementById("user-input").value="";
}
