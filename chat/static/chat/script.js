document.addEventListener("DOMContentLoaded", () => {
  const chatWindow = document.getElementById("chat-window");
  const messageInput = document.getElementById("message-input");
  const sendBtn = document.getElementById("send-btn");
  const deleteBtn = document.getElementById("delete-btn");

  // Function to scroll to bottom
  function scrollToBottom() {
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  // Initial scroll
  scrollToBottom();

  // Fetch messages every 1 second
  setInterval(fetchMessages, 1000);

  function fetchMessages() {
    fetch("/messages/")
      .then((response) => response.json())
      .then((data) => {
        updateChatWindow(data.messages);
      })
      .catch((error) => console.error("Error fetching messages:", error));
  }

    function updateChatWindow(messages) {
        chatWindow.innerHTML = '';
        if (messages.length === 0) {
            chatWindow.innerHTML = `
                <div class="empty-state fade-in">
                    <p>No messages yet. Start the conversation!</p>
                </div>`;
            return;
        }
        messages.forEach(msg => {
            const wrapper = document.createElement('div');
            wrapper.classList.add('message-wrapper');
            
            const avatar = document.createElement('img');
            avatar.classList.add('avatar');
            avatar.src = '/static/chat/profile.png';
            avatar.alt = 'Profile';
            
            const contentDiv = document.createElement('div');
            contentDiv.classList.add('message-content');

            const bubble = document.createElement('div');
            bubble.classList.add('message-bubble');
            bubble.textContent = msg.text;

            const time = document.createElement('span');
            time.classList.add('timestamp');
            time.textContent = msg.timestamp;
            
            contentDiv.appendChild(bubble);
            contentDiv.appendChild(time);

            wrapper.appendChild(avatar);
            wrapper.appendChild(contentDiv);
            chatWindow.appendChild(wrapper);
        });
    }

  // Send Message
  sendBtn.addEventListener("click", sendMessage);
  messageInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });

  function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    fetch("/send/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: message }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          messageInput.value = "";
          fetchMessages(); // Update immediately
          setTimeout(scrollToBottom, 100);
        }
      })
      .catch((error) => console.error("Error sending message:", error));
  }

  // Delete Oldest Message
  deleteBtn.addEventListener("click", () => {
    fetch("/delete/", {
      method: "POST",
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          fetchMessages(); // Update immediately
        } else {
          alert(data.message);
        }
      })
      .catch((error) => console.error("Error deleting message:", error));
  });
});
