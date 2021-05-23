function causalEffect(estimand, estimator){
   $.ajax({
      url: '/compute-effect-with-estimand-and-estimator', 
      type:'POST',
      data: {'estimand_name': estimand, 'estimation_method':estimator},
      success: function(response){
         causalEffectPrompt(response['treatment'], response['outcome'], response['effect']);
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

function identificationOptions(graph, treatment, outcome, callback){
   $.ajax({
      url: '/retrieve-identification-options', 
      type:'POST',
      data: {
         'graph': graph,
         'treatment': treatment.toString(),
         'outcome': outcome.toString(),
      },
      success: function(response){
         callback(response);
      },
      error: function(req, status, error){
         errorPrompt(req.responseText);
      }
   })
}