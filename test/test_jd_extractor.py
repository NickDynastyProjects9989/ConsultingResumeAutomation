from agents.jd_extractor import extract_job_data
import sys
import os
from agents.resume_extractor import extract_resume_data
from agents.resume_optimizer import process_all_clients  # Third Agent

# Import the Job Description Extractor

test_jd = """ 
Responsibilities
Exploring data and crafting models to answer core business problems that may not have a common blueprint
Driving the invention of new approaches and algorithms for tackling data intensive problems
Pioneering R&D efforts to rapidly understand and assimilate state of the art methods
Scaling up from “laptop-scale” to “cluster scale” problems by driving efforts to standardize and industrialize solutions
Championing best practices for future reuse in the form of accessible, reusable patterns, templates, and code bases
Works with Engineering partners to develop dashboards for end users through production deployment processes
Understanding in depth both the business and technical problems Dataworks aims to solve
Delivering tangible value very rapidly, collaborating with diverse teams of varying disciplines and organizational backgrounds
Interacting with senior technologists from the broader enterprise and outside of FedEx (partner ecosystems and customers) to create synergies and identify opportunities for improvement
Work hand in hand with business partners to develop tools that deliver value to the end users
Regularly lead demo sessions and presentations with senior leadership

Qualification
check
Represents the skills you have
Find out how your skills align with this job's requirements. If anything seems off, you can easily click on the tags to select or unselect skills to reflect your actual expertise.

checkMachine Learning
checkData Science
checkStatistical Techniques
checkPython
checkAdvanced Statistical Techniques
checkData Engineering
ML Ops
checkCI/CD Processes
Agile Practices
checkTensorFlow
checkPyTorch
SKLearn
checkXGBoost
checkDatabricks
checkSpark
checkPowerBI
Scala
Java
Kafka
Mathematical Analysis
R&D
checkData Analytics
checkMentoring
Required
Takes ownership over select data science initiatives.
Advances Dataworks’ broad capabilities to use and deploy cutting edge data science and machine learning tools and methods in Dataworks projects, platforms and products.
Anchors current best practices by driving the design and build of reusable data science assets.
Simultaneously works to keep Dataworks on the bleeding edge by understanding the very latest and most sophisticated methods and tools for grappling with extremely large scale and complex problems.
Leads junior data scientists in modeling and development to support operations initiatives and strategic programs, through the use of descriptive, diagnostic, predictive, prescriptive and ensemble modeling, advanced statistical techniques, and use of database tools and/or other approaches in mathematical analysis.
Applies understanding of ML Ops, CI/CD processes and machine learning / data engineering practices to ensure sustainable model development and provide recommendations on complex problems.
Provides guidance to less senior team members to drive results.
Works with cross-functional teams.
Understanding in depth both the business and technical problems Dataworks aims to solve.
Exploring data and crafting models to answer core business problems that may not have a common blueprint.
Driving the invention of new approaches and algorithms for tackling data intensive problems.
Pioneering R&D efforts to rapidly understand and assimilate state of the art methods.
Scaling up from 'laptop-scale' to 'cluster scale' problems by driving efforts to standardize and industrialize solutions.
Delivering tangible value very rapidly, collaborating with diverse teams of varying disciplines and organizational backgrounds.
Interacting with senior technologists from the broader enterprise and outside of FedEx (partner ecosystems and customers) to create synergies and identify opportunities for improvement.
Championing best practices for future reuse in the form of accessible, reusable patterns, templates, and code bases.
Works with Engineering partners to develop dashboards for end users through production deployment processes.
Technical background in computer science, data science, machine learning, artificial intelligence, statistics or other quantitative and computational science.
A track record of designing and deploying large scale technical solutions, which deliver tangible, ongoing value.
Direct experience having built and deployed robust, complex production systems that implement modern, data scientific methods at scale.
Ability to context-switch, to provide support to dispersed teams which may need an 'expert hacker' to unblock an especially challenging technical obstacle, and to work through problems as they are still being defined.
Demonstrated ability to deliver technical projects with a team, often working under tight time constraints to deliver value.
An 'engineering' mindset, willing to make rapid, pragmatic decisions to improve performance, accelerate progress or magnify impact.
Comfort with working with distributed teams on code-based deliverables, using version control systems and code reviews.
Master’s Degree or equivalent in computer science, operations research, statistics, applied mathematics or related quantitative discipline.
Three-Four (3-4) years’ work experience in Master’s Degree or equivalent in computer science, operations research, statistics, applied mathematics or related quantitative discipline.
Extensive knowledge in advanced data science and machine learning tools and methods, including the iterative development of analysis pipelines to provide insights at scale.
Extensive knowledge and experience in conducting end-to end analyses, including data gathering and requirements specification, processing, analysis, and presentations.
Strong understanding of the transportation industry, competitors, and evolving technologies.
Experience providing some level of leadership in a general planning or consulting setting.
Experience as a leader or a senior member of multi-functional project teams.
Strong oral and written communication skills.
Preferred
Use of agile and devops practices for project and software management including continuous integration and continuous delivery
Demonstrated expertise in working with some of the following common languages and tools: SKLearn, XGBoost, Tensorflow, Pytorch, MLlib and other core machine learning frameworks
Python, Scala, Java and other modern programming languages
MLFlow, Databricks, Spark, Kafka and other data tools and frameworks
Experience building PowerBI Dashboards that can efficiently handle large amounts of data without performance impacts

"""

test_resume = """
Education
State University Of Newyork, Master of Science CGPA : 3.6/4 2022‑ 2024 New York, USA
Focus: Statistical Machine Learning, Data Science
Skills
Languages Python, R, SQL, C, MATLAB, PySpark, Scala
Frameworks Pandas, Numpy, SciPy, Scikit‑Learn, TensorFlow, PyTorch, LangChain, FastAPI, MLflow, Kubeflow
Data Engineering Tools Databricks, Apache Spark, Airflow, Terraform, Ansible, Hadoop, Azure Synapse Analytics, Azure Data Factory
Cloud and DevOps AWS SageMaker, Azure Machine Learning, Kubernetes, Docker, GitHub, GitHub Actions, Jenkins
Visualization Tools Tableau, Power BI, Jupyter Notebooks, R Studio, Spyder
Domain Expertise Machine Learning, Deep Learning, Natural Language Processing (NLP), Generative AI, Statistical Modeling,
Causal Inference, A/B Testing, Experimentation, Optimization
Work Experience
Service Oriented Solutions LLC Dallas, TX
DATA SCiENTiST DEC. 2023 ‑ present
• Developed and deployed deep learning models using RNNs in TensorFlow/Keras for time‑series forecasting, improving financial risk assessment
accuracy by 20%.
• Designed and implemented predictive models for classification and clustering using PySpark and scikit‑learn, optimizing customer segmentation
strategies.
• Analyzed model limitations and interpretability, identifying areas where predictions had lower reliability and providing business stakeholders
with actionable insights.
• Built end‑to‑end ML pipelines integrating PySpark, pandas, and MLOps tools (GitHub Actions, Terraform, Docker) for scalable deployment
and monitoring.
• Collaborated with ‑functional teams, including data engineers and business analysts, to integrate AI‑driven insights into production systems
and reporting dashboards
University at Albany (Council on Research) Albany, NY
RESEARCH ASSiSTANT Dec. 2022 – Dec. 2023
• Designed a Proof of Concept (POC) for a Retrieval‑Augmented Generation (RAG) system using LangChain and OpenAI GPT‑3.5, demonstrating
feasibility in classifying essays based on leadership and perseverance traits.
• Transitioned the POC into an MVP, scaling the system to handle 5,000+ essays, achieving a 25 improvement in classification accuracy aligned
with academic grading standards.
• Integrated MLflow to track experiments, improving reproducibility and enabling systematic iteration on prompt optimization methodologies.
Golub Capital LLC Chicago, IL
JUNiOR DATA SCiENTiST Jun. 2023 – Dec. 2023
• Created a POC clustering model using Scikit‑learn to segment sponsors within a $60 billion asset portfolio, demonstrating actionable insights.
• Scaled the POC into an MVP integrated with a Power BI dashboard deployed on a Jenkins CI/CD pipeline, ensuring seamless updates and user
accessibility.
• Conducted A/B tests on portfolio allocation strategies, enabling a 15 reduction in risk and improving strategic decision‑making.
• Solved data imbalance issues in loan default predictions by implementing SMOTE (Synthetic Minority Over‑sampling Technique), enhancing
model reliability and accuracy.
• Built data pipelines in Databricks to preprocess structured and unstructured datasets, achieving 99 data integrity for machine learning
workflows.
Office of Mental Health (OMH) New York, USA
DATA SCiENTiST Jan. 2023 – Jun. 2023
• Designed a Generative AI‑powered chatbot as a POC, leveraging LangChain and OpenAI GPT‑4 for personalized mental health recommendations.
• Deployed the chatbot on Azure Machine Learning with Docker, achieving 90 accuracy in delivering contextually relevant recommendations
and reducing latency.
• Reduced chatbot latency by 30 by optimizing backend services and leveraging FastAPI for high‑speed API calls.
• Implemented robust security measures, including RBAC and AES encryption, ensuring compliance with HIPAA regulations while maintaining
session integrity.
• Migrated a legacy 10,000‑line SAS codebase to SQL, enhancing performance and supporting dynamic chatbot queries.
• Built secure Tableau dashboards for real‑time monitoring of chatbot usage trends, improving provider decision‑making efficiency by 30%.
FEBRUARY 24, 2025 NiKHiL GANNU · RÉSUMÉ 1
Tata Consultancy Services (TCS) New York, USA
DATA SCiENTiST Feb. 2020 – Jul. 2022
• Developed an NLP‑powered recommendation system for financial services, leveraging BERT and Word2Vec embeddings to provide personalized
investment recommendations, increasing customer engagement by 35
• Built an AI‑driven content recommendation engine, utilizing collaborative filtering and reinforcement learning, which boosted financial research
report adoption by 28 and improved portfolio insights.
• Implemented Named Entity Recognition (NER) pipelines using SpaCy and Hugging Face Transformers, automating the extraction of critical
financial entities from regulatory documents.
• Developed a text similarity scoring system using TF‑IDF, cosine similarity, and transformers, enabling automated document matching for
regulatory compliance across multiple jurisdictions.
• Led the development of an AI‑powered fraud detection system, leveraging LSTM sequence models on transaction logs to identify suspicious
patterns, improving fraud detection rates by 40%.
Projects
Generative AI Solutions: Medical Chatbot, RAG System, and QA Chatbot Remote
GiTHUB LiNK JAN. 2023 ‑ PRESENT
• Deployed a Generative AI‑powered system integrating a medical chatbot and QA chatbot using LangChain, Pinecone, and Azure Machine
Learning, achieving 90 recommendation accuracy and serving over 50,000 users annually.
• Led a team of 3 developers to implement scalable deployment with Docker and Kubernetes, reducing operational latency by 30% and ensuring
secure data handling with AES encryption.
Kidney Disease Prediction using Deep Learning Remote
GiTHUB LiNK JUN. 2023 ‑ DEC. 2023
• Built and deployed a TensorFlow‑based CNN model with 92% prediction accuracy, improving diagnostic workflows by 30% through realtime
predictions using TensorFlow Serving.
• Optimized data preprocessing pipelines for clinical datasets, achieving 99 data integrity and enhancing explainability through visualizations
of feature importance.
Detecting Attack by Malicious Executables using different Machine Learning models College Station, Texas
GiTHUB LiNK JAN. 2020 ‑ MAY. 2020
• Employed data processing techniques like validation, normalization and sorting of the given fraud detection dataset
• Built and Compared two ensemble learning models constructed using decision trees, perceptron, and MLP using K‑fold validation and
plotted an ROC curve to choose the best threshold to select the most accuracte model which had an accuracy of 95.98%.
"""

if __name__ == "__main__":
    enhanced_experiences = process_all_clients(test_resume, test_jd)  # Run 3rd Agent # Convert to LaTeX
    print(enhanced_experiences)
    # Step 3: Optimize Resume for Each Client (Third Agent)
    # ✅ Final Check: Ensure Output is Correct