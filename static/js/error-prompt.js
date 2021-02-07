function errorPrompt(errorMsg) {
   return Swal.fire({
      title: '<strong>Oooops!</strong>',
      icon: 'error',
      html:
         errorMsg,
      showCloseButton: false,
      showCancelButton: false,
      focusConfirm: false,
      confirmButtonText:'<i class="fa fa-thumbs-down" aria-hidden="true"></i> OK',
   })
}