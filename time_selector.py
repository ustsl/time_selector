class TimeConventer:
    # formats a date string into minutes
    @staticmethod
    def hours_in_minutes(time):
        time = str(time).split(':')
        return (int(time[0]) * 60) + int(time[1])
    
    # formats a int minutes into date string
    @staticmethod
    def minutes_in_hours(time):
        def format_adapter(time_string):
            if len(str(time_string)) == 0:
                time_string = '00'
            if len(str(time_string)) == 1:
                time_string = f'0{time_string}'     
            return time_string
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
        time_ranges = []
        for start, end in time_ranges:
            start = self.tcr.hours_in_minutes(start)
            end = self.tcr.hours_in_minutes(end)
            time_ranges.append((start, end))
        self.time_ranges += time_ranges
    
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
        sorted_time_ranges = sorted(self.time_ranges) 
        free_time = []
        for couple_of_time in enumerate(sorted_time_ranges):
            if couple_of_time[0] > 0:
                free_minutes = couple_of_time[1][0] - sorted_time_ranges[couple_of_time[0] - 1][1]
                if free_minutes >= duration:
                    free_time.append((sorted_time_ranges[couple_of_time[0] - 1][1], couple_of_time[1][0]))       
        result = map(lambda couple_of_time: (self.tcr.minutes_in_hours(couple_of_time[0]), 
                                   self.tcr.minutes_in_hours(couple_of_time[1])), free_time)
        print(tuple(result))
        return tuple(result)
    
# EXAMPLE
user_time = ('15:30', '17:30')
time_ranges = [('17:30', '20:30'), ('10:30', '11:30'), ('12:20', '13:30')]

trv = TimeRangeValidator()
trv.set_time_ranges(time_ranges)
trv.is_time_range_included(user_time)
trv.get_free_time(100)