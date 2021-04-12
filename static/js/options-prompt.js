function optionsPrompt(title, subtitle, inputOptions) {
    return Swal.fire({
        title: '<strong>' + subtitle +'</strong>',
        icon: 'question',
        customClass: {input: 'my-radio'},
        input: 'radio',
        inputOptions: inputOptions,
        html: '<p><b>' + title + '</b></p>',
        showCloseButton: false,
        showCancelButton: false,
        focusConfirm: true,
        width: 'auto'
    });
}