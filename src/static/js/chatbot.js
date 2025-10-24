document.addEventListener('DOMContentLoaded', () => {
    const chatIcon = document.getElementById('chat-icon');
    const chatWindow = document.getElementById('chat-window');
    const closeChat = document.getElementById('close-chat');
    const chatHeader = document.getElementById('chat-header');

    // Função para tornar um elemento arrastável
    const makeDraggable = (element, dragHandle) => {
        let offsetX, offsetY, isDragging = false;

        dragHandle.addEventListener('mousedown', (e) => {
            isDragging = true;
            offsetX = e.clientX - element.getBoundingClientRect().left;
            offsetY = e.clientY - element.getBoundingClientRect().top;
            dragHandle.style.cursor = 'grabbing';
        });

        document.addEventListener('mousemove', (e) => {
            if (!isDragging) return;

            let newX = e.clientX - offsetX;
            let newY = e.clientY - offsetY;

            // Limitar o movimento dentro da janela de visualização
            const maxX = window.innerWidth - element.offsetWidth;
            const maxY = window.innerHeight - element.offsetHeight;

            element.style.left = `${Math.max(0, Math.min(newX, maxX))}px`;
            element.style.top = `${Math.max(0, Math.min(newY, maxY))}px`;
            // Remove bottom/right para que left/top funcione
            element.style.bottom = 'auto';
            element.style.right = 'auto';
        });

        document.addEventListener('mouseup', () => {
            isDragging = false;
            dragHandle.style.cursor = 'move';
        });
    };

    // Tornar o ícone e a janela do chat arrastáveis
    makeDraggable(chatIcon, chatIcon);
    makeDraggable(chatWindow, chatHeader);

    // Abrir a janela do chat
    chatIcon.addEventListener('click', (e) => {
        // Evita que o evento de arraste dispare o clique
        if (e.target.style.cursor === 'grabbing') return;
        
        if (chatWindow.style.display === 'none' || chatWindow.style.display === '') {
            chatWindow.style.display = 'flex';
        } else {
            chatWindow.style.display = 'none';
        }
    });

    // Fechar a janela do chat
    closeChat.addEventListener('click', () => {
        chatWindow.style.display = 'none';
    });
});
