 🚀 NetflixShowClustering

A data science project that clusters Netflix-like TV shows based on genre, ratings, episode run time, and popularity, using machine learning techniques.
It also provides personalized recommendations of similar shows based on your favorites.

⸻

📌 Features

✅ Extracts data from TMDB API on hundreds of popular TV shows.
✅ Performs feature engineering & one-hot encoding on genres.
✅ Clusters shows using:
	•	K-Means
	•	Agglomerative Clustering
	•	DBSCAN

✅ Visualizes results with seaborn and matplotlib:
	•	PCA cluster scatterplots
	•	Correlation heatmaps
	•	Genre distributions

✅ Builds a fuzzy string matching recommendation system.
✅ Exports dataset to CSV for Tableau dashboards & business insights.

⸻

🚀 Tech Stack
	•	🐍 Python: pandas, numpy, scikit-learn, seaborn, matplotlib, fuzzywuzzy
	•	☁️ Google Colab
	•	📡 TMDB API
	•	📊 Tableau

⸻

📊 Tableau Dashboard

🎨 Interactive dashboards explore:
	•	Clusters of shows by audience patterns
	•	Genre distributions by cluster
	•	Popularity vs rating trends

👉 Click here to view Tableau dashboard
(Replace this link with your Tableau Public URL once published!)

⸻

🗂 Repository structure

NetflixShowClustering/
│
├── NetflixShowClustering.ipynb     # Main Google Colab notebook
├── netflix_show_clustering.py      # Python script version
├── netflix_shows_clustered.csv     # Final processed data for Tableau & analysis
├── NetflixShowClustering.pdf       # PDF export of notebook
├── README.md                       # This file
├── requirements.txt                # Python dependencies
└── .gitignore                      # Ignore notebook checkpoints, etc.


⸻

⚙️ Getting started

🚀 Clone the repository

git clone https://github.com/yourusername/NetflixShowClustering.git
cd NetflixShowClustering

🔧 Install dependencies

pip install -r requirements.txt

📝 Run the notebook
	•	Open NetflixShowClustering.ipynb in Google Colab or Jupyter.
	•	Make sure to set up your TMDB API key (via google.colab.userdata or manually).

⸻

✨ Key Highlights

✅ End-to-end data pipeline:
	•	Data extraction from TMDB API
	•	Cleaning, one-hot encoding genres
	•	Scaling & clustering with multiple techniques
	•	Recommendation system via fuzzy string matching

✅ Exploratory Data Analysis (EDA):
	•	Heatmaps, genre bar charts, scatterplots of episode run time vs ratings

✅ Visualization & BI:
	•	Exported dataset powers a Tableau dashboard for interactive cluster exploration.

✅ Recommendation system:
	•	Input any 1-3 favorite shows, fuzzy matcher finds the closest match and suggests other shows from the same cluster.

⸻

🚀 How the recommendation works

1️⃣ Enter 1-3 show names you like.
2️⃣ The system uses fuzzy matching to find the closest show names in the dataset.
3️⃣ Identifies the cluster these shows belong to.
4️⃣ Recommends other shows from the same cluster.

⸻

🛠 Requirements

requests
pandas
numpy
scikit-learn
seaborn
matplotlib
fuzzywuzzy[speedup]

Install them all with:

pip install -r requirements.txt


⸻

📚 Sample outputs

🎯 Found closest matches: ['Sherlock Holmes']
🎉 Recommendations from cluster 2:
            name       rating  episode_run_time         genres
9    The Daily Show   7.8      30                 ['Comedy', 'News']
14   Breaking Bad    9.5      47                 ['Crime', 'Drama', 'Thriller']
27   Mindhunter     8.6      52                 ['Crime', 'Drama', 'Thriller']


⸻

✅ Future improvements
	•	Integrate collaborative filtering or deep learning embeddings for smarter recommendations.
	•	Add genre-weighted recommendations so you can choose “prefer Comedy over Crime.”
	•	Build a simple Streamlit web app for interactive recommendations.

⸻

🤝 Connect

If you found this project interesting or would like to collaborate, let’s connect!

👉 LinkedIn
👉 GitHub

⸻

📜 License

This project is open source under the MIT License.

⸻

🚀 That’s it!

Your project is now clean, documented, recruiter-friendly, and ready to impress on:
✅ GitHub Projects
✅ LinkedIn Projects section
✅ Your resume & portfolio

⸻

🎯 Want me to also write your LinkedIn post to showcase this project?
Just say:

“Yes, give me a LinkedIn post summary.”

and I’ll create a snappy, professional announcement for you! 🚀
