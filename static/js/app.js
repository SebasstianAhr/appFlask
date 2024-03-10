function abrirModalEliminar(idProducto){
    Swal.fire({
        title: 'Eliminar producto',
        text: 'Esta seguro de que quiere eliminar este producto',
        icon: 'Warning',
        showCancelButton: true,
        cinfirmButtonColor: '#3085d6',
        canselButtonColor: '#d33',
        cancelButtonText: 'NO',
        confirmButtonText: 'SI'
    }).then((result) => {
        if(result.isConfirmed){
            location.href='/eliminar/' +idProducto
        }
    })
}