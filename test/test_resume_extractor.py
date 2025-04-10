from agents.resume_extractor import extract_resume_data

# Sample Resume Text
test_resume = """Education
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
• Transitioned the POC into an MVP, scaling the system to handle 5,000+ essays, achieving a 25% improvement in classification accuracy aligned
with academic grading standards.
• Integrated MLflow to track experiments, improving reproducibility and enabling systematic iteration on prompt optimization methodologies.
Golub Capital LLC Chicago, IL
JUNiOR DATA SCiENTiST Jun. 2023 – Dec. 2023
• Created a POC clustering model using Scikit‑learn to segment sponsors within a $60 billion asset portfolio, demonstrating actionable insights.
• Scaled the POC into an MVP integrated with a Power BI dashboard deployed on a Jenkins CI/CD pipeline, ensuring seamless updates and user
accessibility.
• Conducted A/B tests on portfolio allocation strategies, enabling a 15% reduction in risk and improving strategic decision‑making.
• Solved data imbalance issues in loan default predictions by implementing SMOTE (Synthetic Minority Over‑sampling Technique), enhancing
model reliability and accuracy.
• Built data pipelines in Databricks to preprocess structured and unstructured datasets, achieving 99% data integrity for machine learning
workflows.
Office of Mental Health (OMH) New York, USA
DATA SCiENTiST Jan. 2023 – Jun. 2023
• Designed a Generative AI‑powered chatbot as a POC, leveraging LangChain and OpenAI GPT‑4 for personalized mental health recommendations.
• Deployed the chatbot on Azure Machine Learning with Docker, achieving 90% accuracy in delivering contextually relevant recommendations
and reducing latency.
• Reduced chatbot latency by 30% by optimizing backend services and leveraging FastAPI for high‑speed API calls.
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
report adoption by 28% and improved portfolio insights.
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
Learning, achieving 90% recommendation accuracy and serving over 50,000 users annually.
• Led a team of 3 developers to implement scalable deployment with Docker and Kubernetes, reducing operational latency by 30% and ensuring
secure data handling with AES encryption.
Kidney Disease Prediction using Deep Learning Remote
GiTHUB LiNK JUN. 2023 ‑ DEC. 2023
• Built and deployed a TensorFlow‑based CNN model with 92% prediction accuracy, improving diagnostic workflows by 30% through realtime
predictions using TensorFlow Serving.
• Optimized data preprocessing pipelines for clinical datasets, achieving 99% data integrity and enhancing explainability through visualizations
of feature importance.
Detecting Attack by Malicious Executables using different Machine Learning models College Station, Texas
GiTHUB LiNK JAN. 2020 ‑ MAY. 2020
• Employed data processing techniques like validation, normalization and sorting of the given fraud detection dataset
• Built and Compared two ensemble learning models constructed using decision trees, perceptron, and MLP using K‑fold validation and
plotted an ROC curve to choose the best threshold to select the most accuracte model which had an accuracy of 95.98%.
"""

# Sample Job Description (For Comparison)
test_jd = """
Looking for a Senior Data Engineer with expertise in Python, Spark, AWS, and Databricks.
The role involves developing ETL pipelines, optimizing workflows, and implementing cost-effective solutions.
Skills required: Python, SQL, Spark, Databricks, AWS Redshift, Snowflake, Airflow.
"""

# Run the extractor
extracted_data = extract_resume_data(test_resume, test_jd)
print("🔹 Extracted Resume Data:")
print(extracted_data)
