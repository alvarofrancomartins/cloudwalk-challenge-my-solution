# CloudWalk Challenge 

This is my solution for this challenge.

1. Data analysis for task **3.1** is in the `CloudWalk_Data_Analysis_(Checkout).ipynb` notebook.
2. Data analysis for task **3.2** is in the `CloudWalk_Data_Analysis_(Transactions).ipynb` notebook. 
3. My thought process for creating the simple Monitoring Alert System can be seen in the `Monitoring Alert System Development.ipynb` notebook. 

To run the simulation of the Monitoring Alert System, you can simply run

```python
python3 monitoring.py 'transactions_1' 100
```

The first argument can be either `transactions_1` or `transactions_2`. This tells which dataset (csv file) to use to run the monitoring. 
The second argument is the interval (i.e, delay between frames in milliseconds) for the Matplotlib animation. 

I ran this on my Ubuntu terminal. I have also prepared two videos ([here](https://www.youtube.com/watch?v=vw_pp2OyI8M) and [here](https://www.youtube.com/watch?v=QlueZKk-LIk)) showing the monitoring for `transactions_1` and `transactions_2`.
