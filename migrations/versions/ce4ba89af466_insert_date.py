"""_insert_date

Revision ID: ce4ba89af466
Revises: 7ef5fc66e415
Create Date: 2023-12-28 19:59:53.916722

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'ce4ba89af466'
down_revision: Union[str, None] = '7ef5fc66e415'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute(
        """
        INSERT INTO register ("RegName", "AreaName", "TerName", "RegTypeName", "TerTypeName")
        SELECT REGNAME, AREANAME, TERNAME, REGTYPENAME, TerTypeName
        FROM ZNO2019;
        """
    )

    op.execute(
        """
        INSERT INTO eo ("EOName", "EOTypeName", "EORegName", "EOAreaName", "EOTerName", "EOParent")
        SELECT EONAME, EOTYPENAME, EOREGNAME, EOAREANAME, EOTERNAME, EOPARENT
        FROM ZNO2019;
        """
    )

    op.execute(
        """
        INSERT INTO result_ukr ("UkrTest", "UkrTestStatus", "UkrBall100", "UkrBall12", "UkrBall", "UkrAdaptScale")
        SELECT UkrTest, UkrTestStatus, UkrBall100, UkrBall12, UkrBall, UkrAdaptScale
        FROM ZNO2019;
        """
    )

    op.execute(
        """
        INSERT INTO pt_ukr ("UkrPTName", "UkrPTRegName", "UkrPTAreaName", "UkrPTTerName")
        SELECT UkrPTName, UkrPTRegName, UkrPTAreaName, UkrPTTerName
        FROM ZNO2019;
        """
    )

    op.execute(
        """
        INSERT INTO student ("OutId", "Birth", "SexTypeName", "ClassProfileName", "ClassLangName")
        SELECT OUTID, Birth, SEXTYPENAME, ClassProfileNAME, ClassLangName
        FROM ZNO2019;
        UPDATE student 
        SET "Register_id" = (SELECT id FROM register WHERE id = student.id),
        "EO_id" = (SELECT id FROM eo WHERE id = student.id),
        "Result_Ukr_id" = (SELECT id FROM result_ukr WHERE id = student.id),
        "PT_Ukr_id"= (SELECT id FROM pt_ukr WHERE id = student.id);
        
        """
    )


def downgrade() -> None:
    pass
