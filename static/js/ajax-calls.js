function causalEffect(estimand, estimator){
    $.ajax({
        url: '/compute-effect-with-estimand-and-estimator', 
        type:'POST',
        data: {'estimand_name': estimand, 'estimation_method':estimator},
        success: function(response){
           causalEffectPrompt(response['treatment'], response['outcome'], response['effect'], refutationTests);
        },
        error: function(req, status, error){
          errorPrompt(req.responseText);
        }
     });
}

function estimationMethods(estimand, callback){
    $.ajax({
        url: '/compute-estimation-methods', 
        type:'POST',
        data: {'estimand_name': estimand},
        success: function(response){
           callback(estimand, response);
        },
        error: function(req, status, error){
          errorPrompt(req.responseText);
        }
     });
}

function refutationTests(){
   $.ajax({
       async: false,
       url: '/refutation-tests', 
       type:'POST',
       success: function(response){
         html = '<ul>'
         for(const property in response) {
            html = html +  '<li>' + response[property] + '</li>'
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
       },
       error: function(req, status, error){
         errorPrompt(req.responseText);
       },
    });
}