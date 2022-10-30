from sqlalchemy import Column, String, Text

from .template_model import TemplateModel


class CharityProject(TemplateModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text(1), nullable=False)

    # def __repr__(self):
    #    return (
    #        f'Создано {self.create_date.isoformat(timespec="minutes")} '
    #        f'Нехватает {self.full_amount - self.invested_amount}'
    #    )
