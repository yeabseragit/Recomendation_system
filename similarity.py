# Importing pandas and numpy libraries
import pandas as pd
import numpy as np

# Adjusted Cosine Similarity Function
def adjustedCosineSimilarity(movieA, movieB, avgA, avgB, userThreshold=5):
    # Find the indices of users who rated both movies
    commonUsers = (movieA != 0) & (movieB != 0)
    
    if commonUsers.sum() < userThreshold:
        # Not enough users have rated both movies
        return np.nan, commonUsers.sum()
    
    # Compute the adjusted ratings (subtract the average rating)
    adjustedA = movieA[commonUsers] - avgA
    adjustedB = movieB[commonUsers] - avgB
    
    # Compute numerator and denominator of cosine similarity
    numerator = np.dot(adjustedA, adjustedB)
    denominator = np.sqrt(np.dot(adjustedA, adjustedA) * np.dot(adjustedB, adjustedB))
    
    if denominator == 0:
        return np.nan, commonUsers.sum()
    
    similarity = numerator / denominator
    return similarity, commonUsers.sum()

# Function to compute similarity and output a DataFrame
def computeSimilarity(inputFile, userThreshold=5):
    # Load the data
    df = pd.read_csv(inputFile, sep='\t', names=['userId', 'movieId', 'rating', 'timestamp'])
    df = df[['userId', 'movieId', 'rating']]  # We only need userId, movieId, and rating
    
    # Create a matrix where rows are movies, columns are users, and values are ratings
    ratingsMatrix = df.pivot(index='movieId', columns='userId', values='rating').fillna(0)
    
    # Compute average ratings for each movie (row)
    movieAvgRatings = ratingsMatrix.mean(axis=1)

    # Store the results in a list
    results = []

    # Loop over each movie and compare with all other movies
    for i, movieA in ratingsMatrix.iterrows():
        mostSimilarMovie = None
        highestSimilarity = -1
        mostCommonRatings = 0
        
        for j, movieB in ratingsMatrix.iterrows():
            if i != j:  # Don't compare a movie to itself
                sim, common = adjustedCosineSimilarity(movieA, movieB, movieAvgRatings[i], movieAvgRatings[j], userThreshold)
                
                if sim > highestSimilarity:
                    highestSimilarity = sim
                    mostSimilarMovie = j
                    mostCommonRatings = common
        
        # Append result for this movie
        results.append([i, mostSimilarMovie, highestSimilarity, mostCommonRatings])

    # Convert to DataFrame and return
    resultsDf = pd.DataFrame(results, columns=['baseMovieId', 'mostSimilarMovieId', 'similarityScore', 'commonRatingsCount'])
    return resultsDf

# Set the path to the dataset
inputFile = r"C:\Users\Yeabs\OneDrive\Desktop\5100\ml-100k\u.data"

# Compute the movie similarities
similarityDf = computeSimilarity(inputFile, userThreshold=5)

# Display the first 20 rows of the output
similarityDf.head(20)

# Save the result to a CSV file
outputFile = r"C:\Users\Yeabs\OneDrive\Desktop\5100\ml-100k\movie_similarity_output.csv"
similarityDf.to_csv(outputFile, index=False)
print(f"Results saved to {outputFile}")
