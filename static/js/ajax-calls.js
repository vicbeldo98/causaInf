function causalEffect(estimand){
    $.ajax({
        url: '/compute-effect-with-estimand', 
        type:'POST',
        data: {'estimand_name': estimand},
        success: function(response){
           causalEffectPrompt(response['treatment'],response['outcome'],response['effect']);
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
           callback(response);
        },
        error: function(req, status, error){
          errorPrompt(req.responseText);
        }
     });
}

function estimate(estimand, estimation-method){
    $.ajax({
        url: '/compute-estimation-methods', 
        type:'POST',
        data: {'estimand_name': estimand},
        success: function(response){
           callback(response);
        },
        error: function(req, status, error){
          errorPrompt(req.responseText);
        }
     });
}