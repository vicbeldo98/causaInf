# Install Poetry in Linux/Ubuntu:
```pip3 install poetry```

## Tool setup and initializaation

1.  Clone repository in local by executing: ```git clone https://github.com/vicbeldo98/dagitty.git```

2.  Place yourself inside the dagitty folder: ```cd dagitty```

4.  Run ``` poetry install``` in order to resolve all the necessary requirements for for the tool to work. 

4.  Start the flask service by executing the following command: ```poetry run python3 app.py```

5. Go to [localhost:5000](http://localhost:5000/) and you should be able to see the new DAGitty version!


## Tool usage

1.  Design a DAG depending of your case of study (specifying which will be the treatment and outcome nodes). You can also copy an existing graph you have saved. In folder LUCAS-EXAMPLE, copy the contents of lucas-graph.txt and paste them in the Model code section placed on the right of the tool. Finally, click on update DAG.

2.  Upload your data by clicking on Upload csv-> Choose file.... You must select a csv file which columns names match the node names you have used in your DAG.

3.  You can click on Compute ATE and it will guide you through a dialog with several options
