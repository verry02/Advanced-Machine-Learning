# Advanced-Machine-Learning
This repository contains my latest project for the exam "Advanced Machine Learning", done with other two colleagues at the Polytechnic University of Turin during the academic year 2024/2025



# Natural Language Queries in Egocentric Videos 

Link to the slides: https://bit.ly/4aaWCK6

Link to the official document: https://bit.ly/49UOmhK


The project focuses on addressing the Natural Language Queries (NLQ) task within egocentric videos, as outlined in the Ego4D benchmark.

The main objective of the project is to predict the temporal segments in a video that answer specific natural language queries, such as “Where was object X last seen?” or “Which objects did the user interact with?”. This task requires integrating information from both video and textual modalities while tackling challenges such as handling long video durations and accurately linking queries to specific video segments.

The repository implements the following key steps:
	
 1.	Dataset Analysis: Exploration of the Ego4D NLQ annotations, including query template distributions, duration of annotated clips, and correlations with video scenarios.
	
 2.	Training Models: Implementation and comparison of two architectures, VSLBase and VSLNet, using pre-extracted visual features from Omnivore and EgoVLP models.
	
 3.	Results Evaluation: Comparison of the obtained results with the official baselines provided in the Ego4D paper.
	
 4.	Proposed Extensions: Additional experiments, including modifications to the VSLNet architecture, to evaluate the impact of different model components on performance.

This project provides insights into the intersection of natural language processing and video understanding, leveraging state-of-the-art methods to tackle complex real-world challenges in egocentric vision.


# Utilities 

Span-based Localizing Network for Natural Language Video Localization: https://github.com/26hzhang/VSLNet

tensorflow-glove: https://github.com/GradySimon/tensorflow-glove/tree/master

EgocentricVision: https://github.com/EgocentricVision/EgocentricVision
