function causalEffectPrompt(estimand, estimand_options) {
    return Swal.fire({
      title: '<strong>Estimation</strong>',
      icon: 'question',
      customClass: {input: 'my-radio'},
      input: 'radio',
      inputOptions: estimand_options,
      html: '<p><b>Please, choose a method in order to estimate the ATE</b></p>',
      showCloseButton: false,
      showCancelButton: false,
      focusConfirm: true,
      width: 'auto',
      showLoaderOnConfirm: true,
      preConfirm: (estimator) => {
        var formData = new FormData();
        formData.append('estimand_name', estimand);
        formData.append('estimation_method', estimator);

        return fetch(`/compute-effect-with-estimand-and-estimator`, {
          method: "POST",
          body: formData
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
    }).then((response)=> {
        treatment = response.value.treatment
        outcome = response.value.outcome
        effect = response.value.effect
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
        var pvalue;
        var htmlString = '<table border="1"><thead><tr><th>Refutation method</th><th>New effect</th><th>Procedure</th></tr></thead><tbody>';
        if (result.value) {
            for(const property in result.value) {
                if(property=="original"){
                  effect = result.value[property]
                }else if(property=="p-value"){
                  pvalue = result.value[property]
                }else{
                  htmlString = htmlString +  '<tr><th>' + property + '</th><th>' + result.value[property][0] + '</th><th>' + result.value[property][1] + '</th></tr>';
                }
            }
            htmlString = htmlString + '</tbody></table>';
            return Swal.fire({
                title: '<strong>Refutation</strong>',
                icon: 'info',
                html: '<h3>Original Causal effect : ' + effect + '</h3><h3>p-value : ' + pvalue + '</h3>' +  htmlString,
                showCloseButton: true,
                focusConfirm: false,
                confirmButtonText:'<i class="fa fa-thumbs-up" aria-hidden="true"></i> OK',
            });
        }
    })
  })
};
