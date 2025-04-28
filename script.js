const chatContainer = document.getElementById("chat-container");
const promptInput = document.getElementById("prompt");
const cityInput = document.getElementById("city");
const generateBtn = document.getElementById("generate-btn");
const clearBtn = document.getElementById("clear-btn");
const loadingSpinner = document.getElementById("loading-spinner");

let messages = [];

function renderMessages() {
  chatContainer.innerHTML = "";
  messages.forEach((msg) => {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("mb-4");

    if (msg.role === "user") {
      msgDiv.innerHTML = `<div class="flex justify-end"><div class="bg-blue-100 text-blue-900 p-3 rounded-lg max-w-sm"><p>${msg.content}</p></div></div>`;
    } else {
      msgDiv.innerHTML = `<div class="flex justify-start"><div class="bg-gray-200 text-gray-800 p-3 rounded-lg max-w-sm"><p>${msg.content}</p></div></div>`;
    }

    chatContainer.appendChild(msgDiv);
  });
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function sendPrompt() {
  const prompt = promptInput.value.trim();
  const city = cityInput.value.trim();

  if (!prompt) return;

  messages.push({ role: "user", content: prompt });
  renderMessages();

  loadingSpinner.classList.remove("hidden");

  try {
    const response = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, city }),
    });

    const data = await response.json();
    loadingSpinner.classList.add("hidden");

    if (data.error) {
      messages.push({ role: "assistant", content: `Error: ${data.error}` });
    } else {
      messages.push({ role: "assistant", content: data.completion });
    }
    renderMessages();
  } catch (err) {
    loadingSpinner.classList.add("hidden");
    messages.push({ role: "assistant", content: `Error: ${err.message}` });
    renderMessages();
  }

  promptInput.value = "";
}

generateBtn.addEventListener("click", sendPrompt);
clearBtn.addEventListener("click", () => {
  messages = [];
  renderMessages();
  promptInput.value = "";
  cityInput.value = "";
});
