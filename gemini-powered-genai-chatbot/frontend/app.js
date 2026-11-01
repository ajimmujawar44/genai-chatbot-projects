
"use strict";

// 1. Get elements from index.html
const themeBtn = document.getElementById("themeBtn");
const sendBtn = document.getElementById("sendBtn");
const userInput = document.getElementById("userInput");
const welcomeMessage = document.getElementById("welcomeMessage");
const chatFeed = document.getElementById("chatFeed");
const newChatBtn = document.getElementById("newChatBtn");

// 2. Local FastAPI backend
const API_URL = "http://127.0.0.1:8000/api/chat";

console.log("Chatbot frontend loaded.");
console.log("Using backend:", API_URL);

let isSending = false;

// 3. Toggle dark/light theme
if (themeBtn) {
    themeBtn.addEventListener("click", () => {
        document.body.classList.toggle("light-mode");
    });
}

// 4. Start a new chat
if (newChatBtn) {
    newChatBtn.addEventListener("click", () => {
        if (chatFeed) {
            chatFeed.replaceChildren();
            chatFeed.style.display = "none";
        }

        if (welcomeMessage) {
            welcomeMessage.style.display = "block";
        }

        if (userInput) {
            userInput.value = "";
            userInput.focus();
        }
    });
}

// 5. Add a chat bubble
function addMessageBubble(role, message) {
    const bubble = document.createElement("div");
    bubble.classList.add("msg", role);
    bubble.textContent = message;

    chatFeed.appendChild(bubble);
    chatFeed.scrollTop = chatFeed.scrollHeight;

    return bubble;
}

// 6. Send a message to FastAPI
async function handleSendMessage() {
    if (!userInput || !chatFeed || isSending) {
        return;
    }

    const text = userInput.value.trim();

    if (!text) {
        userInput.focus();
        return;
    }

    if (welcomeMessage) {
        welcomeMessage.style.display = "none";
    }

    chatFeed.style.display = "flex";

    addMessageBubble("user", text);
    userInput.value = "";

    isSending = true;

    if (sendBtn) {
        sendBtn.disabled = true;
    }

    userInput.disabled = true;

    const botBubble = addMessageBubble("bot", "Thinking...");

    try {
        console.log("Sending request to:", API_URL);

        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: text
            })
        });

        const data = await response.json().catch(() => ({}));

        console.log("Backend status:", response.status);
        console.log("Backend response:", data);

        if (!response.ok) {
            throw new Error(
                typeof data.detail === "string"
                    ? data.detail
                    : `Server returned status ${response.status}`
            );
        }

        if (typeof data.reply !== "string" || !data.reply.trim()) {
            throw new Error("The backend returned an empty response.");
        }

        // Display the backend response safely as plain text.
        // This avoids requiring DOMPurify and prevents HTML injection.
        // HTML/Markdown formatting will appear as plain text.
        botBubble.innerHTML = data.reply;

    } catch (error) {
        console.error("Chat request failed:", error);

        botBubble.textContent =
            `Sorry, I couldn't get a response. ${error.message} ` +
            "Please check that your backend is running.";

    } finally {
        isSending = false;

        if (sendBtn) {
            sendBtn.disabled = false;
        }

        userInput.disabled = false;
        userInput.focus();

        chatFeed.scrollTop = chatFeed.scrollHeight;
    }
}

// 7. Send button
if (sendBtn) {
    sendBtn.addEventListener("click", handleSendMessage);
}

// 8. Enter sends; Shift+Enter inserts a new line
if (userInput) {
    userInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            handleSendMessage();
        }
    });
}
