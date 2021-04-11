function causalEffectPrompt(treatment, outcome, effect) {
    return Swal.fire({
        title: '<strong>Computed Causal Effect</strong>',
        icon: 'info',
        html:
            'The causal effect ' + treatment + ' on ' + outcome + ' is ' + effect,
        showCloseButton: false,
        showCancelButton: false,
        focusConfirm: false,
        confirmButtonText:'<i class="fa fa-thumbs-up" aria-hidden="true"></i> OK',
     });
}