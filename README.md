# AC215_HiSolver (Milestone2)

AC215 - Milestone2

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

## AC215 - Milestone2 - HiSolver

### Project Intro

**Team Members**
Yan Kaled, Tom Zhang, Tadhg Looram, Mina Lee, Jason Xiang, Nishtha Sardana & Kareema Batool

**Group Name**
HiSolver

**Project**
In this project, we are fine-tuning an LLM for an animation engine (specifically Python package Manim). The goal is to develop an AI application powered by an LLM that can receive user input in the form of raw text consisting of mathematical problems at the SAT level. The application should provide step-by-step solutions or hints for the student - as well as generate Python code for the animation engine. One major challenge would be to construct and fine-tune the said LLM.

### Milestone2

Our proposed data pipeline has 4 major steps: data collection, data pre-processing, LLM fine-tuning, and model deployment. For this milestone, we will be solely focusing on the first two components.

#### Data Collection

See [`src/collection/README.md`](src/collection/README.md) for an in-depth description of how to set up this component of the pipeline.

At this stage, we are using a container to run a python script that scrapes data from GitHub API. The scraper looks for all GitHub repositories containing the keyword "manim" (the animation engine Python package). For each repository, we collect all the Python files, then store them in a Google Cloud Storage (GCS) Bucket.

As of 09/26/2023, there are approximately 2,400 such repositories of interest. It takes approximately 1 second to collect and upload 2 Python files to the GCS bucket.

#### Data Pre-processing

See [`src/preprocessing/README.md`](src/preprocessing/README.md) for an in-depth description of how to set up this component of the pipeline.

Note that not all Python files we collected from the last step are relevant. We are only interested in those that contain code examples of actually using the Manim package. So at this step, we will first be filtering for relevant Python files by looking for appropriate import statements. Then we perform standard text preprocessing procedures for NLP such as tokenization, encoding, etc.

#### LLM Fine-tuning

For a future milestone.

#### Model Deployment

Also for a future milestone.
