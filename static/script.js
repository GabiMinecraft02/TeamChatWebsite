const pseudo = window.pseudo; // si défini via Flask
const socket = io();

function envoyer() {
    const content = document.getElementById("content").value;
    if (!content) return;
    socket.send({ pseudo, content });
    document.getElementById("content").value = "";
}

socket.on("message", (data) => {
    const li = document.createElement("li");
    li.textContent = data.pseudo + " : " + data.content;
    document.getElementById("messages").appendChild(li);
});
