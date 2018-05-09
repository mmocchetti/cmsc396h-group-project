'''
Temperature Container
'''
class TempHolder:
    range_start = 0
    range_end = 0
    
    star_count_lst = [0,0,0,0,0,0]
    counter = 0
    
    def __init__(self, in_range_start, in_range_end):
        self.range_start = in_range_start
        self.range_end = in_range_end
        self.counter = 0
        self.star_count_lst = [0,0,0,0,0,0]
        
    def is_in_temp_range(self, temp):
        if self.range_start <= temp and temp < self.range_end:
            return True
        else:
            return False
            
    def add_rating(self, rating):
        if int(rating) == 0:
            self.star_count_lst[0] += 1
        if int(rating) == 1:
            self.star_count_lst[1] += 1
        if int(rating) == 2:
            self.star_count_lst[2] += 1
        if int(rating) == 3:
            self.star_count_lst[3] += 1
        if int(rating) == 4:
            self.star_count_lst[4] += 1
        if int(rating) == 5:
            self.star_count_lst[5] += 1
        
        self.counter += 1
        
    def __str__(self):
        return_str = ""
        
        return_str += "Temp: " + str(self.range_start) + "-" + str(self.range_end) + "\n"
        return_str += "Count: " + str(self.counter) + "\n"

        if self.star_count_lst[0] == 0:
            return_str += "0 Stars: 0.00%\n" 
        else:
            return_str += "0 Stars: " + str(round((self.star_count_lst[0] / (self.counter * 1.0)), 4) * 100) + "%\n"
           
        if self.star_count_lst[1] == 0:
            return_str += "1 Stars: 0.00%\n"
        else:
            return_str += "1 Stars: " + str(round((self.star_count_lst[1] / (self.counter * 1.0)), 4) * 100) + "%\n"
            
        if self.star_count_lst[2] == 0:
            return_str += "2 Stars: 0.00%\n"
        else:
            return_str += "2 Stars: " + str(round((self.star_count_lst[2] / (self.counter * 1.0)), 4) * 100) + "%\n"
            
        if self.star_count_lst[3] == 0:
            return_str += "3 Stars: 0.00%\n"
        else:
            return_str += "3 Stars: " + str(round((self.star_count_lst[3] / (self.counter * 1.0)), 4) * 100) + "%\n"
            
        if self.star_count_lst[4] == 0:
            return_str += "4 Stars: 0.00%\n"
        else:
            return_str += "4 Stars: " + str(round((self.star_count_lst[4] / (self.counter * 1.0)), 4) * 100) + "%\n"
            
        if self.star_count_lst[5] == 0:
            return_str += "5 Stars: 0.00%\n"
        else:
            return_str += "5 Stars: " + str(round((self.star_count_lst[5] / (self.counter * 1.0)), 4) * 100) + "%\n"
        
        return return_str
        
class TempAnalysis:
    temp_holder_lst = list()
    
    def __init__(self):
        temp_counter = 0
        
        while temp_counter < 110:
            self.temp_holder_lst.append(TempHolder(temp_counter, temp_counter + 10))
            temp_counter += 10
    
    def add_rating(self, rating, temp):
        for temp_holder in self.temp_holder_lst:
            if temp_holder.is_in_temp_range(temp):
                temp_holder.add_rating(rating)
                return True
        
        return False
        
    def __str__(self):
        return_str = "Breakdown by Temperature:\n"
        return_str += "-------------------------\n"
        
        for temp_holder in self.temp_holder_lst:
            return_str += str(temp_holder) + "\n"
    
        return return_str
        
        
'''
Temperature Container
'''
class FRSHTTHolder:
    frshtt_code = ""
    
    star_count_lst = [0,0,0,0,0,0]
    counter = 0
    
    def __init__(self, in_frshtt_code):
        self.frshtt_code = in_frshtt_code
        self.counter = 0
        self.star_count_lst = [0,0,0,0,0,0]
        
    def is_in_code(self, in_frshtt_code):
        if self.frshtt_code == in_frshtt_code:
            return True
        else:
            return False
            
    def add_rating(self, rating):
        if int(rating) == 0:
            self.star_count_lst[0] += 1
        if int(rating) == 1:
            self.star_count_lst[1] += 1
        if int(rating) == 2:
            self.star_count_lst[2] += 1
        if int(rating) == 3:
            self.star_count_lst[3] += 1
        if int(rating) == 4:
            self.star_count_lst[4] += 1
        if int(rating) == 5:
            self.star_count_lst[5] += 1
        
        self.counter += 1
        
    def __str__(self):
        return_str = ""
        
        return_str += "Code: " + str(self.frshtt_code) + "\n"
        return_str += "Count: " + str(self.counter) + "\n"

        if self.star_count_lst[0] == 0:
            return_str += "0 Stars: 0.00%\n" 
        else:
            return_str += "0 Stars: " + str(round((self.star_count_lst[0] / (self.counter * 1.0)), 4) * 100) + "%\n"
           
        if self.star_count_lst[1] == 0:
            return_str += "1 Stars: 0.00%\n"
        else:
            return_str += "1 Stars: " + str(round((self.star_count_lst[1] / (self.counter * 1.0)), 4) * 100) + "%\n"
            
        if self.star_count_lst[2] == 0:
            return_str += "2 Stars: 0.00%\n"
        else:
            return_str += "2 Stars: " + str(round((self.star_count_lst[2] / (self.counter * 1.0)), 4) * 100) + "%\n"
            
        if self.star_count_lst[3] == 0:
            return_str += "3 Stars: 0.00%\n"
        else:
            return_str += "3 Stars: " + str(round((self.star_count_lst[3] / (self.counter * 1.0)), 4) * 100) + "%\n"
            
        if self.star_count_lst[4] == 0:
            return_str += "4 Stars: 0.00%\n"
        else:
            return_str += "4 Stars: " + str(round((self.star_count_lst[4] / (self.counter * 1.0)), 4) * 100) + "%\n"
            
        if self.star_count_lst[5] == 0:
            return_str += "5 Stars: 0.00%\n"
        else:
            return_str += "5 Stars: " + str(round((self.star_count_lst[5] / (self.counter * 1.0)), 4) * 100) + "%\n"
        
        return return_str
        
class FRSHTTAnalysis:
    frshtt_holder_lst = list()
    
    def __init__(self):
        # no weather
        self.frshtt_holder_lst.append(FRSHTTHolder("000000"))
        # rain
        self.frshtt_holder_lst.append(FRSHTTHolder("010000"))
        # thunder strom
        self.frshtt_holder_lst.append(FRSHTTHolder("010010"))
        # fog
        self.frshtt_holder_lst.append(FRSHTTHolder("100000"))
        # snow
        self.frshtt_holder_lst.append(FRSHTTHolder("001000"))
        # mixed (snow/rain)
        self.frshtt_holder_lst.append(FRSHTTHolder("011000"))
        # dry thunder
        self.frshtt_holder_lst.append(FRSHTTHolder("000010"))
        # hail
        self.frshtt_holder_lst.append(FRSHTTHolder("000100"))
    
    def add_rating(self, rating, frshtt_code):
        for frshtt_holder in self.frshtt_holder_lst:
            if frshtt_holder.is_in_code(frshtt_code):
                frshtt_holder.add_rating(rating)
                return True
        
        return False
        
    def __str__(self):
        return_str = "Breakdown by Code:\n"
        return_str += "-------------------------\n"
        
        for frshtt_holder in self.frshtt_holder_lst:
            return_str += str(frshtt_holder) + "\n"
    
        return return_str
