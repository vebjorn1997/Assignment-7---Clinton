import pandas as pd

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

def jobs_created(url_path: str, president: str):
    """
    Function that takes the url path of the csv file and returns the number of jobs created
    """
    dem_jobs = 0
    rep_jobs = 0
    total_jobs = 0
    pres = []
    with open(president, "r", encoding="utf-8") as file:
        for line in file:
            pres.append(line.split())

    df = pd.read_csv(url_path, skiprows=5)
    # Fill the NaN values with the values from October 2012, this is because we are measuring the change in jobs from one month to the next and the dataset ends in October 2012
    df_values = df.fillna( df.values[-1][10] ).values

    flag = 0 # 0 - Dem, 1 - Rep
    # Month Change Calculation
    for year in df_values:
        yearly_jobs = 0
        for month in enumerate(year):
            if month[0] == 0:
                continue

            # flag = 0 if year[0] == "Dem" else 1
            prev_month = month[0] - 1
            # print("Prev Month: ", year[prev_month])
            if prev_month != 0:
                if flag == 0: # Dem
                    change = month[1] - year[prev_month]
                    dem_jobs += change
                    yearly_jobs += change
                else: # Rep
                    change = month[1] - year[prev_month]
                    rep_jobs += change
                    yearly_jobs += change

            for party in pres:
                if int(party[0]) == year[0]:
                    flag = 0 if party[1] == "Dem" else 1
        total_jobs += yearly_jobs

    print("Total jobs: ", total_jobs)

    # flag = 0 # 0 - Dem, 1 - Rep
    # for x in df_values:
    #     # print(x[1::])
    #     match flag:
    #         case 0:
    #             dem_jobs += sum(x[1::])
    #             total_jobs += sum(x[1::])
    #         case 1:
    #             rep_jobs += sum(x[1::])
    #             total_jobs += sum(x[1::])
    #     for party in pres:
    #         if int(party[0]) == x[0]:
    #             flag = 0 if party[1] == "Dem" else 1

    return dem_jobs, rep_jobs, total_jobs


def main():
    conclusion_writings()
    check_equality()
    dem_jobs, rep_jobs, total_jobs = jobs_created("BLS_private.csv", "presidents.txt")
    print(f"The number of jobs created by the Democrats is {dem_jobs}")
    print(f"The number of jobs created by the Republicans is {rep_jobs}")
    print(f"The total number of jobs created is {total_jobs}")

if __name__ == "__main__":
    main()
