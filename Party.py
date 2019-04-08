class Party:
    def __init__(self, mon1, mon2=None, mon3=None, mon4=None, mon5=None, mon6=None):
        self.mons = [mon1, mon2, mon3, mon4, mon5, mon6]

    def switch(self, num1, num2):
        self.mons[num1-1], self.mons[num2-1] = self.mons[num2-1], self.mons[num1-1]

    def __str__(self):
        str1 = ""
        for mon in self.mons:
            if mon is not None:
                str1 += str(mon)
                str1 += "\n"
        return str1

    def living_mons(self):
        available_mons = []
        for i in range(1, 5):
            if self.mons[i] is not None and self.mons[i].temp_stats[0] > 0:
                available_mons.append(i + 1)
        return len(available_mons)