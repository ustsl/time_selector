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
            elif len(str(time_string)) == 1:
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
    
    # set busy time_ranges in a format [('17:30', '20:30', 0), ('10:30', '11:30', 30), ('12:20', '13:30', 30)]
    def set_time_ranges(self, str_time_ranges):
        int_time_ranges = []
        for time_couple in str_time_ranges:
            start = self.tcr.hours_in_minutes(time_couple[0])
            end = self.tcr.hours_in_minutes(time_couple[1])
            if len(time_couple) == 3:
                end += time_couple[2]  # if delay, end_time = end_time + delay
            int_time_ranges.append((start, end))
        self.time_ranges += int_time_ranges
    
    # checking user time range for intersection with busy times
    def is_time_range_included(self, user_time):
        for b_start, b_end in self.time_ranges:
            s_start = self.tcr.hours_in_minutes(user_time[0])
            s_end = self.tcr.hours_in_minutes(user_time[1])
            if len(user_time) == 3:
                s_end += user_time[2] # if delay, end_time = end_time + delay
            if b_start < s_start < b_end or b_start < s_end < b_end:
                print("Time is busy")
                return False
        print("Time is free")
        return True
    
    # obtaining suitable time ranges depending on the duration of the operation
    def get_free_time(self, duration=0, delay=0):
        duration+=delay
        sorted_time_ranges = sorted(self.time_ranges) 
        free_time = []
        for couple_of_time in enumerate(sorted_time_ranges):
            if couple_of_time[0] > 0:
                free_minutes = couple_of_time[1][0] - sorted_time_ranges[couple_of_time[0] - 1][1]
                if free_minutes >= duration:
                    free_time.append((sorted_time_ranges[couple_of_time[0] - 1][1], couple_of_time[1][0]))       
        result = map(lambda couple_of_time: (self.tcr.minutes_in_hours(couple_of_time[0]), 
                                   self.tcr.minutes_in_hours(couple_of_time[1])), free_time)
        return tuple(result)
    
    
# EXAMPLE
user_time_1 = ('15:30', '17:40', 30)
user_time_2 = ('15:30', '16:00', 30)
time_ranges = [('17:30', '20:30', 60), ('10:30', '11:30', 30), ('12:20', '13:30', 30)]

trv = TimeRangeValidator()
trv.set_time_ranges(time_ranges)
print(trv.is_time_range_included(user_time_1))
print(trv.is_time_range_included(user_time_2))
print(trv.get_free_time(60, 30))
# Time is busy
# False
# Time is free
# True
# (('09:00', '10:30'), ('14:00', '17:30'))