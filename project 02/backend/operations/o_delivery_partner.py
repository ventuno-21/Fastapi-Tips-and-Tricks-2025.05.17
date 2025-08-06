from typing import Sequence

from fastapi import HTTPException, status
from sqlmodel import select, any_

from ..schemas.s_delivery_partner import DeliveryPartnerCreate
from ..db.sqlmodel_models import DeliveryPartner, Shipment

from .o_user import UserService


class DeliveryPartnerService(UserService):
    def __init__(self, session, tasks):
        super().__init__(DeliveryPartner, session, tasks)

    async def add(self, delivery_partner: DeliveryPartnerCreate):
        return await self._add_user(
            delivery_partner.model_dump(),
            "partner",
        )

    async def get_partner_by_zipcode(self, zipcode: int) -> Sequence[DeliveryPartner]:
        """
        -> Sequence[DeliveryPartner]: The return type is annotated as
        a Sequence (like a list or tuple) of DeliveryPartner objects,
        where DeliveryPartner is likely a SQLAlchemy model representing
        a delivery partner entity in the database.


        any_(): This is a SQLAlchemy function specifically designed for
        working with array columns in databases like PostgreSQL.
        It generates a SQL ANY operator, which checks if a value (in this case, zipcode)
        exists within an array column (serviceable_zip_codes).
        In SQL terms, zipcode == any_(DeliveryPartner.
        serviceable_zip_codes) translates to a condition like
        zipcode = ANY(serviceable_zip_codes).
        For example, if a DeliveryPartner has
        serviceable_zip_codes = [12345, 67890],
        and the input zipcode is 12345, the condition checks if 12345
        is in the array [12345, 67890], returning True if it is.
        """
        return (
            await self.session.scalars(
                select(DeliveryPartner).where(
                    zipcode == any_(DeliveryPartner.serviceable_zip_codes)
                )
            )
        ).all()

    async def assign_shipment(self, shipment: Shipment):
        print(" ***  inside deliveryPartnerService/ assaign_shipment *** ")
        # print(
        #     "===>  inside deliveryPartnerService/ assaign_shipment/shipment.destination ====   ",
        #     shipment.destination,
        # )
        eligible_partners = await self.get_partner_by_zipcode(shipment.destination)
        # all_partners = await self.get_partner_by_zipcode(102)
        # print(
        #     " ===> inside deliveryPartnerService/ assaign_shipment/shipment.destination/eligible_partners ====   ",
        #     eligible_partners,
        # )
        for partner in eligible_partners:
            if partner.current_handling_capacity > 0:
                partner.shipments.append(shipment)
                return partner

        # If no eliglible partners found or
        # parters have reached max handling capacity
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f"No delivery partner available, This may cause because =>  first the delivery partner reached out its maximum capcity for specific zip_code/destination taht you provided, second, the zip_code/destination doesnt belong to any delivery partner ",
        )

    async def update(self, partner: DeliveryPartner):
        print(" ***************   Inside update delivery partner operation *********")
        return await self._update(partner)

    async def token(self, email, password) -> str:
        return await self._generate_token(email, password)
