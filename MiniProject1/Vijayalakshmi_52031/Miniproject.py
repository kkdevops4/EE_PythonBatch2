

movies = [
    {"title": "The Shawshank Redemption", "genre": "Drama", "year": 1994, "rating": 9.3},
    {"title": "The Dark Knight", "genre": "Action", "year": 2008, "rating": 9.0},
    {"title": "Interstellar", "genre": "Sci-Fi", "year": 2014, "rating": 8.7}
]



n = int(input("How many movies do you want to add? "))

for i in range(n):
    print("\nEnter details for Movie", i + 1)

    title = input("Title: ")
    genre = input("Genre (Action/Drama/Sci-Fi): ")
    year = int(input("Year: "))
    rating = float(input("Rating: "))

    

    movie = {
        "title": title,
        "genre": genre,
        "year": year,
        "rating": rating
    }

    movies.append(movie)




def top_rated_per_decade(movie_list):

    decade_best = {}

    for movie in movie_list:

        decade = (movie["year"] // 10) * 10

        if decade not in decade_best:
            decade_best[decade] = movie

        elif movie["rating"] > decade_best[decade]["rating"]:
            decade_best[decade] = movie

    print("\nTop-Rated Movie Per Decade")

    for decade in sorted(decade_best):

        best_movie = decade_best[decade]

        print(
            str(decade) + "s : " +
            best_movie["title"] +
            " (Rating: " +
            str(best_movie["rating"]) + ")"
        )




def average_rating_by_genre(movie_list):

    total_rating = {}
    movie_count = {}

    for movie in movie_list:

        genre = movie["genre"]

        if genre not in total_rating:
            total_rating[genre] = 0
            movie_count[genre] = 0

        total_rating[genre] += movie["rating"]
        movie_count[genre] += 1

    print("\nAverage Rating By Genre")

    for genre in total_rating:

        average = total_rating[genre] / movie_count[genre]

        print(genre + " : " + str(round(average, 2)))


top_rated_per_decade(movies)
average_rating_by_genre(movies)