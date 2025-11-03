const API_URL = 'http://localhost:5000';

const messagesDiv = document.getElementById('messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

function addMessage(text, isUser, metadata = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    textDiv.textContent = text;
    messageDiv.appendChild(textDiv);
    
    // Add metadata for bot messages
    if (!isUser && metadata) {
        const metaDiv = document.createElement('div');
        metaDiv.className = 'message-meta';
        
        let metaText = '';
        if (metadata.model) metaText += `Model: ${metadata.model} | `;
        if (metadata.context_count) metaText += `Sources: ${metadata.context_count} | `;
        if (metadata.total_tokens) metaText += `Tokens: ${metadata.total_tokens}`;
        
        metaDiv.textContent = metaText;
        messageDiv.appendChild(metaDiv);
        
        // Add sources if available
        if (metadata.sources && metadata.sources.length > 0) {
            const sourcesDiv = document.createElement('div');
            sourcesDiv.className = 'message-sources';
            sourcesDiv.innerHTML = '<strong>Sources:</strong> ' + metadata.sources.join(', ');
            messageDiv.appendChild(sourcesDiv);
        }
    }
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    
    addMessage(message, true);
    userInput.value = '';
    sendBtn.disabled = true;
    sendBtn.textContent = 'Thinking...';
    
    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message })
        });
        
        const data = await response.json();
        
        if (data.error) {
            addMessage(`Error: ${data.error}`, false);
        } else {
            addMessage(data.reply, false, {
                model: data.model,
                context_count: data.context_count,
                total_tokens: data.total_tokens,
                sources: data.sources
            });
        }
    } catch (error) {
        addMessage('Sorry, there was an error connecting to the server.', false);
        console.error('Error:', error);
    } finally {
        sendBtn.disabled = false;
        sendBtn.textContent = 'Send';
    }
}

async function checkHealth() {
    try {
        const response = await fetch(`${API_URL}/health`);
        const data = await response.json();
        
        if (data.knowledge_base_loaded) {
            addMessage(`✅ System ready! Loaded ${data.documents} documents with ${data.llm_model}`, false);
        } else {
            addMessage('⚠️ Knowledge base not loaded. Some features may not work.', false);
        }
    } catch (error) {
        addMessage('⚠️ Could not connect to server. Please check if the backend is running.', false);
    }
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    addMessage('🤖 Hi! I\'m your AI Coach Bot powered by NVIDIA NIMs. Ask me anything about BMX, fitness, or products!', false);
    checkHealth();
});
