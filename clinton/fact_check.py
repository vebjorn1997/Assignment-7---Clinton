import doctest
import pandas as pd


"""
This module provides functionality for fact-checking claims about job creation
made during Clinton's speech in 2012.

It uses data from the Bureau of Labor Statistics (BLS) to analyze and compare
job creation between Democratic and Republican presidencies.

The module includes a Jobs class for tracking job statistics, functions for
data processing and analysis, and utilities for generating conclusions.

To run the program all you need to do is run the main function. It takes no arguments.
"python fact_check.py"
It should generate a conclusions.md file with the results 
assuming that you have the presidents.txt file, BLS_private.csv file, and labour_data_10_07_24.xlsx file.
"""


class Jobs:
    """
    A class to keep track of the number of jobs created by Democrats, Republicans and the total number of jobs created.
    Values in thousands.
    """
    def __init__(self):
        self.dem_jobs = 0
        self.rep_jobs = 0
        self.total_jobs = 0

    def add_dem_jobs(self, prev_month: int, current_month: int):
        """
        Add jobs created during a Democratic presidency to the total.

        Example:
            >>> jobs = Jobs()
            >>> jobs.add_dem_jobs(1000, 1100)
            >>> jobs.dem_jobs
            100
        """
        self.dem_jobs += current_month - prev_month
        self.total_jobs += current_month - prev_month

    def add_rep_jobs(self, prev_month: int, current_month: int):
        """
        Add jobs created during a Republican presidency to the total.

        Example:
            >>> jobs = Jobs()
            >>> jobs.add_rep_jobs(1000, 1100)
            >>> jobs.rep_jobs
            100
        """
        self.rep_jobs += current_month - prev_month
        self.total_jobs += current_month - prev_month

    def __str__(self):
        return f"Democrat Jobs: {format(self.dem_jobs * 1000, ',')}\nRepublican Jobs: {format(self.rep_jobs * 1000, ',')}\nTotal Jobs: {format(self.total_jobs * 1000, ',') }"


def assumptions_writings():
    """
    Function that includes some assumptions made, and creates the conclusions.md file
    """
    with open("conclusions.md", "w", encoding="utf-8") as file:
        file.write("## Assumptions\n")
        file.write("""Due to the BLS data only being given for each month and not the exact date,
                    I will assume that each president took office on the first day of the month.
                   This assumption lines up pretty well with the claims of Clinton even though there might be some discrepancies.
                   \n---\n""")


def write_to_conclusion(writing: str = ""):
    """
    Function that writes to the conclusions.md file
    """
    with open("conclusions.md", "a", encoding="utf-8") as file:
        file.write(writing)

def read_csv(file_path: str, args: dict) -> pd.DataFrame | None:
    """
    Function that reads a csv file and returns the content
    """
    try:
        return pd.read_csv(file_path, **args)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def check_equality():
    """
    This function checks if the content of the given BLS data is the same as the data retrived at October 7th 2024
    """
    try:
        updated_labour_stats = pd.read_excel(
            "labour_data_10_07_24.xlsx", index_col=0, header=0, skiprows=13
        )
        given_labour_stats = read_csv(
            "BLS_private.csv", {"index_col": 0, "header": 0, "skiprows": 6}
        )
        is_equal = updated_labour_stats.equals(given_labour_stats)
    except Exception as e:
        print(f"An error occurred: {e}")
        is_equal = False

    write_to_conclusion(
        f"\n## Equality Check\nThe content of the given BLS data is {'equal' if is_equal else 'different'} then data retrived at October 7th 2024\n\n---\n"
    )


def jobs_created(file_path: str, presidents_file_path: str):
    """
    Calculate the number of jobs created during Democratic and Republican presidencies.

    This function reads employment data from a CSV file and presidential term data from the presidents.txt file,
    then calculates the number of jobs created during each party's presidencies.

    Args:
        file_path (str): Path to the CSV file containing employment data.
        presidents_file_path (str): Path to the file containing years when presidencies changed.

    Returns:
        Jobs: An instance of the Jobs class with the calculated job numbers.

    Note:
        - The function assumes that the employment data CSV has a specific structure with years and monthly data.
        - It also assumes that the presidents file contains years when the presidency switched between parties.
        - The calculation starts from 1961 and continues until the end of the available data.
        - For any values that is a NaN, will be replaced with the value of the last month. This is to handle november and december 2012 being missing.
    """
    jobs = Jobs()
    flip_years = []
    with open(presidents_file_path, "r", encoding="utf-8") as file:
        for line in file:
            flip_years.append(int(line))

    df = read_csv(file_path, {"skiprows": 5})
    if df is None:
        return
    df_values = df.fillna(df.values[-1][10]).values

    flag = True  # True for dem, False for rep
    for index, year in enumerate(df_values):
        if year[0] in flip_years:
            flag = not flag
        for month_index, month_total_jobs in enumerate(year[1::]):
            # If first year, 1961, last month of previous year is equal to the first month of the current year
            if year[0] == 1961 and month_index == 0:
                prev_month = month_total_jobs
            elif month_index == 0:
                prev_month = df_values[index - 1][-1]
            else:
                prev_month = year[month_index]

            if flag:
                jobs.add_dem_jobs(prev_month, month_total_jobs)
            else:
                jobs.add_rep_jobs(prev_month, month_total_jobs)

    return jobs


def main():
    """
    Main function to execute the fact-checking process.

    This function orchestrates the following steps:
    1. Writes initial conclusions and assumptions to a file.
    2. Checks for equality between given BLS data and data retrived at October 7th 2024 from the BLS website.
    3. Calculates jobs created by Democrats, Republicans and the total number of jobs created.
    4. Writes the jobs created to the conclusions.md file.
    5. Writes the conclusion of the fact-checking process to the conclusions.md file.

    The function relies on several helper functions:
    - conclusion_writings(): Writes conclusions to a file.
    - check_equality(): Compares BLS data sets.
    - jobs_created(): Calculates how many jobs were created for each party.

    No parameters are required as it uses predefined file paths and a Jobs class instance.

    Returns:
    None
    """
    assumptions_writings()
    check_equality()
    jobs = jobs_created("BLS_private.csv", "presidents.txt")
    write_to_conclusion(f"\n## Jobs Created\n{str(jobs)}\n\n---\n")
    write_to_conclusion("\n ## Conclusion\n Based on my own analysis and assumptions of the data, I can with some confidence say that Clinton's claim is correct. Based on the data there were 66 million jobs created during this timeperiod, and the split between Democrats and Republicans matches the claims made by Clinton. That being said, there are some uncertaies as to what clinton meant by the word \"produced\" in his speech. There are other external factors that has skewed the data to favour the Demoracts, such as the several economic crises that happened during the Republican presidencies. Other factors include the exculsion of government jobs and farm jobs, although the government jobs would most likely have favour the Democrats over the Republicans. Other questions includes questions of wether or not a president should be creditet with jobs created a month into the office. Either way, did he lie or skew that data to favour his side is not for me to say, (I'm not political scientist) but the data he quote supports his claim.\n\n---\n")


if __name__ == "__main__":
    main()
    doctest.testmod()
