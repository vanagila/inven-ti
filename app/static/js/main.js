// scripts comuns para a aplicação
// visualizar senha
window.togglePassword = function() {
    var input = document.getElementById('senha');
    var icon = document.getElementById('toggleIcon');
    if (!input || !icon) return;
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.replace('fa-eye-slash', 'fa-eye');
    }
};

// Espera DOM pronto e registra handlers de modal
document.addEventListener('DOMContentLoaded', function () {
    let modalEditar = document.getElementById('modalEditar');
    if (modalEditar) {
        modalEditar.addEventListener('show.bs.modal', function (event) {
            let button = event && event.relatedTarget ? event.relatedTarget : null;
            if (!button) return;

            let form = document.getElementById('modalEditar-form');
            if (!form) return;

            let fields = ['patrimonio','tipo','marca','modelo','numero_serie','localizacao','data_aquisicao','status','observacoes'];
            fields.forEach(function(name){
                let el = form.querySelector('[name="'+name+'"]');
                if (!el) return;

                let val = button.dataset && typeof button.dataset[name] !== 'undefined' ? button.dataset[name] : button.getAttribute('data-'+name);
                if (val === null || typeof val === 'undefined') val = '';

                if (el.tagName.toLowerCase() === 'select'){
                    for (let i=0;i<el.options.length;i++){
                        el.options[i].selected = (el.options[i].value === val) || (el.options[i].text === val);
                    }
                } else {
                    el.value = val;
                }
            });

            let updateUrl = (button.dataset && button.dataset.updateUrl) ? button.dataset.updateUrl : button.getAttribute('data-update-url');
            if (updateUrl) {
                form.action = updateUrl;
            }
        });
    }

    // Handler para o modal de novo suporte (modalNovoSuporte)
    const modal = document.getElementById('modalSuporte');
    const form = document.getElementById('formSuporte');
    const title = modal.querySelector('.modal-title');
    const btnSalvar = document.getElementById('btnSalvar');

    modal.addEventListener('show.bs.modal', event => {
        const button = event.relatedTarget;
        const mode = button.getAttribute('data-mode');
        const action = button.getAttribute('data-action') || '';

    // Limpa o form
    form.reset();
    form.action = action;
    form.querySelectorAll('input, select, textarea').forEach(el => el.removeAttribute('readonly'));
    btnSalvar.style.display = 'inline-block';
    btnSalvar.disabled = false;

    // Preenche campos se for edição ou visualização
    if (mode === 'edit' || mode === 'view') {
      ['id', 'data_suporte', 'tipo_suporte', 'responsavel', 'custo', 'descricao'].forEach(field => {
        const input = form.querySelector(`[name="${field}"]`);
        if (input && button.dataset[field]) {
            input.value = button.dataset[field];
        }
      });
    }

    // Ajusta título e comportamento
    if (mode === 'create') {
        title.textContent = 'Registrar Suporte';
    } else if (mode === 'edit') {
        title.textContent = 'Editar Suporte';
    } else if (mode === 'view') {
        title.textContent = 'Detalhes do Suporte';
        form.querySelectorAll('input, select, textarea').forEach(el => el.setAttribute('readonly', true));
        btnSalvar.style.display = 'none';
    }
    });
});
