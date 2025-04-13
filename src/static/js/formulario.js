document.addEventListener("DOMContentLoaded", function () {
    const cepInput = document.getElementById("cep");
    cepInput.addEventListener("blur", function () {
        const cep = cepInput.value.replace(/\D/g, "");
        if (cep.length === 8) buscarEndereco(cep);
    });

    const telefoneInput = document.getElementById("telefone");
    telefoneInput.addEventListener("blur", function () {
        validatePhone(telefoneInput);
    });

    document.getElementById("formulario-inscricao").addEventListener("submit", async function (event) {
        event.preventDefault(); // Previne o envio padrão do formulário

        const courseSelect = document.getElementById("course");
        if (validateCourse(courseSelect)) {
            // Aqui você pode enviar o formulário via AJAX ou fazer um fetch
            const formData = new FormData(this);
            try {
                const response = await fetch(this.action, {
                    method: this.method,
                    body: formData,
                });

                if (response.ok) {
                    // Se a resposta for bem-sucedida, mostre o modal
                    showModal();
                } else {
                    // Caso contrário, exiba uma mensagem de erro
                    alert("Erro ao enviar a inscrição. Tente novamente.");
                }
            } catch (error) {
                alert("Erro ao enviar a inscrição. Tente novamente.");
            }
        }
    });
});

function validatePhone(input) {
    const phonePattern = /^\d{10,11}$/;
    const isValid = phonePattern.test(input.value);
    document.getElementById('phone-error').style.display = isValid ? "none" : "block";
}

function validateCourse(select, event) {
    if (select.value === "") {
        document.getElementById("course-error").style.display = "block";
        event.preventDefault();
        return false;
    }
    return true;
}

async function buscarEndereco(cep) {
    try {
        const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
        const data = await response.json();
        if (data.erro) alert("CEP não encontrado.");
        else {
            document.getElementById("rua").value = data.logradouro;
            document.getElementById("cidade").value = data.localidade;
            document.getElementById("estado").value = data.uf;
        }
    } catch {
        alert("Erro ao buscar endereço.");
    }
}

function showModal() {
    document.getElementById("modal-confirmacao").style.display = "block";
}

function closeModal() {
    document.getElementById("modal-confirmacao").style.display = "none";
}

function concluir() {
    window.location.href = "/";
}

function novaInscricao() {
    closeModal();
    document.getElementById("formulario-inscricao").reset();
}
