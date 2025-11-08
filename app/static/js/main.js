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

    // Handler para o modal de novo suporte (modalNovoSuporte) - inicializa/limpa ao abrir
    let modalNovoSuporte = document.getElementById('modalNovoSuporte');
    if (modalNovoSuporte) {
        modalNovoSuporte.addEventListener('show.bs.modal', function (event) {
            let form = modalNovoSuporte.querySelector('form#modalNovoSuporte-form');
            if (!form) return;
            
            form.reset();

            // se o modal foi aberto a partir de um botão com data-attributes, preencha alguns campos
            let trigger = event && event.relatedTarget ? event.relatedTarget : null;
            if (trigger && trigger.dataset) {
                // Preencher campos hidden com informações do equipamento
                ['id_equipamento', 'patrimonio', 'marca', 'modelo'].forEach(field => {
                    let input = form.querySelector(`input[name="${field}"]`);
                    if (input && trigger.dataset[field]) {
                        input.value = trigger.dataset[field];
                    }
                });

                // Atualizar a exibição do texto do equipamento
                // let span = form.querySelector('.equipamento-info');
                // if (span) {
                //     let patrimonioInput = form.querySelector('input[name="patrimonio"]');
                //     let marcaInput = form.querySelector('input[name="marca"]');
                //     let modeloInput = form.querySelector('input[name="modelo"]');

                //     let displayText = patrimonioInput.value || '';
                //     if (marcaInput.value) displayText += ' - ' + marcaInput.value;
                //     if (modeloInput.value) displayText += ' ' + modeloInput.value;
                    
                //     span.textContent = displayText;
                // }
            }

            // definir data padrão se vazio
            let dataInput = form.querySelector('input[name="data_suporte"]');
            if (dataInput && !dataInput.value) {
                let today = new Date().toISOString().slice(0,10);
                dataInput.value = today;
            }

            let first = form.querySelector('input, select, textarea');
            if (first) first.focus();
        });
    }
});
