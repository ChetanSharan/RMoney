# This Project is designed to test Rolling Trade Strategy.

### Objective: The script aims to analyse stock data of Apple Inc. (AAPL) ticker to detect potential trading signals based on historical maximum and minimum prices within a specific lookback period. Based on these  signals, positions and returns arecalculated. The resulting dataset is saved to a CSV file

### Steps Followed for project development.
1. Fetch Stock Data:
● Utilising yfinance, fetch the stock data for the ticker 'AAPL' for the past 2 years with an hourly interval.

2. Calculate Rolling Maximum and Minimum:
● For the column 'Close', calculate the rolling maximum and minimum over the lookback period. Store these in new columns max_price and min_price, respectively.

3. Determine Trading Signals:
● Identify short signals where the current close price matches the rolling maximum price. Store this in a Boolean column named Short_signal.
● Similarly, identify long signals where the current close price matches the rolling minimum price. Store this in a column named Long_signal.

4. Signal Processing:
● Initialise a new column named Signal with NaN values.
● Update the Signal column to represent a long signal with a value of 1 and a short signal with a value of -1.

5. Calculate Positions:
● Create a column Position0 that forward-fills any NaN values from the Signal column.
● Create a column Position1 to identify positions' initiation, where the position changes from the previous row.
● Generate a monetary value of the position in Position2 using Position1 and the current 'Close' price.

6. Filtering and Return Calculation:
● Extract rows from the main dataframe where Position1 is not zero into a new dataframe called df_ret.
● Remove any NaN values from df_ret.
● Calculate absolute returns using positions. Store in abs_returns.
● Convert the absolute returns to percentage returns. Store in pct_returns.
● Compute the cumulative sum of percentage returns. Store in pct_returns_cumsum.

7. Save the Results:
● Save the df_ret dataframe to a CSV file named 'aaa_returns.csv'.

### Assumptions made. 
There was one minor design changed in the project, instead of using equal operator, less that equal to operator was used & vice versa for long & short signals detection.

### How to run the code.
Execute the file "Acces.py". This will generate a CSV file named "aaa_returns.csv".

### Result of the project.
The line graph of Apple Inc. for last two years. Shown in blue colour. The Red line shows percentage return of the staregy selected.

![image](https://github.com/user-attachments/assets/290e0081-ac96-4916-ba21-275cca525d21)

Overall display of Percentage Returns.

![image](https://github.com/user-attachments/assets/045cd5eb-3d93-47f7-9168-09c51673e21f)

Image 1/2

![image](https://github.com/user-attachments/assets/33e636c9-c700-45f9-9776-06b53d26aa19)

Image 2/2


