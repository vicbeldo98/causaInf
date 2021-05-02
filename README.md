## Tool setup and initializaation

1.  Clone repository in local by executing: ```git clone https://github.com/vicbeldo98/dagitty.git```

2.  Place yourself inside the dagitty folder: ```cd dagitty```

3.  Install all the necessary requirementsfor the tool to work: ```pip3 install -r requisitos.txt```

4.  Start the flask service by executing the following command: ```python3 app.py```  

5. Go to (localhost:5000)[http://localhost:5000/] and you should be able to see the new DAGitty version!


## Tool usage

1.  Design a DAG depending of your case of study (specifying which will be the treatment and outcome nodes). You can also copy an existing graph you have saved. In folder LUCAS-EXAMPLE, copy the contents of lucas-graph.txt and paste them in the Model code section placed on the right of the tool. Finally, click on update DAG.

2.  Upload your data by clicking on Upload csv-> Choose file.... You must select a csv file which columns names match the node names you have used in your DAG.

3.  Two options from here: 
    1.  You can click on Compute with options and it will guide you through a dialog with several options
    2.  YOu can click on Compute from graph, which will compute the causal effect of the treatment node on the outcome node using machine learning, taking into account the adjusted nodes in the graph (if possible).