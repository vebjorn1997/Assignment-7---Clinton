import pandas as pd

class Jobs:
    def __init__(self):
        self.dem_jobs = 0
        self.rep_jobs = 0
        self.total_jobs = 0

    def add_dem_jobs(self, prev_month: int, current_month: int):
        self.dem_jobs += current_month - prev_month
        self.total_jobs += current_month - prev_month

    def add_rep_jobs(self, prev_month: int, current_month: int):
        self.rep_jobs += current_month - prev_month
        self.total_jobs += current_month - prev_month

    def __str__(self):
        return f"Democrat Jobs: {self.dem_jobs}\nRepublican Jobs: {self.rep_jobs}\nTotal Jobs: {self.total_jobs}"

def conclusion_writings(writing: str = ""):
    """
    Function that just writes some info to the conclusions.md file
    """
    with open("conclusions.md", "w", encoding="utf-8") as file:
        file.write("## Assumptions\n")
        file.write("Due to the BLS data only being given for each month and not the exact date, I will assume that each president took office on the first day of the month.\n\n---\n")
        if writing:
            file.write(writing)

def check_equality():
    """
    This function checks if the content of the given BLS data is the same as the data retrived at October 7th 2024
    """
    try:
        updated_labour_stats = pd.read_excel("labour_data_10_07_24.xlsx", index_col=0, header=0, skiprows=13)
        given_labour_stats = pd.read_csv("BLS_private.csv", index_col=0, header=0, skiprows=6)
        is_equal = updated_labour_stats.equals(given_labour_stats)
    except Exception as e:
        print(f"An error occurred: {e}")
        is_equal = False

    conclusion_writings(f"\n## Equality Check\nThe content of the given BLS data is {'equal' if is_equal else 'different'} then data retrived at October 7th 2024\n\n---\n")

def jobs_created(file_path: str, presidents_file_path: str, jobs: Jobs):
    """
    This function calculates the number of jobs created by the Democrats and Republicans
    """
    flip_years = []
    with open(presidents_file_path, "r", encoding="utf-8") as file:
        for line in file:
            flip_years.append(int(line))

    df = pd.read_csv(file_path, skiprows=5)
    df_values = df.fillna(df.values[-1][10]).values

    flag = True # True for dem, False for rep
    for index, year in enumerate(df_values):
        if year[0] in flip_years:
            flag = not flag
        for month_index, month_total_jobs in enumerate(year[1::]):
            #If first year, 1961, last month of previous year is equal to the first month of the current year
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

def main():
    """
    Main function to execute the fact-checking process.

    This function orchestrates the following steps:
    1. Writes initial conclusions and assumptions to a file.
    2. Checks for equality between given BLS data and data retrived at October 7th 2024 from the BLS website.
    3. Calculates jobs created by Democrats, Republicans and the total number of jobs created.
    4. Prints the job creation statistics.

    The function relies on several helper functions:
    - conclusion_writings(): Writes conclusions to a file.
    - check_equality(): Compares BLS data sets.
    - jobs_created(): Calculates job creation statistics.

    No parameters are required as it uses predefined file paths and a Jobs class instance.

    Returns:
    None
    """
    conclusion_writings()
    check_equality()
    jobs = Jobs()
    jobs_created("BLS_private.csv", "presidents.txt", jobs)
    print(jobs)

if __name__ == "__main__":
    main()
