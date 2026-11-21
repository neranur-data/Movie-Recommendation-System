# Movie Recommendation System

**User-Based and Item-Based Collaborative Filtering | Python, Pandas, Pearson Correlation**

## Project Overview

This project explores two collaborative filtering approaches for recommending movies using MovieLens movie metadata and user ratings:

- **User-based collaborative filtering:** identifies users with similar rating patterns and recommends movies favored by those users.
- **Item-based collaborative filtering:** identifies movies with rating patterns similar to a selected movie.

The approaches are demonstrated separately; the project does not combine their outputs into a single hybrid prediction score.

## Dataset

Source: [MovieLens datasets — GroupLens](https://grouplens.org/datasets/movielens/)

The scripts expect two local CSV files:

| File | Fields used | Purpose |
| --- | --- | --- |
| `movie.csv` | `movieId`, `title`, `genres` | Movie metadata |
| `ratings.csv` | `userId`, `movieId`, `rating`, `timestamp` | User ratings |

Dataset versions and sizes can vary. Download the appropriate MovieLens files and check that their names and columns match the scripts.

## Methods

### 1. User-Based Collaborative Filtering

1. Merge movie metadata with ratings.
2. Remove movies with relatively few ratings (the supplied script filters titles with **1,000 or fewer** ratings).
3. Build a user–movie matrix, with users as rows, movie titles as columns, and ratings as values.
4. Select a target user and identify movies they have rated.
5. Find other users who rated a sufficient proportion of the same movies.
6. Calculate Pearson correlations between users' rating patterns and select similar users.
7. Calculate a recommendation score as `correlation × rating`, then take the mean of those scores for each movie.
8. Rank candidate movies and exclude titles already rated by the target user.

The user-based function exposes configurable overlap, correlation, and score thresholds.

### 2. Item-Based Collaborative Filtering

1. Prepare the user–movie rating matrix.
2. Choose a movie (either by title or randomly from the matrix).
3. Calculate Pearson correlations between its rating column and other movie columns.
4. Rank movies by correlation to identify similar titles.

The supplied item-based script demonstrates title-based and random-movie examples. Its helper function currently returns the top 10 correlations, **including the selected movie itself** if present.

## Project Files

- `user_based_recommender_english.py` — user-based workflow and recommendation function.
- `item_based_recommender_english.py` — item-based workflow and helper functions.

## Tools and Skills

Python · Pandas · Data preparation · DataFrame merging · Pivot tables · Collaborative filtering · Pearson correlation · Recommendation ranking

## Running the Project

1. Install Python and Pandas:

   ```bash
   pip install pandas
   ```

2. Download the relevant MovieLens dataset from GroupLens.
3. Place `movie.csv` and `ratings.csv` in a local folder.
4. **Update the CSV paths in both Python scripts** to point to your local files. The current scripts contain absolute paths from the development computer; one section of the user-based script also uses a relative `datasets/movie_lens_dataset/` path.
5. Run the scripts in an environment with sufficient RAM. The user–movie pivot table and correlation calculations may be memory-intensive.

## Interpretation and Limitations

- Pearson correlation measures similarity in **rating patterns**, not necessarily identical ratings.
- Correlations based on small numbers of shared ratings may be unstable.
- The user-based score is the **mean of `correlation × rating`**, not a normalized weighted average.
- Removing infrequently rated movies reduces sparsity but may exclude niche titles.
- The supplied scripts are exploratory learning workflows, not a production recommendation service.
- No held-out evaluation or recommendation metrics (such as Precision@K or Recall@K) are reported here.

## Possible Improvements

- Make file paths configurable and remove repeated data-loading steps.
- Set a minimum number of shared ratings for correlation calculations.
- Exclude the selected movie from item-based recommendations.
- Evaluate recommendations on a held-out dataset.
- Explore normalized weighted scoring and model-based collaborative filtering.

## Learning Outcome

This project demonstrates how to transform large-scale user–item interaction data into personalized recommendation candidates and how user similarity differs from item similarity.
