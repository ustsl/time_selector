class TimeConventer:
    # formats a date string into minutes
    @staticmethod
    def hours_in_minutes(time):
        time = str(time).split(':')
        return (int(time[0]) * 60) + int(time[1])
    
    # formats a int minutes into date string
    @staticmethod
    def minutes_in_hours(time):
        def format_adapter(elem):
            if len(str(elem)) == 0:
                elem = '00'
            if len(str(elem)) == 1:
                elem = f'0{elem}'     
            return elem
        hours = format_adapter(time//60)
        minutes = format_adapter(time%60)
        return f'{hours}:{minutes}'
        
        
class TimeRangeValidator:
    # object for determining free time
    def __init__ (self):   
        self.tcr = TimeConventer()
        self.time_ranges = [(0,540), (1260, 1440)]
    
    # set busy time_ranges in a format [('17:30', '20:30'), ('10:30', '11:30'), ('12:20', '13:30')]
    def set_time_ranges(self, time_ranges):
        data = []
        for start, end in time_ranges:
            start = self.tcr.hours_in_minutes(start)
            end = self.tcr.hours_in_minutes(end)
            data += [(start, end)]
        self.time_ranges += data
    
    # checking user time range for intersection with busy times
    def is_time_range_included(self, user_time):
        for b_start, b_end in self.time_ranges:
            s_start = self.tcr.hours_in_minutes(user_time[0])
            s_end = self.tcr.hours_in_minutes(user_time[1])
            if b_start < s_start < b_end:
                print("Time is busy")
                return True
            elif b_start < s_end < b_end:
                print("Time is busy")
                return True
        print("Time is free")
        return False
    
    # obtaining suitable time ranges depending on the duration of the operation
    def get_free_time(self, duration):
        data = sorted(self.time_ranges) 
        free_time = []
        hours_free_time = []
        for elem in enumerate(data):
            if elem[0] > 0:
                free_minutes = elem[1][0] - data[elem[0] - 1][1]
                if free_minutes >= duration:
                    free_time += [(data[elem[0] - 1][1], elem[1][0])]
        for start, end in free_time:
            start = self.tcr.minutes_in_hours(start)
            end = self.tcr.minutes_in_hours(end)
            hours_free_time += [(start, end)]    
        print(hours_free_time)
        return hours_free_time
    
# EXAMPLE
user_time = ('15:30', '17:30')
time_ranges = [('17:30', '20:30'), ('10:30', '11:30'), ('12:20', '13:30')]

trv = TimeRangeValidator()
trv.set_time_ranges(time_ranges)
trv.is_time_range_included(user_time)
trv.get_free_time(100)