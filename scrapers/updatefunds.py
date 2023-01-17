from algeria.fund.models import Fund
import datetime
import csv

def run():
    """
    Function must be named 'run' so that django's 'runscript' command will work.
    Example command: ./manage.py runscript scrapers.updatefunds

    This funtion will delete all current entries of our 'Fund' models and replace
    them with the entries within the 'funds.csv' file

    WARNING: This function throws the following warning
        'RuntimeWarning: DateTimeField Fund.posted_date received a naive datetime (YYYY-MM-DD 00:00:00) while time zone support is active.'
    This is fine and can be ignored.
    """
    # Open the funds.csv file
    with open("scrapers/funds.csv") as file:
        # Create our reader.
        csv_reader = csv.reader(file)
        # Iterate past our header row.
        print(f"\n[DEBUG]\n{next(csv_reader)}")
        # Now that we know we have a file with data in it, it is somewhat safe to delete the old data.
        Fund.objects.all().delete()
        # Iterate through each row and populate new Funds
        for row in csv_reader:
            # ASSUMPTION: Each list representing a row is organzied as such [Title, Posted Date, Closed Date, Link, Source]
            title = row[0]
            source = row[-1]
            link = row[3]
            # Because we scrape two different sites, we have two different date formats. So we must check which one we have
            # and convert to pass django validation appropriately. (Convert to YYYY-MM-DD HH:MM)
            # ASSUMPTION: The two date formats we get are either mm/dd/yyyy or yyyy-mm-dd
            if("/" in row[1]):
                # Use datetime to convert our given date into our needed date.
                posted_date = datetime.datetime.strptime(row[1], "%m/%d/%Y").strftime("%Y-%m-%d")
            elif("-" in row[1]):
                posted_date = datetime.datetime.strptime(row[1], "%Y-%m-%d").strftime("%Y-%m-%d")
            # Django needs also needs "HH:MM" but our source does not give us that, so we will just append " 00:00" to our date (note the space).
            posted_date = posted_date + " 00:00"

            if(row[2] == ''):
                # Replace empty Closed Date with None to pass Django validation.
                closed_date = None
            else:
                if("/" in row[2]):
                    closed_date = datetime.datetime.strptime(row[1], "%m/%d/%Y").strftime("%Y-%m-%d")
                elif("-" in row[2]):
                    closed_date = datetime.datetime.strptime(row[1], "%Y-%m-%d").strftime("%Y-%m-%d")
                closed_date = closed_date + " 00:00"

            fund, is_created = Fund.objects.get_or_create(title=title, source=source, posted_date=posted_date, closed_date=closed_date, link=link)
            # Save the fund.
            fund.save()