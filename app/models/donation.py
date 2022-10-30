from sqlalchemy import Column, ForeignKey, Integer, Text

from .template_model import TemplateModel


class Donation(TemplateModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
