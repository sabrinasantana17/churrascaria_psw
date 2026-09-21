/*
 * churrascaria.js
 * Pequenos ajustes para o tema SB Admin 2 funcionar bem com os forms
 * padrão do Django ({{ form.as_p }}) sem precisar instalar pacotes extras
 * (django-widget-tweaks / crispy-forms).
 */
(function () {
    "use strict";

    document.addEventListener("DOMContentLoaded", function () {

        // 1) Aplica classes do Bootstrap nos campos gerados pelo Django
        document.querySelectorAll("form.django-form input, form.django-form select, form.django-form textarea")
            .forEach(function (field) {
                var type = (field.getAttribute("type") || "").toLowerCase();

                if (type === "checkbox" || type === "radio") {
                    field.classList.add("form-check-input");
                } else if (type === "submit" || type === "button") {
                    // botões já são estilizados manualmente
                } else {
                    field.classList.add("form-control");
                }
            });

        // 2) Envolve cada <p> do form.as_p num espaçamento consistente
        document.querySelectorAll("form.django-form p").forEach(function (p) {
            p.classList.add("form-group");
        });

        // 3) Ativa o DataTables (busca/paginação/ordenação) nas tabelas marcadas
        if (window.jQuery && jQuery.fn.DataTable) {
            jQuery(".datatable").DataTable({
                language: {
                    search: "Buscar:",
                    lengthMenu: "Mostrar _MENU_ registros",
                    info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
                    infoEmpty: "Nenhum registro encontrado",
                    infoFiltered: "(filtrado de _MAX_ registros no total)",
                    paginate: { previous: "Anterior", next: "Próximo" },
                    zeroRecords: "Nenhum resultado encontrado"
                }
            });
        }
    });
})();
