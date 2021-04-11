function causalEffectPrompt(treatment, outcome, effect) {
    return Swal.fire({
        title: '<strong>Computed Causal Effect</strong>',
        icon: 'info',
        html:
            'The causal effect ' + treatment + ' on ' + outcome + ' is ' + effect + '<br>. Do you wanna refute your model?',
        showCloseButton: true,
        showCancelButton: true,
        focusConfirm: false,
        confirmButtonText:'Refute',
     }).then((result) => {
        if (result.isConfirmed) {
            refutationTests();
        }
     });
}
