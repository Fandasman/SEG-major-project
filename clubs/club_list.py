from .models import Club, User

class ClubList:
    def __init__(self):
        self.club_list = []
        for club in Club.objects.all():
            self.club_list.append(club)

    def get_all_clubs(self):
        return self.club_list

    def find_club(self, club_name):
        for club in self.club_list:
            if club.name == club_name:
                return club
        return None
