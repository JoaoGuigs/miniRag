const apiBase = "http://localhost:8000";

const uploadForm = document.getElementById("upload-form");
const fileInput = document.getElementById("pdf-file");
const uploadStatus = document.getElementById("upload-status");

const chatForm = document.getElementById("chat-form");
const questionInput = document.getElementById("question");
const chatResponse = document.getElementById("chat-response");

uploadForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (!fileInput.files[0]) {
    uploadStatus.textContent = "Selecione um PDF primeiro.";
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  uploadStatus.textContent = "Enviando e indexando PDF...";

  try {
    const res = await fetch(`${apiBase}/upload`, {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    uploadStatus.textContent = data.message || "PDF enviado com sucesso.";
  } catch (err) {
    console.error(err);
    uploadStatus.textContent = "Erro ao enviar PDF.";
  }
});

let sessionId = localStorage.getItem("sessionId") || null;
if(!sessionId) {
  sessionId = crypto.randomUUID();
  localStorage.setItem("sessionId", sessionId);
}
chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const pergunta = questionInput.value.trim();
  if (!pergunta) return;

  chatResponse.textContent = "Perguntando ao modelo...";

  try {
    // FastAPI define `pergunta` como parâmetro simples, então mandamos como query string mesmo usando POST
    const res = await fetch(
      `${apiBase}/chat?pergunta=${encodeURIComponent(pergunta)}&session_id=${encodeURIComponent(sessionId)}`,
      { method: "POST" }
    );

    const data = await res.json();
    chatResponse.textContent = data.response ?? "(sem resposta)";
  } catch (err) {
    console.error(err);
    chatResponse.textContent = "Erro ao perguntar ao modelo.";
  }
});