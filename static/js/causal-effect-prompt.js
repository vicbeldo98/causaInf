function causalEffectPrompt(treatment, outcome, effect) {
    return Swal.fire({
        title: '<strong>Computed Causal Effect</strong>',
        icon: 'info',
        html: 'The causal effect ' + treatment + ' on ' + outcome + ' is ' + effect + '.<br>Do you wanna refute your model?<br>(This process may take a few minutes).',
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
              return response.json();
            })
            .catch(error => {
              Swal.showValidationMessage(
                `Request failed: ${error}`
              )
            })
        },
        allowOutsideClick: () => !Swal.isLoading()
    }).then((result, effect) => {
      var effect;
      var htmlString = '<table border="1"><thead><tr><th>Refutation method</th><th>New effect</th><th>Procedure</th></tr></thead><tbody>';
      if (result.value) {
          for(const property in result.value) {
              if(property=="original"){
                effect = result.value[property]
              }else{
                htmlString = htmlString +  '<tr><th>' + property + '</th><th>' + result.value[property][0] + '</th><th>' + result.value[property][1] + '</th></tr>';
              }
          }
          htmlString = htmlString + '</tbody></table>';
          return Swal.fire({
              title: '<strong>Refutation</strong>',
              icon: 'info',
              html: '<h3>Original Causal effect : ' + effect + '</h3>' + htmlString,
              showCloseButton: true,
              focusConfirm: false,
              confirmButtonText:'<i class="fa fa-thumbs-up" aria-hidden="true"></i> OK',
          });
      }
  })
}



