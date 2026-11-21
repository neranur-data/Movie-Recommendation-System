############################################
# User-Based Collaborative Filtering
#############################################

# Step 1: Data Preparation
# Step 2: Identify Movies Rated by the Target User
# Step 3: Identify Other Users Who Rated the Same Movies
# Step 4: Find Users with Similar Rating Patterns
# Step 5: Calculate the Mean Weighted Recommendation Score
# Step 6: Wrap the Workflow in a Function

#############################################
# Step 1: Data Preparation
#############################################
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)

def create_user_movie_df():
    import pandas as pd
    movie = pd.read_csv("movie.csv")
    rating = pd.read_csv("ratings.csv")
    df = movie.merge(rating, how="left", on="movieId")
    comment_counts = pd.DataFrame(df["title"].value_counts())
    rare_movies = comment_counts[comment_counts["count"] <= 1000].index
    common_movies = df[~df["title"].isin(rare_movies)]
    user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
    return user_movie_df

user_movie_df = create_user_movie_df()

import pandas as pd
random_user = int(pd.Series(user_movie_df.index).sample(1, random_state=45).iloc[0])


#############################################
# Step 2: Identify Movies Rated by the Target User
#############################################
random_user
user_movie_df
random_user_df = user_movie_df[user_movie_df.index == random_user]

movies_watched = random_user_df.columns[random_user_df.notna().any()].tolist()

user_movie_df.loc[user_movie_df.index == random_user,
                  user_movie_df.columns == "Silence of the Lambs, The (1991)"]


len(movies_watched)



#############################################
# Step 3: Identify Other Users Who Rated the Same Movies
#############################################

movies_watched_df = user_movie_df[movies_watched]

user_movie_count = movies_watched_df.T.notnull().sum()

user_movie_count = user_movie_count.reset_index()

user_movie_count.columns = ["userId", "movie_count"]

user_movie_count[user_movie_count["movie_count"] > 20].sort_values("movie_count", ascending=False)

user_movie_count[user_movie_count["movie_count"] == 33].count()


users_same_movies = user_movie_count[user_movie_count["movie_count"] > 20]["userId"]


# users_same_movies = user_movie_count[user_movie_count["movie_count"] > perc]["userId"]
# perc = len(movies_watched) * 60 / 100

#############################################
# Step 4: Find Users with Similar Rating Patterns
#############################################

# We will complete the following three steps:
# 1. Combine the target user and other users in one DataFrame.
# 2. Calculate pairwise rating correlations.
# 3. Identify the most similar users.


final_df = pd.concat([movies_watched_df[movies_watched_df.index.isin(users_same_movies)],
                      random_user_df[movies_watched]])

corr_df = final_df.T.corr().unstack().sort_values().drop_duplicates()

corr_df = pd.DataFrame(corr_df, columns=["corr"])

corr_df.index.names = ['user_id_1', 'user_id_2']

corr_df = corr_df.reset_index()

top_users = corr_df[(corr_df["user_id_1"] == random_user) & (corr_df["corr"] >= 0.65)][
    ["user_id_2", "corr"]].reset_index(drop=True)

top_users = top_users.sort_values(by='corr', ascending=False)

top_users.rename(columns={"user_id_2": "userId"}, inplace=True)


rating = pd.read_csv("ratings.csv")
top_users_ratings = top_users.merge(rating[["userId", "movieId", "rating"]], how='inner')

top_users_ratings = top_users_ratings[top_users_ratings["userId"] != random_user]


#############################################
# Step 5: Calculate the Mean Weighted Recommendation Score
#############################################

top_users_ratings['weighted_rating'] = top_users_ratings['corr'] * top_users_ratings['rating']

top_users_ratings.groupby('movieId').agg({"weighted_rating": "mean"})

recommendation_df = top_users_ratings.groupby('movieId').agg({"weighted_rating": "mean"})

recommendation_df = recommendation_df.reset_index()

recommendation_df[recommendation_df["weighted_rating"] > 3.5]

movies_to_be_recommend = recommendation_df[recommendation_df["weighted_rating"] > 3.5].sort_values("weighted_rating", ascending=False)

movie = pd.read_csv("movie.csv")
movies_to_be_recommend.merge(movie[["movieId", "title"]])



#############################################
# Step 6: Wrap the Workflow in a Function
#############################################

def create_user_movie_df():
    import pandas as pd
    movie = pd.read_csv("movie.csv")
    rating = pd.read_csv("ratings.csv")
    df = movie.merge(rating, how="left", on="movieId")
    comment_counts = pd.DataFrame(df["title"].value_counts())
    rare_movies = comment_counts[comment_counts["count"] <= 1000].index
    common_movies = df[~df["title"].isin(rare_movies)]
    user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
    return user_movie_df

user_movie_df = create_user_movie_df()

# perc = len(movies_watched) * 60 / 100
# users_same_movies = user_movie_count[user_movie_count["movie_count"] > perc]["userId"]


def user_based_recommender(random_user, user_movie_df, ratio=60, cor_th=0.65, score=3.5):
    import pandas as pd
    random_user_df = user_movie_df[user_movie_df.index == random_user]
    movies_watched = random_user_df.columns[random_user_df.notna().any()].tolist()
    movies_watched_df = user_movie_df[movies_watched]
    user_movie_count = movies_watched_df.T.notnull().sum()
    user_movie_count = user_movie_count.reset_index()
    user_movie_count.columns = ["userId", "movie_count"]
    perc = len(movies_watched) * ratio / 100
    users_same_movies = user_movie_count[user_movie_count["movie_count"] > perc]["userId"]

    final_df = pd.concat([movies_watched_df[movies_watched_df.index.isin(users_same_movies)],
                          random_user_df[movies_watched]])
    final_df = final_df[~final_df.index.duplicated(keep="first")]
    print("Number of duplicate user IDs:", final_df.index.duplicated().sum())
    print(final_df.columns[final_df.columns.duplicated()])
    print("Number of duplicate user IDs:", final_df.index.duplicated().sum())
    corr_df = final_df.T.corr().unstack().sort_values()
    corr_df = pd.DataFrame(corr_df, columns=["corr"])
    corr_df.index.names = ['user_id_1', 'user_id_2']
    corr_df = corr_df.reset_index()

    top_users = corr_df[(corr_df["user_id_1"] == random_user) & (corr_df["corr"] >= cor_th)][
        ["user_id_2", "corr"]].reset_index(drop=True)

    top_users = top_users.sort_values(by='corr', ascending=False)
    top_users = top_users[top_users["user_id_2"] != random_user]
    print(top_users.head(10))
    top_users.rename(columns={"user_id_2": "userId"}, inplace=True)
    rating = pd.read_csv("ratings.csv")
    top_users_ratings = top_users.merge(rating[["userId", "movieId", "rating"]], how='inner')
    print("Number of similar users:", len(top_users))
    print("Number of merged ratings:", len(top_users_ratings))
    top_users_ratings['weighted_rating'] = top_users_ratings['corr'] * top_users_ratings['rating']
    print(
        top_users_ratings.groupby("movieId")["userId"]
        .nunique()
        .value_counts()
        .sort_index()
    )

    recommendation_df = top_users_ratings.groupby("movieId").agg(
        weighted_rating=("weighted_rating", "mean"),
        user_count=("userId", "nunique")
    )
    recommendation_df = recommendation_df.reset_index()

    movies_to_be_recommend = recommendation_df[recommendation_df["weighted_rating"] > score].sort_values("weighted_rating", ascending=False)
    movie = pd.read_csv("movie.csv")
    recommendations = movies_to_be_recommend.merge(
        movie[["movieId", "title"]]
    )
    print("Number of recommendations before filtering:", len(recommendations))
    print("Number of previously rated recommendations:",
          recommendations["title"].isin(movies_watched).sum())
    recommendations = recommendations[
        ~recommendations["title"].isin(movies_watched)
    ]

    return recommendations



random_user = int(pd.Series(user_movie_df.index).sample(1).iloc[0])
user_based_recommender(random_user, user_movie_df, cor_th=0.30, score=1.5)


