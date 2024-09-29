from db_controller import db_controller
from datetime import datetime, timedelta
import logging


# saves the daily_totals data to the db for every day that has not been saved till the last saved day
def check_and_save(day):
    # check if there is already data saved for this day
    logger.info(f"loading daily totals for day: {day}")
    activity = db_controller.get_daily_totals_entrys_of_day(day)

    if day_was_saved(activity):
        logger.info(f"day {day} was already saved")
        return

    save_day(day)
    check_and_save(day - timedelta(days=1))


def day_was_saved(activity):
    if len(activity) > 0:
        return True

    return False


def save_day(day):
    daily_activity = db_controller.get_totals_of_day(str(day))

    if len(daily_activity) == 0:
        logger.info(f"no activity for {day} found. Saving default")
        db_controller.save_daily_total(day, 0, "00:00:00")

    for activity in daily_activity:
        total_time = activity["total_time"]
        height = activity["height"]
        logger.info(
            f"saving activity to db: day {day}, height {height}, total_time {total_time}"
        )
        db_controller.save_daily_total(day, height, total_time)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        filename="../logs/calculate_daily_activity.log",
        encoding="utf-8",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    today = datetime.today().date()
    logger.info(f"running calculate_daily_activity for {today - timedelta(days=1)}")
    # always start a day behind today so every entry is already saved in the db bevore calculating the totals
    check_and_save(today - timedelta(days=1))
