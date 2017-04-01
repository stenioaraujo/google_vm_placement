#### Universidade Federal de Campina Grande

##### Curso Ciência da Computação

##### Disciplina
- Metodologia Científica

##### Professora
- Raquel Vigolvino Lopes

##### Alunos:

- Brendha Cruz Silva
- Stenio Araújo

Referente ao periodo **2016.2**

#### Install the requirements
    pip install -r requirements.txt

#### Run the example
    python3 example_execution.py

#### Run the tests
From the root of the repository (**google_vm_placement**), run the following
 command:

    python3 -m unittest discover -v

#### Run the experiments
The file **generate_inputs.py** and **experiment_inputs.txt** are responsible for
the inputs that will be used by the file **run_all_experiments.sh**.

**run_all_experiments.sh** uses **GNU Parallel**, so all the available cpus will be used.

Once you have the **experiment_inputs.txt** filled up with the inputs for the experiment, you may run it:

    ./run_all_experiments.py

The script will save the results in **experiment_results.csv**
