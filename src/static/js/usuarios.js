function showPopup(message, type) {
    const popup = document.getElementById('usuarios-popup');
    popup.textContent = message;
    popup.className = `usuarios-popup ${type}`;
    popup.classList.add('show');

    setTimeout(() => {
        popup.classList.remove('show');
    }, 3000);
}

document.getElementById('usuarios-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const formData = new FormData(this);

    try {
        const response = await fetch('/adicionar_usuario', {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();

        if (response.ok) {
            showPopup(data.message, 'success');
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            showPopup(data.message, 'error');
        }
    } catch (error) {
        showPopup('Erro ao adicionar usuário', 'error');
    }

    this.reset();
});

async function excluirUsuario(userId) {
    if (!confirm('Tem certeza que deseja excluir este usuário?')) {
        return;
    }

    try {
        const response = await fetch(`/excluir_usuario/${userId}`, {
            method: 'POST',
        });

        const data = await response.json();

        if (response.ok) {
            showPopup(data.message, 'success');
            const userElement = document.querySelector(`li[data-id="${userId}"]`);
            if (userElement) {
                userElement.remove();
            }
        } else {
            showPopup(data.message, 'error');
        }
    } catch (error) {
        showPopup('Erro ao excluir usuário', 'error');
    }
}
