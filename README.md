# AC215_HiSolver

## Project Organization

      ├── LICENSE
      ├── README.md
      ├── notebooks
      ├── references
      ├── requirements.txt
      ├── setup.py
      └── src
            ├── collection
            │     ├── README.md
            │     ├── Dockerfile
            │     ├── preprocess.py
            │     └── requirements.txt
            |── preprocessing
            |     ├── README.md
            |     ├── Dockerfile
            |     ├── preprocessing.py
            |     └── requirements.txt
            |── data-versioning
            |     ├── README.md
            |     ├── docker-shell.bat
            |     ├── docker-shell.sh
            |     ├── Dockerfile
            |     ├── Pipfile
            |     ├── Pipfile.lock
            |     ├── processed_dataset.dvc
            |     ├── processed_dataset
            |     └── cli.py
            |── training
            |     ├── README.md
            |     ├── Dockerfile
            |     ├── training.py
            |     └── requirements.txt
            └── deployment
                  ├── README.md
                  ├── Dockerfile
                  ├── deployment.py
                  └── requirements.txt

---

## Project Intro

**Team Members:**
Yan Kaled, Tom Zhang, Tadhg Looram, Mina Lee, Jason Xiang, Nishtha Sardana & Kareema Batool

**Group Name:**
HiSolver

**Project:**
In this project, we are fine-tuning an LLM for an animation engine (specifically Python package Manim). The goal is to develop an AI application powered by an LLM that can receive user input in the form of raw text consisting of mathematical problems at the SAT level. The application should provide step-by-step solutions or hints for the student - as well as generate Python code for the animation engine. One major challenge would be to construct and fine-tune the said LLM.

## Milestone Tracking

### Milestone 2

Our proposed data pipeline has 4 major steps: data collection, data pre-processing, LLM fine-tuning, and model deployment. For this milestone, we will be solely focusing on the first two components.

#### 1. Data Collection

See `src/collection/README.md` for an in-depth description of how to set up this component of the pipeline.

At this stage, we are using a container to run a python script that scrapes data from GitHub API. The scraper looks for all GitHub repositories containing the keyword "manim" (the animation engine Python package). For each repository, we collect all the Python files, then store them in a Google Cloud Storage (GCS) Bucket.

As of 09/26/2023, there are approximately 2,400 such repositories of interest. It takes approximately 1 second to collect and upload 3 Python files to the GCS bucket.

All files will be stored within the `raw/` folder on the bucket, while preserving directory structure from the original repositories from which they were extracted.

#### 2. Data Pre-processing

See `src/preprocessing/README.md` for an in-depth description of how to set up this component of the pipeline.

Note that not all Python files we collected from the last step are relevant. We are only interested in those that contain code examples of actually using the Manim package. So at this step, we will first be filtering for relevant Python files by looking for appropriate import statements. Then we perform standard text preprocessing procedures for NLP such as tokenization, encoding, etc. To optimize speed, we're currently ignoring any subdirectory with more than 20 Python files.

At the end, the processed data will be stored in the `processed/` folder on the bucket. The directory structure will be exactly the same, except that each Python file will have a `.json` appendix - as we would have transformed the Python file content into JSON files. Each JSON file has the following structure:

```json
[
  {
    "input": "# `` .animate '' syntax :",
    "output": "self.play ( grid.animate.shift ( LEFT ) )"
  },
  {
    "input": "# Tex to color map",
    "output": "t2c = { `` A '' : BLUE , `` B '' : TEAL , `` C '' : GREEN , }"
  }
]
```

This will be our training data for fine-tuning the LLM - prompt and its expected output. For now, we've created the prompts by simply extracting the code comments from our scraped Python files. More refinements can be implemented in a later milestone.

#### 3. Data versioning

See `src/data-versioning/README.md` for an in-depth description of how to set up this component of the pipeline.

This Python-scripted Docker container is orchestrated to securely download and manage processed data from a designated Google Cloud Storage bucket, aimed at implementing Data Version Control (DVC) on the cloud. Initiated by a shell script, the container interfaces with the Google Cloud environment, pulling relevant data blobs and ensuring their organized local placement, thus facilitating streamlined, secure, and orderly data retrieval and versioning workflows within cloud-based storage solutions.

All files will be stored within the `dvc_store/` folder on the bucket, while preserving directory structure from the original repositories from which they were extracted.

#### 4. LLM Fine-tuning

For a future milestone.

#### 5. Model Deployment

Also for a future milestone.

### Milestone 3

We improved upon existing components from the previous milestone as well as implemented new components of our data pipeline. The following are the tasks we accomplished for this milestone.

#### 1. Data Pre-processing (Continued)

See `src/preprocessing/README.md` for an in-depth description of how to set up this component of the pipeline.

We changed up the logic a bit since last time: now we are parsing each python file to extract all class definition code snippets (as that's essentially how Manim animations are defined). We separate code snippets into their own JSON files, each with the following structure:

```json
{
  "data": {
    "code": "class DrawCircle(Scene):\n    def construct(): pass"
  }
}
```

Note that at this step we're only worried about extracting the code snippets. Fine-tuning an LLM would also require the input prompt associated with those code outputs. For quality assurance, we will be using Label Studio for humans to manually provide those code summaries. We will describe how to set up Label Studio in the next section.

#### 2. Data Labeling

See `src/data-labeling/README.md` for an in-depth description of how to set up this component of the pipeline.

This component of the pipeline involves setting up a Label Studio web app so that users can manually provide summaries to those code snippets we previously processed.

#### 3. Training [TODO - only thing left for this milestone]

- TODO get labeled data then use TF data/records to prep input for training
- TODO use GCP's Vertex AI to do
  - experiment tracking
  - hyperparameter tuning
  - serverless training

#### 4. DVC

TODO some comment on DVC - cause our commit last time was past the deadline

#### 5. Summary

TODO this is the updated data pipeline: TODO list components, etc.

#### Aside

- FIXME Copying the secrets folder everywhere is not good practice; might need to look into docker-compose instead of Dockerfile because volume mounting with relative path doesn't work for Dockerfile
- FIXME preprocessing.py is kinda slow - the last part... parhaps save locally then bulk upload?
