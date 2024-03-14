async function visualizarFoto(evento) {
  const files = evento.target.files;
  const archivo = files[0];
  let filename = archivo.name;
  let extension = filename.split(".").pop();
  extension = extension.tolowerCase();
  if (extension !== "jpg") {
    evento.target.value = "";
    swal.fire("Seleccionar", "La imagen debe ser en formato JPG", "warning");
  } else {
    const objectURL = URL.createObjectURL(archivo);
    imagenProducto.setAttribute("src", objectURL);
  }
}