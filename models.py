from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
from sqlalchemy.orm import relationship

Base = declarative_base()


class Student(Base):
    __tablename__ = 'student'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    OutId = sa.Column(sa.String(100))
    Birth = sa.Column(sa.String(100))
    SexTypeName = sa.Column(sa.String(100))
    ClassProfileName = sa.Column(sa.String(100))
    ClassLangName = sa.Column(sa.String(100))

    Register_id = sa.Column(sa.Integer, sa.ForeignKey('register.id'))
    EO_id = sa.Column(sa.Integer, sa.ForeignKey('eo.id'))
    Result_Ukr_id = sa.Column(sa.Integer, sa.ForeignKey('result_ukr.id'))
    PT_Ukr_id = sa.Column(sa.Integer, sa.ForeignKey('pt_ukr.id'))

    register = relationship("Register", back_populates="student")
    eo = relationship("EO", back_populates="student")
    result_ukr = relationship("Result_Ukr", back_populates="student")
    pt_ukr = relationship("PT_Ukr", back_populates="student")


class Register(Base):
    __tablename__ = 'register'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    RegName = sa.Column(sa.String(100))
    AreaName = sa.Column(sa.String(100))
    TerName = sa.Column(sa.String(100))
    RegTypeName = sa.Column(sa.String(100))
    TerTypeName = sa.Column(sa.String(100))

    student = relationship("Student", back_populates="register")


class EO(Base):
    __tablename__ = 'eo'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    EOName = sa.Column(sa.String(1000))
    EOTypeName = sa.Column(sa.String(1000))
    EORegName = sa.Column(sa.String(1000))
    EOAreaName = sa.Column(sa.String(1000))
    EOTerName = sa.Column(sa.String(1000))
    EOParent = sa.Column(sa.String(1000))

    student = relationship("Student", back_populates="eo")


class Result_Ukr(Base):
    __tablename__ = 'result_ukr'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    UkrTest = sa.Column(sa.String(100))
    UkrTestStatus = sa.Column(sa.String(100))
    UkrBall100 = sa.Column(sa.String(100))
    UkrBall12 = sa.Column(sa.String(100))
    UkrBall = sa.Column(sa.String(100))
    UkrAdaptScale = sa.Column(sa.String(100))

    student = relationship("Student", back_populates="result_ukr")


class PT_Ukr(Base):
    __tablename__ = 'pt_ukr'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    UkrPTName = sa.Column(sa.String(1000))
    UkrPTRegName = sa.Column(sa.String(1000))
    UkrPTAreaName = sa.Column(sa.String(1000))
    UkrPTTerName = sa.Column(sa.String(1000))

    student = relationship("Student", back_populates="pt_ukr")