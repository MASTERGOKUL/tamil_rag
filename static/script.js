document.getElementById('send-button').onclick = function() {
    const userInput = document.getElementById('user-input').value;
    if (userInput) {
        appendMessage('user', userInput);
        document.getElementById('user-input').value = '';
        
        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ input: userInput })
        })
        .then(response => response.json())
        .then(data => {
            appendMessage('bot', data.response);
        });
    }
};

function appendMessage(sender, message) {
    const conversation = document.getElementById('conversation');
    const messageElement = document.createElement('div');
    messageElement.classList.add(sender);
    messageElement.textContent = message;
    conversation.appendChild(messageElement);
    conversation.scrollTop = conversation.scrollHeight; // Scroll to the bottom
}
