# CausaInf

CausaInf is a tool that provides a way of making causal inference based on causal diagrams.
Visual and dynamically, it tries to help enterprises and people analyze their data.

This tool relies mainly on two causal inference technologies: [DAGitty](http://www.dagitty.net/) and [DoWhy](https://microsoft.github.io/dowhy/) (created and mantained by Microsoft).

DoWhy is used under the MIT License:

 MIT License

    Copyright (c) Microsoft Corporation. All rights reserved.

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE

Basically, using the interface and functionality provided by DAGitty, we have added some functionalities (those remarked in red colour) that internally use DoWhy in order to ease the process of making causal inference.

![CausaInf](https://user-images.githubusercontent.com/49116334/131493260-40d4aa8d-6a88-4395-a5e4-4190775a53a6.jpg)

You can choose the variables you want to adjust, and the estimation method. Available estimation methods are:
1.  Double Machine Learning
2.  Linear Regression
3.  Propensity Score Matching
4.  Propensity Score Stratification

Optional refutation methods and p-values provided if needed.

# Usage
#### Install on Ubuntu
Install Poetry in Linux/Ubuntu:
```pip3 install poetry```

#### Tool setup and initializaation

1.  Clone repository in local by executing: ```git clone https://github.com/vicbeldo98/dagitty.git```

2.  Place yourself inside the dagitty folder: ```cd dagitty```

4.  Run ``` poetry install``` in order to resolve all the necessary requirements for for the tool to work. 

4.  Start the flask service by executing the following command: ```poetry run python3 app.py```

5. Go to [localhost:5000](http://localhost:5000/) and you should be able to see the new DAGitty version!


#### Tool usage

1.  Design a DAG depending of your case of study (specifying which will be the treatment and outcome nodes). You can also copy an existing graph you have saved. In folder LUCAS-EXAMPLE, copy the contents of lucas-graph.txt and paste them in the Model code section placed on the right of the tool. Finally, click on update DAG.

2.  Upload your data by clicking on Upload csv-> Choose file.... You must select a csv file which columns names match the node names you have used in your DAG.

3.  You can click on Compute ATE and it will guide you through a dialog with several options
