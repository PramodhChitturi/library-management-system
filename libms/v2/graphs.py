from matplotlib import pyplot as plt
from mpld3 import fig_to_html
from datetime import datetime, timedelta

class Graph:
    
    def get_dates(self, days):
        date_obj = datetime.now()
        date_now = date_obj.date()
        all_dates = []
        count = 0
        while True:
            new_date = str(date_now)
            all_dates.append(new_date)
            count += 1
            if count == days:
                break
            date_now = date_now - timedelta(days= 1)
        all_dates.reverse()
        print(all_dates)
        print(len(all_dates))
        return all_dates
    def borrowAndReturn_VS_days(self, data, days):
        x_points = self.get_dates(days)
        plt.xlabel('dates')
        plt.ylabel("no.of.borrow/returns")
        
graph = Graph()
graph.borrowAndReturn_VS_days('adsf', 7)