from collections import namedtuple

from django.db import models


class Member(models.Model):
    user = models.ForeignKey(
        to='app.User',
        on_delete=models.CASCADE,
        verbose_name='Bruger'
    )
    club = models.ForeignKey(
        to='app.Club',
        on_delete=models.CASCADE,
        verbose_name='Klub'
    )
    active = models.BooleanField(
        default=False
    )
    marked_spam = models.BooleanField(
        default=False
    )
    invited_by = models.ForeignKey(
        to='app.User',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Inviteret af',
        related_name='invited_by'
    )
    date_joined = models.DateTimeField(
        auto_now_add=True
    )

    DTO = namedtuple("DTO", "id club date_joined user is_trainee is_coach is_admin")

    def is_trainee(self):
        return self.trainee_set.exists()

    def is_coach(self):
        return self.coach_set.exists()

    def is_admin(self):
        return self.admin_set.exists()

    def is_pending(self):
        return self.active is False and self.marked_spam is False

    def __dto__(self):
        return Member.DTO(
            id=self.id,
            club={
                'club_id': self.club_id,
                'link': '/api/v1/club/' + str(self.club_id) + '/'
            },
            date_joined=self.date_joined,
            user=self.user.__dto__(),
            is_trainee=self.is_trainee(),
            is_coach=self.is_coach(),
            is_admin=self.is_admin()
        )._asdict()

    @staticmethod
    def __dtolist__(members):
        return [m.__dto__() for m in members]

    class Meta:
        unique_together = ('user', 'club',)
