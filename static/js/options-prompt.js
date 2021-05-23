function optionsPrompt(title, subtitle, inputOptions) {
    return Swal.fire({
        title: '<strong>' + title +'</strong>',
        icon: 'question',
        customClass: {input: 'my-radio'},
        input: 'radio',
        inputOptions: inputOptions,
        html: '<p><b>' + subtitle + '</b></p>',
        showCloseButton: false,
        showCancelButton: false,
        focusConfirm: true,
        width: 'auto'
    });
}