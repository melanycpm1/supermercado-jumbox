function abrirModalUsuario(id, nombre, apellido, email, rol, sucursal) {
        // llenar inputs
        document.getElementById('edit_id').value = id;
        document.getElementById('edit_nombre').value = nombre;
        document.getElementById('edit_apellido').value = apellido;
        document.getElementById('edit_email').value = email;
        document.getElementById('edit_contrasena').value = "";
        document.getElementById('edit_rol').value = rol;
        document.getElementById('edit_sucursal').value = sucursal;

        // actualizar action del formulario
        document.getElementById("formEditar").action = "/editar_usuario/" + id;

        // abrir modal
        let modal = new bootstrap.Modal(document.getElementById('modalEditar'));
        modal.show();
    }