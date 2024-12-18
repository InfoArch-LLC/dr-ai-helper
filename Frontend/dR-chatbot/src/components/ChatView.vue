<template>
  <div class="chat-container">
    <!-- Container for Api response -->
    <div class="response-container" v-if="response" v-html="formattedResponse"></div>
    
    <!-- Loading message -->
    <p v-if="loading" class="loading-text"> Generating response...</p>
    <p v-if="error" class="error">{{ error }}</p>

    <!-- Container for sending message -->
    <div class="input-container">
      <textarea
        class="promptarea"
        v-model="prompt"
        placeholder="Ask me something..."
        @keydown.enter="generateResponse"
      ></textarea>
      <button @click="generateResponse">Send</button>
    </div>
  </div>
</template>
  
<script>
import axios from "axios";
import hljs from "highlight.js";
import "highlight.js/styles/atom-one-light.css"; // Code theme
import { marked } from "marked";

export default {
  data() {
    return {
      prompt: "",
      response: "",
      loading: false,
      error: "",
    };
  },
  computed: {
    formattedResponse() {
      if (!this.response) return "";

      marked.setOptions({
        breaks: true,
        gfm: true,
      });

      const responseWithHighlightedCode = this.response.replace(
        /```(.*?)```/gs, // Regex to identify embedded code
        (match, code) => {
          const highlightedCode = hljs.highlightAuto(code).value;
          return `<pre><code class="hljs">${highlightedCode}</code></pre><br/>`;
        }
      );

      return marked(responseWithHighlightedCode);
    },
  },
  methods: {
    async generateResponse() {
      if (!this.prompt) {
        this.error = "Please enter a prompt.";
        return;
      }
      this.response = "";
      this.error = "";
      this.loading = true;

      try {
        const api_url = "http://127.0.0.1:8080/api/llm/ask_storage"; // API URL
        const headers = { "Content-Type": "application/json" };
        const data = { query: this.prompt };

        const res = await axios.post(api_url, data, { headers });

        if (res.status === 200) {
          this.response = res.data.answer;
        } else {
          this.error = "Error Getting API Data";
        }
      } catch (err) {
        this.error = "Failed to fetch data from the API.";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.chat-container{
  width: 80vw;
}

.response-container{
  max-width: 80vw;
  background-color: #f6f8fa;
  padding: 20px;
  border-radius: 10px;
  overflow-x: auto;
  margin: 5vh 0 20vh 0;
  text-align: left;
}

.response-container pre {
  background-color: #f6f8fa;
  border-radius: 10px;
  overflow-x: auto;
}

.response-container code {
  font-family: "Courier New", Courier, monospace;
}

.input-container {
  display: flex;
  align-items: center;
  max-width: 80vw;
  gap: 10px;
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  background-color: #fff;
  z-index: 10;
}

.promptarea {
  flex-grow: 1;
  min-width: 70vw;
  min-height: 20vh;
  padding: 10px;
  font-size: 14px;
  margin-bottom: 10px;
  margin-top: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
  resize: vertical;
}

button {
  background-color: #3498db;
  width: 25vw;
  height: 7vh;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #2980b9;
}

button:active {
  background-color: #206a89;
}

/* Widget styles */
@media (max-width: 400px) and (max-height: 600px) {
  .input-container {
    width: 100vw;
    left: 0;
    transform: none;
    padding: 0 10px;
  }
  .main-logo {
    width: 200px;
  }
}
</style>
