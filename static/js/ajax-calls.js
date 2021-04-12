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