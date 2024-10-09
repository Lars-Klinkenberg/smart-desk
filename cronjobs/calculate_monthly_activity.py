from db_controller import db_controller
from datetime import datetime
import logging


# saves the monthly_avg data to the db for every month that has not been saved till the last saved month
def check_and_save(id_of_month, year):
    # check if there is already data saved for this month
    logger.info(f"loading monthly avgs for month: {id_of_month}, {year}")
    activity = db_controller.get_monthly_avg_entries_of_month(id_of_month, year)

    if month_was_saved(activity):
        logger.info(f"month {id_of_month}, {year} was already saved")
        return

    save_month(id_of_month, year)

    if id_of_month == 1:
        id_of_month = 12
        year -= 1
    else:
        id_of_month -= 1
    check_and_save(id_of_month, year)


def month_was_saved(activity):
    if len(activity) > 0:
        return True

    return False


def save_month(id_of_month, year):
    monthly_activity = db_controller.get_month_avgs(id_of_month, year)

    if len(monthly_activity) == 0:
        logger.info(f"no activity for {id_of_month}, {year} found. Saving default")
        db_controller.save_monthly_avg(0, "00:00:00", id_of_month, year)

    for activity in monthly_activity:
        avg_time = activity["avg_time"]
        height = activity["height"]
        logger.info(
            f"saving activity to db: height {height}, avg_time {avg_time}, id_of_month {id_of_month}, year {year}"
        )
        db_controller.save_monthly_avg(height, avg_time, id_of_month, year)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        filename="../logs/calculate_monthly_activity.log",
        encoding="utf-8",
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    id_of_month = datetime.today().month
    year = datetime.today().year

    # always start a month behind so every entry is already saved in the db bevore calculating the totals
    if id_of_month == 1:
        id_of_month = 12
        year -= 1
    else:
        id_of_month -= 1

    logger.info(f"running calculate_daily_activity for {id_of_month}, {year}")
    check_and_save(id_of_month, year)
