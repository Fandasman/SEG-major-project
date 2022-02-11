"""Creates groups and assigns permissions for the groups for a chess club"""
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from clubs.models import User

class ChessClubGroups:

    #The club name is passed in to be used as a way of separating groups and permissions for each club
    def __init__(self, chess_club_name):
        self.chess_club_name = chess_club_name

        #Creates groups for club: names are club_codename + space + role name
        self.applicant_group, created = Group.objects.get_or_create(name = self.chess_club_name + ' Applicant')
        self.member_group, created = Group.objects.get_or_create(name = self.chess_club_name + ' Member')
        self.officer_group, created = Group.objects.get_or_create(name = self.chess_club_name + ' Officer')
        self.owner_group, created = Group.objects.get_or_create(name = self.chess_club_name + ' Owner')

        #Creates permissions for each club and assigns permissions to groups.
        user_content_type = ContentType.objects.get_for_model(User)
        self.member_list_permission = Permission.objects.create(
            codename = 'can_access_member_list_' + self.chess_club_name,
            name = 'Can access a basic list of members and some details for club ' + self.chess_club_name,
            content_type = user_content_type,
        )

        self.member_group.permissions.add(self.member_list_permission)
        self.officer_group.permissions.add(self.member_list_permission)
        self.owner_group.permissions.add(self.member_list_permission)

        self.full_member_list_permission = Permission.objects.create(
            codename = 'can_access_full_member_list_' + self.chess_club_name,
            name = 'Can access list of members with all information for club ' + self.chess_club_name,
            content_type = user_content_type,
        )
        self.officer_group.permissions.add(self.full_member_list_permission)
        self.owner_group.permissions.add(self.full_member_list_permission)

        self.applications_permission = Permission.objects.create(
            codename = 'can_accept_applications_' + self.chess_club_name,
            name = 'Can allow an applicant to become a member for club ' + self.chess_club_name,
            content_type = user_content_type,
        )
        self.officer_group.permissions.add(self.applications_permission)

        self.remove_member_permission = Permission.objects.create(
            codename = 'can_remove_member_' + self.chess_club_name,
            name = 'Can remove a member from the club for club ' + self.chess_club_name,
            content_type = user_content_type,
        )
        self.officer_group.permissions.add(self.remove_member_permission)

        self.promote_permission = Permission.objects.create(
            codename = 'can_promote_member_' + self.chess_club_name,
            name = 'Can promote a member to an officer for club ' + self.chess_club_name,
            content_type = user_content_type,
        )
        self.owner_group.permissions.add(self.promote_permission)

        self.demote_permission = Permission.objects.create(
            codename = 'can_demote_officer_' + self.chess_club_name,
            name = 'Can demote an officer to a member for club ' + self.chess_club_name,
            content_type = user_content_type,
        )
        self.owner_group.permissions.add(self.demote_permission)

        self.ownership_permission = Permission.objects.create(
            codename = 'can_transfer_ownership_' + self.chess_club_name,
            name = 'Can transfer owner status to an officer for club ' + self.chess_club_name,
            content_type = user_content_type,
        )
        self.owner_group.permissions.add(self.ownership_permission)

        self.become_owner_permission = Permission.objects.create(
            codename = 'can_become_owner_' + self.chess_club_name,
            name = 'Can receive ownership of club for club ' + self.chess_club_name,
            content_type = user_content_type,
        )
        self.officer_group.permissions.add(self.become_owner_permission)
