import numpy as np

def evaluation_metrics(true_value, predicted_values):
    # Convert lists to numpy arrays
    predicted_values = np.array(predicted_values)

    # Calculate Mean Squared Error (MSE)
    mse = np.mean((true_value - predicted_values)**2)

    # Calculate Mean Absolute Error (MAE)
    mae = np.mean(np.abs(true_value - predicted_values))

    # Calculate Root Mean Squared Error (RMSE)
    rmse = np.sqrt(mse)

    # Calculate Bias
    bias = np.mean(true_value - predicted_values)

    #Calculate ENoRMSE
    error = np.mean((1-(predicted_values/true_value))**2)
    enormse = np.sqrt(error)

    metrics = [mse, mae, rmse, bias, enormse]
    return metrics


def boxplot_ite(ite):

    # Calculate statistics
    data = np.reshape(ite, -1)
    minimum = np.min(data)
    first_quartile = np.percentile(data, 25)
    median = np.median(data)
    third_quartile = np.percentile(data, 75)
    maximum = np.max(data)
    
    # Interquartile range (IQR)
    iqr = third_quartile - first_quartile
    
    # Define upper and lower bounds for outliers
    upper_bound = third_quartile + 1.5 * iqr
    lower_bound = first_quartile - 1.5 * iqr
    
    # Detect outliers
    outliers = data[(data < lower_bound) | (data > upper_bound)]
    boxplot = [minimum, first_quartile, median, third_quartile, maximum, iqr, upper_bound, lower_bound]
    return boxplot