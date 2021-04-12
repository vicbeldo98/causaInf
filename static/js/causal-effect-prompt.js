function causalEffectPrompt(treatment, outcome, effect) {
    return Swal.fire({
        title: '<strong>Computed Causal Effect</strong>',
        icon: 'info',
        html: 'The causal effect ' + treatment + ' on ' + outcome + ' is ' + effect + '<br>. Do you wanna refute your model?',
        showCancelButton: true,
        confirmButtonText: 'Refute',
        showLoaderOnConfirm: true,
        preConfirm: () => {
          return fetch(`/refutation-tests`, {
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
            method: "POST",
            })
            .then(response => {
              if (!response.ok) {
                throw new Error(response.statusText)
              }
              return response.json()
            })
            .catch(error => {
              Swal.showValidationMessage(
                `Request failed: ${error}`
              )
            })
        },
        allowOutsideClick: () => !Swal.isLoading()
    }).then((result) => {
        if (result.value) {
            html = '<ul>'
            for(const property in result.value) {
                html = html +  '<li>' + result.value[property] + '</li>'
            }
            html = html +'<ul>'
            return Swal.fire({
                title: '<strong>Refutation Results</strong>',
                icon: 'info',
                html: html,
                showCloseButton: true,
                focusConfirm: false,
                confirmButtonText:'<i class="fa fa-thumbs-up" aria-hidden="true"></i> OK',
            });
        }
    })
}

function simpleCausalEffectPrompt(treatment, outcome, effect) {
  return Swal.fire({
      title: '<strong>Computed Causal Effect</strong>',
      icon: 'info',
      html: 'The causal effect ' + treatment + ' on ' + outcome + ' is ' + effect,
      confirmButtonText:'<i class="fa fa-thumbs-up" aria-hidden="true"></i> OK',
  });
}



