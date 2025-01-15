# Here is a solution for each tutorial
Please do not look at this until you've successfully completed the tutorial.

<details>
    <summary>Pass^K</summary>

    ```Python

    def passHatK(frame,n:int,success= "pass"):
        """A function that takes a dataframe with the rows representing a single task/observation
        and columns representing each run or pass. The metric pass^k is calculated to determine
        reliability and consistency across the dataset as a whole.
        
        success = the value to be checked for success (note, the dataframe must include explicit success, it cannot be calculated dynamically within this function)
        n = the total number of runs to be measured
        k = the current pass or run
        c = the current number of successes per row
        """
    total = 0
    for row in frame.itertuples(index=False, name="task"):
        k = 1
        c = 0
        for i in range(1,n+1):
            current = 1 if row[i] == success else 0
            c += current
            total += comb(c,k)/comb(n,k)
            k += 1
    return total / len(frame)

    ```
    </details>