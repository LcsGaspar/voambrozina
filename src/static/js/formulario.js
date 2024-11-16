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

    document.getElementById("registration-form").addEventListener("submit", function (event) {
        validateCourse(document.getElementById("course"), event);
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
    }
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
    document.getElementById("confirmationModal").style.display = "block";
}

function closeModal() {
    document.getElementById("confirmationModal").style.display = "none";
}

function concluir() {
    window.location.href = "/";
}

function novaInscricao() {
    closeModal();
    document.getElementById("registration-form").reset();
}
