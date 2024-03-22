//eliminar producto.

document.addEventListener('DOMContentLoaded', function () {
  const trash = document.querySelectorAll('.fa-trash');
  trash.forEach(icon => {
      icon.addEventListener('click', function (event) {
          event.preventDefault();

          const productId = this.getAttribute('data-id');

          Swal.fire({
              title: '¿Estás seguro de querer eliminar este producto?',
              icon: 'warning',
              showCancelButton: true,
              confirmButtonText: 'Sí',
              cancelButtonText: 'Cancelar'
          }).then((result) => {
              if (result.isConfirmed) {
                  window.location.href = '/eliminarProducto/' + productId;
              }
          });
      });
  });
});

// editar producto.

document.addEventListener('DOMContentLoaded', function () {
  const edit = document.querySelectorAll('.fa-edit');
  edit.forEach(icon => {
      icon.addEventListener('click', function (event) {
          event.preventDefault();

          const productId = this.getAttribute('data-id');

          Swal.fire({
              title: '¿Estás seguro de querer editar este producto?',
              icon: 'warning',
              showCancelButton: true,
              confirmButtonText: 'Sí',
              cancelButtonText: 'Cancelar'
          }).then((result) => {
              if (result.isConfirmed) {
                  window.location.href = '/editarProducto/' + productId;
              }
          });
      });
  });
});


function cancelarRegistro() {
  window.location.href = '/iniciarSesion';
}

// visualizar la foto
function visualizarFoto(event) {
  imagenProducto = document.getElementById('imagenProducto');
  
  if (event.target.files && event.target.files[0]) {
      var reader = new FileReader();

      reader.onload = function (e) {
          imagenProducto.src = e.target.result;
      }

      reader.readAsDataURL(event.target.files[0]);
  } else {
      imagenProducto.src = '';
  }
}